# Engineering reading digest

A small experiment in using coding agents as engineering research assistants.

The skill searches broadly across engineering blogs, research, project documentation and community discussions. It follows promising links back to the original source, checks dates and claims, then produces a short reading digest.

I use it to find things worth reading around systems engineering, databases, Go, Java, Kubernetes, infrastructure and agent tooling. The topics are deliberately loose. The aim is to surface interesting work, including things I would probably not have found myself.

## Why?

There is far more good engineering writing than I can keep up with.

RSS feeds and link aggregators help, but they still leave most of the filtering to me. General AI summaries have the opposite problem: they are convenient, but can be shallow, repetitive or poorly sourced.

This experiment gives an agent a more deliberate research process:

- search across a broad range of sources
- use community sites as discovery signals rather than primary evidence
- read the original material before recommending it
- check publication dates and important claims
- remember previous selections to reduce repetition
- explain briefly why each item is worth reading

The result is closer to having someone spend an hour looking around the engineering internet for you.

## Example

Ask your agent:

> Generate my engineering reading digest.

The exact reader profile lives in [`prompt.md`](prompt.md), so it is easy to replace my interests with your own.ound the engineering internet for you.
## Using it

Clone the repository, and instruct your agent harness to install the skill.
Or simply run the prompt skills/engineering-reading-digest/SKILL.md
