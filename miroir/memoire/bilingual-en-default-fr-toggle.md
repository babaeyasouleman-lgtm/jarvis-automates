---
name: bilingual-en-default-fr-toggle
description: "Sites for Souleman's Ottawa-area prospects default to English with a French toggle, in Canadian French."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 28a5a108-ea01-4ba2-a216-e879622ab1eb
  modified: 2026-07-29T21:51:40.201Z
---

Prospect sites default to **English** with a **French toggle** in the navbar — not
French-first, not English-only. Requested explicitly for the first prospect and treated
as the standing default, since these are Ottawa/Gatineau businesses serving both
communities.

Use **Canadian** French: *soumission* (not devis), *courriel* (not email),
*main-d'œuvre*, *territoire desservi*.

**Why:** the bilingual toggle is itself a selling point in his pitch — an Ottawa owner
immediately grasps its value, and their current site almost never has it.

**How to apply:** tag every string with `data-i18n`, keep English in the HTML and French
in a JS `FR` object, harvest English from the DOM at load so it is never duplicated.
Verify zero untranslated keys before delivering, and point out the FR button when
handing over the file so he can demo it live. Part of [[prospect-demo-workflow]].
