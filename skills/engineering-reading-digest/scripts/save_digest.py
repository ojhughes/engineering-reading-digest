#!/usr/bin/env python3
"""Save a completed digest with per-harness identity and revision history."""
import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import time
from urllib.parse import urlparse


@contextlib.contextmanager
def write_lock(root, timeout=20):
    """Shared by all digest, feed-index and access-log writers on this host."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    with (root / '.digest-write.lock').open('a') as lock:
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise TimeoutError('Digest writer busy; no files replaced')
                time.sleep(0.05)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def atomic_write(path, body):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.' + path.name + '-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def read_index(path):
    if not path.exists():
        return []
    # A malformed record is an error, not permission to lose earlier history.
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError('History records must be objects')
    return rows


def validate(record, markdown, harness, date):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', harness):
        raise ValueError('Harness must be a lowercase slug, not a path or model label')
    if dt.date.fromisoformat(date).isoformat() != date:
        raise ValueError('Date must be YYYY-MM-DD')
    if not markdown.strip() or not isinstance(record, dict) or not record.get('items'):
        raise ValueError('Only completed digests with selected items can be saved')
    seen = set()
    for item in record['items']:
        for key in ('url', 'title', 'publisher', 'publication_date', 'updated_date', 'tags'):
            if key not in item:
                raise ValueError('Missing item field: ' + key)
        parsed = urlparse(item['url'])
        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            raise ValueError('Invalid canonical URL')
        if item['url'] in seen:
            raise ValueError('Duplicate canonical URL')
        seen.add(item['url'])
        if not item['title'] or not item['publisher'] or not isinstance(item['tags'], list):
            raise ValueError('Invalid title, publisher or tags')
        for key in ('publication_date', 'updated_date'):
            if item[key] is not None:
                dt.date.fromisoformat(item[key])


def save(root, harness, date, markdown, record):
    validate(record, markdown, harness, date)
    root = Path(root).expanduser().resolve()
    ident = 'engineering-reading-' + harness + '-' + date
    filename = 'digest-' + harness + '-' + date + '.md'
    digest = root / filename
    index = root / 'index.jsonl'
    new = dict(record)
    new.update(digest_id=ident, harness=harness, digest_date=date, file=filename)
    new.pop('previous_versions', None)  # Preserve stored history, not caller guesses.
    new['content_sha256'] = hashlib.sha256(markdown.encode()).hexdigest()
    with write_lock(root):
        rows = read_index(index)
        matches = [r for r in rows if r.get('digest_id') == ident]
        if len(matches) > 1:
            raise ValueError('Duplicate digest identity in index; repair explicitly')
        old = matches[0] if matches else None
        previous = list(old.get('previous_versions', [])) if old else []
        old_current = {k: v for k, v in (old or {}).items() if k != 'previous_versions'}
        changed = old_current != new
        old_text = digest.read_text() if digest.exists() else None
        if not changed and old_text == markdown:
            return digest, False
        # Archive before replacing. Include orphan files left by an interrupted save.
        if old is not None or old_text is not None:
            old_blob = json.dumps(old_current, sort_keys=True) + '\n' + (old_text or '')
            token = hashlib.sha256(old_blob.encode()).hexdigest()[:16]
            base = root / 'history' / (ident + '-' + token)
            if old_text is not None:
                atomic_write(base.with_suffix('.md'), old_text)
            if old is not None:
                atomic_write(base.with_suffix('.json'), json.dumps(old, indent=2) + '\n')
                revision = dict(old_current)
                revision['archive_record'] = str(base.with_suffix('.json').relative_to(root))
                if old_text is not None:
                    revision['archive_file'] = str(base.with_suffix('.md').relative_to(root))
                if revision not in previous:
                    previous.append(revision)
        if previous:
            new['previous_versions'] = previous
        output = [r for r in rows if r.get('digest_id') != ident] + [new]
        encoded = ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in output)
        for line in encoded.splitlines():
            json.loads(line)
        # Each replacement is atomic, not a multi-file transaction. A retry repairs
        # a crash between writes; content_sha256 exposes a mismatched file/index.
        atomic_write(digest, markdown)
        atomic_write(index, encoded)
    return digest, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--harness', required=True)
    parser.add_argument('--date', required=True)
    parser.add_argument('--digest', required=True)
    parser.add_argument('--record', required=True)
    args = parser.parse_args()
    path, changed = save(args.root, args.harness, args.date,
                         Path(args.digest).read_text(), json.loads(Path(args.record).read_text()))
    print(json.dumps({'file': str(path), 'changed': changed}))


if __name__ == '__main__':
    main()
