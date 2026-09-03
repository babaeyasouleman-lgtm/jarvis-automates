---
name: stock-photos-architectural-not-medical
description: "For medical prospect mockups, search architectural interiors on StockSnap rather than \"clinic\" or \"doctor\"; rawpixel via Openverse is watermarked and unusable."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: beedc5a0-8198-4612-9fe4-04135b430819
  modified: 2026-08-12T04:36:59.848Z
---

When a medical or clinical prospect needs stock photography, search Openverse for **architectural interiors** (`lobby interior`, `reception desk`, `minimal interior`, `wood interior`) filtered to `source=stocksnap&license=cc0`, not for `clinic`, `doctor` or `medical`.

**Why:** on Inovo Medical (2026-08-06) the medical queries returned posed groups in blue scrubs and dated masks, which is exactly what the prospect already had on their own site and what reads as cheap. The reference site Souleman sent, parodontielanaudiere.com, wins on an architectural interior photo of a real clinic, not on a medical stock photo. Interiors also carry zero faces, so nothing on the page can be mistaken for a real patient or employee, which is the hard line on a medical prospect.

**How to apply:** query StockSnap through Openverse only, and pass `source=stocksnap` as an API parameter so rawpixel never appears in the results at all. **rawpixel results are watermarked** and cannot be used, verified on nine downloads. StockSnap serves a maximum of 960px wide, so size every display slot below that and never stretch a hero across the full viewport: use `grid-template-columns:1fr minmax(0,940px)` so the colour panel absorbs any extra width.

**The CDN needs a browser User-Agent.** `cdn.stocksnap.io` returns a 4570-byte HTML page, not an image, unless the request carries both `-A "Mozilla/5.0 ... Chrome/120..."` and `-H "Referer: https://stocksnap.io/"`. Ten identical 4.5 KB files is the signature of this failure, so check `head -c 8 | xxd -p` for `ffd8ff` before building a contact sheet from them. Confirmed 2026-08-12 on Salon Amina beauté. Related: [[demo-delivery-single-html]], [[prospect-demo-workflow]].
