---
name: demo-delivery-single-html
description: Deliver prospect demo sites as one self-contained HTML file with images inlined as base64 — never a ZIP.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 28a5a108-ea01-4ba2-a216-e879622ab1eb
  modified: 2026-07-29T21:51:30.465Z
---

Demo sites must be delivered as a **single self-contained `.html` file** with every
image inlined as a base64 `data:` URI. Do not produce a ZIP. His words, 2026-07-29:
"vu que c'est une demo en general je n'aurais pas besoin d'un zip mais juste du html
que j'envoie."

**Why:** he emails the file straight to the business owner. A folder loses its images
when only the HTML is attached, and a ZIP adds an unzip step that non-technical owners
abandon. One file means the owner double-clicks and it just works, offline.

**How to apply:** optimize the images first (target under ~1.5MB total so it clears any
mail provider), inline with the skill's `inline.py`, then gate delivery on `verify.py`.
Keep the working `index.html` + `assets/` folder for iteration, but hand him the single
file. Part of [[prospect-demo-workflow]].
