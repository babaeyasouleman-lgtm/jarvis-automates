---
name: prospect-demo-workflow
description: Souleman pitches web-design work by sending prospects a bilingual demo site of their own business; the /prospect-site skill automates it.
metadata: 
  node_type: memory
  type: project
  originSessionId: 28a5a108-ea01-4ba2-a216-e879622ab1eb
  modified: 2026-07-29T21:51:21.126Z
---

Souleman wins web-design clients by building an impressive demo of the prospect's own
site and emailing it to the owner *before* any contract, then building the real site if
they bite. First prospect: Alictro Electric Inc. (Ottawa electrician, alictro.ca),
2026-07-29.

The whole workflow is automated in the `prospect-site` skill at
`~/.claude/skills/prospect-site/` — invoke it with `/prospect-site <url>`. Its
`PREFERENCES.md` is the living record of his likes/dislikes and must be read before
building and updated after every delivery.

**Why:** this repeats for every new prospect, so the research → build → optimize →
inline → validate pipeline is worth running the same way each time instead of
rediscovering it.

**How to apply:** when he gives a company URL and wants something to show an owner,
invoke the skill rather than improvising. Deliverable is always ONE self-contained HTML
file — see [[demo-delivery-single-html]].
