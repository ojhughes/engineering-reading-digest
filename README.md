# Engineering reading digest

A reusable agent skill for producing engineering reading digests from public
sources. It covers systems, databases, Go, Java and the JDK, Kubernetes, DevOps,
and agent tooling.

The workflow discovers articles, reads the original material, checks claims and
dates, and uses saved reading history to avoid repeating earlier selections.
The source catalogue helps discovery without limiting it to familiar publishers.

## Getting started

1. Clone this repository:

   ```sh
   git clone https://github.com/ojhughes/engineering-reading-digest.git
   cd engineering-reading-digest
   ```

2. Open the checkout in an agent harness with public web access and local file
   access. Ask it to read `skills/engineering-reading-digest/SKILL.md` and generate
   a digest, using the checkout as the working root.

3. Adjust the reader profile in `prompt.md` to suit your interests. This is a
   relative symlink to the skill's maintained prompt.

You can also install the `skills/engineering-reading-digest` directory in your
harness's skill directory. Set `DIGEST_ROOT` to the absolute path of this checkout,
or provide that path explicitly when requesting a digest. The default working
root is `~/digests`.

The harness performs research using its own browsing and delegation tools. The
repository does not include a standalone crawler or scheduler. It supports
parallel discovery where the harness permits it, with a documented sequential
fallback.

## Contents

- [`prompt.md`](prompt.md): editorial rules, topic coverage and evidence requirements.
- [`sources.yaml`](sources.yaml): public feeds, article indexes and dated access observations.
- [`skills/engineering-reading-digest/SKILL.md`](skills/engineering-reading-digest/SKILL.md): workflow instructions.
- [`save_digest.py`](skills/engineering-reading-digest/scripts/save_digest.py): saves completed editions and reading history.
- [`storage.md`](skills/engineering-reading-digest/references/storage.md): storage format and concurrent write rules.

## Saving editions

The save helper requires Python 3 on macOS or Linux and uses only the standard
library. Source-index maintenance also needs a YAML parser, such as PyYAML,
available in the agent's environment.

```sh
python3 skills/engineering-reading-digest/scripts/save_digest.py --help
```

The skill explains how to prepare the Markdown digest and its JSON record.
Editions are saved as `digest-<harness>-<date>.md`. The helper retains revisions
and keeps selections in `index.jsonl` so different harnesses can share history.
Generated editions, history, access logs and scratch files are ignored by Git.
The source catalogue is tracked, so review changes before committing them.

## Contributing

Add substantive engineering sources and verify feed addresses before marking
them as working. Keep failed access attempts dated and specific to the method
used. Preserve the prompt's requirements for original-source reading and honest
uncertainty.

Use commit messages in this form:

```text
component-name: short description

Longer description explaining what changed and why.
```

## Licence

This repository is licensed under the [MIT licence](LICENSE). Linked articles
and other third-party material remain under their respective owners' terms.
