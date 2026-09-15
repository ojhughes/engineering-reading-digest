---
name: engineering-reading-digest
description: Produce a source-verified engineering reading digest covering systems, Go, Java, Kubernetes, DevOps and agent tooling, with cross-harness history and persistent source maintenance. Use for an engineering reading digest or its scheduled run.
---

# Engineering reading digest

Generate and return the complete digest, then save it with the executing harness
name. This skill uses plain Markdown, YAML and JSONL and no harness-specific SDK.

## Resolve the run

- Working root: explicit user path, then `DIGEST_ROOT`, then `~/digests`.
- Harness: explicit override, otherwise the actual host (`codex`, `claude`,
  `cursor`, etc.). Do not use the underlying model name. Use `unknown` and state
  the limitation only when the host cannot be established unattended.
- Date: current date in Europe/London unless the user specifies another date.
- Create a unique `.scratch/<harness>/<date>/<run-id>/` directory under the root.

Read the current `<root>/prompt.md` and `<root>/sources.yaml` on every run.
The prompt is the full editorial and evidence contract. If no local prompt
exists, read [references/prompt.md](references/prompt.md). If the source index is
missing, disclose it and use public discovery. On this installation, the root
prompt links to that reference so there is one maintained copy.

Read `index.jsonl`, its `previous_versions`, and relevant unindexed legacy
editions to exclude prior selections across all harnesses. Honour dated access
observations without treating publishers as permanently blocked.

## Discover and verify

Follow the prompt's A–D slice definitions and evidence contracts. Use native
subagents when available; run D early so its leads reach the technical workers.
Otherwise perform D, then A–C sequentially and state the limitation. Do not depend
on Codex tool names: use the current harness's supported delegation, browsing,
file and shell capabilities. Do not create user-facing tasks to emulate workers.

The parent owns shared writes. Workers return compact evidence and their own
maintenance observations. Verify every finalist's identity and date evidence,
and independently check at least three finalists' technical claims. Read source
content, not search snippets. Retain publisher-feed reading URLs when those
supply the article. A short brief must not mean shallow reading.

Unattended runs obey host permissions. Prefer public browsing tools if shell
network is unavailable. If an action cannot be permitted unattended, record it
and continue accessible work; never disable safeguards or invent a digest.

## Save

Prepare the full Markdown reply in a scratch file and a JSON record with `items`.
Each item requires `url`, exact `title`, `publisher`, `publication_date`,
`updated_date`, and `tags`; unavailable dates are JSON null. Add reading URLs,
date provenance, repeat reasons and verified attention where relevant, as the
prompt specifies.

Use the bundled standard-library Python helper (macOS/Linux):

```sh
python3 <skill-directory>/scripts/save_digest.py \
  --root <working-root> --harness <harness> --date <YYYY-MM-DD> \
  --digest <scratch-digest.md> --record <scratch-record.json>
```

It writes `digest-<harness>-<date>.md` and upserts
`engineering-reading-<harness>-<date>` in `index.jsonl`. Different harnesses and
dates coexist. Changed revisions are archived in `history/`, and their selection
metadata stays in `previous_versions` for repeat checking. Identical reruns are
idempotent. A failed run must never be passed to the saver as a finished digest.

The helper takes the shared `.digest-write.lock` only while saving. Source and
access-log maintenance must use the same advisory lock around a fresh
read/merge/write, merging observations rather than a stale whole-file snapshot.
Read [references/storage.md](references/storage.md) when performing these writes.
Return the entire digest in the conversation even if persistence fails, with an
honest note about any unsaved state.
