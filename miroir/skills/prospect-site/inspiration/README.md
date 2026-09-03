# Inspiration screenshots

Drop image files in this folder. Read them before designing.

## Why this folder exists

I cannot screenshot a live site. Both routes are dead ends, tested repeatedly:

- The browser tool **times out after 300 seconds** on a real URL.
- The preview pane runs at **`visibilityState: "hidden"` with a 0x0 viewport**, so it never
  paints anything to capture.

So `scripts/inspect_motion.py` reads a site's **code**, which gives motion recipes with
real numbers, and that works well. But it tells me nothing about how a page *looks*:
spacing, rhythm, type size, where the weight sits, how generous the whitespace is. That
part only arrives as pixels, and the only pixels I can see are the ones he supplies.

Every visual rebuild so far traces back to this gap. On Maro I guessed cream and gold with
a light display serif; two screenshots showed the real thing in seconds.

## How to add one

Any common image format. Name it so the source and the intent are obvious:

```
venetianspa-hero.png
venetianspa-scroll-midpage.png
truekind-bubbles-around-image.png
spenceltd-nav-and-cursor.png
```

The pattern is `site-what-it-shows`. Two or three per site beats twenty.

**Most useful shots, in order:** the top of the page including the nav, one mid-page
section showing section rhythm and spacing, and any single component he specifically likes.

## How to use it

Before designing, list this folder and open anything relevant to the prospect's trade or to
the direction he asked for. Screenshots outrank my own taste, and they outrank the palette
guesses in the design database.

Then record what was actually taken from them in `MOTION.md`, so the reasoning
survives into the next build.

## If autonomous screenshots ever become worth it

`REFERENCES.md` lists **SawyerHood/dev-browser**, a Playwright-based tool that would let me
capture pages myself and remove this whole limitation. It is not installed, and installing
anything on his machine is his call, not mine. Worth raising if the screenshot round-trip
starts costing real time.
