# Shared storage

The working root holds live state, independent of where a harness finds the skill:

- `prompt.md`: current editorial contract; read every run.
- `sources.yaml`: current feed index and scheduling observations; read every run.
- `digest-<harness>-<date>.md`: completed edition for one harness and date.
- `index.jsonl`: one record per harness/date, plus untouched legacy records.
- `history/`: archived revisions. Each current record's `previous_versions`
  retains earlier item metadata for exclusions without opening every archive.
- `access-failures.jsonl`: observations keyed by URL, fetching method and date.
- `.scratch/<harness>/<date>/<run-id>/`: isolated workers, caches and run reports.
- `.digest-write.lock`: advisory lock shared by writers, not held during research.

## Maintenance writes

When writing source observations or access logs, load the saver as a Python
module and use its `write_lock(root)` and `atomic_write(path, text)` functions.
Inside the lock, re-read the current file, merge only the fields observed in this
run, validate the resulting YAML or JSONL, then replace it. Never write a stale
whole-file snapshot after another harness may have changed it.

Feed identity is its URL, not its label. Keep `last_checked` from each actual
attempt; successful parsing alone updates `latest_ok` and `latest_item`. Preserve
older successful fields on failure. Include method, raw date value/field and
conditional-request validators where observed. A parser limitation is not proof
of an invalid publisher feed. Derive counts after merging.

Use an already-installed YAML parser. If none is available unattended, save the
observations in scratch and report that index maintenance was deferred; do not
install packages or pretend the YAML was validated. The digest saver requires
only the standard Python library on macOS or Linux.

## History behaviour

The saver validates all new records before replacing files, locks and re-reads
history, and only replaces the exact `engineering-reading-<harness>-<date>` ID.
It preserves unrelated harnesses and legacy records. Same-content, same-metadata
retries are no-ops. Changed metadata or content archives the previous version.
Each file replacement is atomic; the digest and index are not a single filesystem
transaction. The stored content hash allows an interrupted save to be detected,
and repeating the same save repairs it.

Do not silently assign a legacy edition to a harness. Migrate only when its
provenance is established, retaining an archive and the original file. A failed
research run belongs in scratch and must not overwrite a successful edition.
