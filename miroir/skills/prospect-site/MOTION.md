# Motion inspiration

How to feed a site he likes into this skill, and the vanilla recipes that come out of it.

## The workflow: just send the URL

For **motion**, a screenshot is useless and a screen recording is not readable either.
The URL is better than both, because the page ships its own animation code and that code
says exactly what moves, by how much, and on what trigger.

```bash
python scripts/inspect_motion.py https://the-site-he-likes.com/page/
```

It reports the animation stack, the actual motion calls with their numbers, and the CSS
motion properties in use. That output is the recipe.

For **layout, colour and spacing**, screenshots are still the right input, since none of
that is reliably readable from markup. See the note in Step 1 of SKILL.md.

## Why the code gets rebuilt rather than copied

Two reasons, and the second one is the hard blocker:

1. Their JavaScript is their work. Techniques are not ownable, so identifying "this is a
   scroll-scrubbed clip-path reveal" and writing our own is normal practice. Lifting their
   file is not.
2. **The deliverable is one self-contained HTML file that must work offline.** A CDN tag
   for GSAP, Lenis or Swiper fails the moment the owner double-clicks the file with no
   network, and inlining a whole animation library blows the size budget. Every effect
   below is therefore written in plain CSS and JS, in a few lines each.

Everything here must sit behind `prefers-reduced-motion`, like the rest of the page.

---

## Recipes

### 1. Clip-path reveal on images (cheapest, biggest effect)

Seen on Venetian Spa: the image wrapper animates from a collapsed polygon to full, while
the image itself scales from 1.5 down to 1. The photo appears to unfold and settle.

```css
.reveal-img{overflow:hidden}
.js .reveal-img{clip-path:polygon(0 0,0 0,0 0,0 0)}
.js .reveal-img img{transform:scale(1.4)}
.js .reveal-img,.js .reveal-img img{
  transition:clip-path 1.05s cubic-bezier(.16,1,.3,1), transform 1.25s cubic-bezier(.16,1,.3,1)}
.js .reveal-img.in{clip-path:polygon(0 0,100% 0,100% 100%,0 100%)}
.js .reveal-img.in img{transform:scale(1)}
```

Add `.in` with the IntersectionObserver already in `mechanics.html`. No JS beyond that.

### 2. Corner radius that grows as you scroll

Their section rounds its top corners to 400px on scroll scrub. Striking, and it costs one
scroll handler.

```js
function scrubRadius(el, maxPx){
  function frame(){
    var r = el.getBoundingClientRect();
    var p = 1 - Math.min(Math.max(r.top / window.innerHeight, 0), 1); // 0..1 entering
    el.style.borderTopLeftRadius = el.style.borderTopRightRadius = (p * maxPx) + 'px';
  }
  addEventListener('scroll', function(){ requestAnimationFrame(frame); }, {passive:true});
  frame();
}
```

### 3. Heading that assembles letter by letter

They split the heading into characters and stagger each one up from `y:30` with 50ms
between letters. Split the text yourself, no library needed:

```js
function splitChars(el){
  var text = el.textContent;
  el.textContent = '';
  text.split('').forEach(function(ch, i){
    var s = document.createElement('span');
    s.textContent = (ch === ' ') ? ' ' : ch;
    s.style.cssText = 'display:inline-block;opacity:0;transform:translateY(30px);' +
      'transition:opacity .32s ease,transform .32s cubic-bezier(.16,1,.3,1);' +
      'transition-delay:' + (i * 0.035) + 's';
    el.appendChild(s);
  });
}
// on reveal: el.querySelectorAll('span').forEach(s => { s.style.opacity=1; s.style.transform='none'; })
```

Keep it for **one** heading per page. On every heading it becomes a tic.
Note it destroys the text node, so run it after the bilingual harvest, and re-run it on
language switch.

### 4. Vertical blinds opening over the hero

Their hero is covered by thin vertical strips that rotate open on scroll, each slightly
after the last. Build the strips in JS, drive `rotateY` from scroll progress:

```css
.blinds{position:absolute;inset:0;display:flex;perspective:1200px;pointer-events:none}
.blinds i{flex:1;background:var(--paper);transform-origin:left center;will-change:transform}
```

```js
var strips = hero.querySelectorAll('.blinds i');
addEventListener('scroll', function(){ requestAnimationFrame(function(){
  var r = hero.getBoundingClientRect();
  var p = Math.min(Math.max(-r.top / (r.height || 1), 0), 1);   // 0..1 through the hero
  strips.forEach(function(s, i){
    var d = Math.min(Math.max((p - i * 0.012) / 0.5, 0), 1);
    s.style.transform = 'rotateY(' + (90 * d) + 'deg)';
  });
}); }, {passive:true});
```

### 5. Smooth inertia scrolling (Lenis)

Their config: 1.4s duration on an exponential ease-out. This is the one effect worth
**skipping**. Reproducing real inertia means intercepting wheel events and driving scroll
position yourself, which fights trackpads, breaks anchor links and feels wrong on mobile.
A polished page without it beats a janky page with it. Use
`html{scroll-behavior:smooth}` for anchor jumps and stop there.

### 6. Centre-focused carousel

Their Swiper scales the centre slide to 1 and the neighbours to 0.75. Without Swiper:
CSS scroll-snap for the track, one IntersectionObserver to add `.is-centre` to whichever
slide is most visible, and a CSS transition on `transform:scale()`.

### 7. Pinned slide deck, the "dynamic anchor screen"

From racon360. One section pins to the viewport while an inner wrapper slides by exactly
one panel per screen of scrolling, and the anchor links scroll-to with an eased tween.
This is the single most impressive effect in the set and it is pure `position:sticky`
plus one transform.

```css
.deck{height:400vh}                 /* one extra 100vh per panel */
.deck-stage{position:sticky;top:0;height:100vh;overflow:hidden}
.deck-track{will-change:transform}
.deck-panel{height:100vh;display:grid;place-items:center}
```

```js
var deck=document.querySelector('.deck'), track=document.querySelector('.deck-track');
var n=track.children.length;
addEventListener('scroll',function(){ requestAnimationFrame(function(){
  var r=deck.getBoundingClientRect();
  var p=Math.min(Math.max(-r.top/(r.height-innerHeight),0),1);   // 0..1 across the deck
  track.style.transform='translateY('+(-p*(n-1)*100)+'vh)';
}); },{passive:true});
```

Give the anchor buttons `scrollTo` on the deck's own scroll range and the nav dots light up
from the same `p`. Set `.deck{height:auto}` and drop the transform under reduced motion.

### 8. Custom cursor that sticks to buttons

From spenceltd. A follower dot lerps toward the pointer, and when it enters a target it
**snaps to that element's centre** rather than tracking freely. That snap is what makes it
feel expensive. Their code also skews the dot by its velocity.

```css
@media (hover:hover){
  .cur{position:fixed;left:0;top:0;width:34px;height:34px;border-radius:50%;
       border:1px solid var(--maroon);pointer-events:none;z-index:999;
       transform:translate(-50%,-50%);transition:width .25s,height .25s,background .25s}
  .cur.stick{width:66px;height:66px;background:rgba(90,22,12,.1)}
}
```

```js
var cur=document.querySelector('.cur'), tx=0,ty=0,cx=0,cy=0,stick=null;
addEventListener('mousemove',function(e){ tx=e.clientX; ty=e.clientY; });
document.querySelectorAll('a,button').forEach(function(el){
  el.addEventListener('mouseenter',function(){ stick=el; cur.classList.add('stick'); });
  el.addEventListener('mouseleave',function(){ stick=null; cur.classList.remove('stick'); });
});
(function loop(){
  var gx=tx, gy=ty;
  if(stick){ var r=stick.getBoundingClientRect();
    gx=r.left+r.width/2 - (r.left+r.width/2-tx)*0.35;      /* partial snap */
    gy=r.top+r.height/2 - (r.top+r.height/2-ty)*0.35; }
  cx+=(gx-cx)*0.18; cy+=(gy-cy)*0.18;
  cur.style.transform='translate('+cx+'px,'+cy+'px) translate(-50%,-50%)';
  requestAnimationFrame(loop);
})();
```

Desktop only, behind `@media (hover:hover)`, and never hide the real cursor with
`cursor:none` on a business site: if the JS fails the visitor has no pointer at all.

### 9. Floating label bubbles around an image

From truekindskincare, the effect he described as words in bubbles around the photo. Pills
are absolutely positioned around a central image, each drifting on its own loop at a
different delay, and the whole group drifts slightly on scroll.

```css
.bub-wrap{position:relative;max-width:640px;margin-inline:auto}
.bub{position:absolute;background:#fff;border:1px solid var(--line);border-radius:100px;
     padding:11px 22px;font-size:14px;white-space:nowrap;box-shadow:0 10px 30px -18px rgba(0,0,0,.4)}
.bub:nth-child(1){top:8%;left:-8%}
.bub:nth-child(2){top:44%;right:-10%}
.bub:nth-child(3){bottom:10%;left:4%}
.js .bub{animation:drift 6s ease-in-out infinite}
.js .bub:nth-child(2){animation-delay:-2s}
.js .bub:nth-child(3){animation-delay:-4s}
@keyframes drift{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
```

Their bubbles carry the brand's three claims. For a trades prospect the equivalent is
"licensed", "same-week service", "written quote". Keep it to three, and on mobile drop
them below the image instead of overlapping it.

### 10. Glass panels

From fluid.glass, which is built almost entirely on this: `backdrop-filter: blur(10px)` on
small panels and `blur(2rem)` on large ones, over a background that moves.

```css
.glass{background:rgba(255,255,255,.55);backdrop-filter:blur(14px) saturate(150%);
       border:1px solid rgba(255,255,255,.6);border-radius:18px}
```

It only reads as glass if something textured sits behind it, so pair it with a photo or a
soft colour wash. Provide a solid fallback with `@supports not (backdrop-filter:blur(1px))`,
since the effect is expensive on low-end phones.

### 11. Clip-path inset reveal for a quote

From jannataresort's reviews. The quote is masked by an inset that opens, so the text wipes
in rather than fading. Cheaper and more elegant than a per-character split for long text.

```css
.js .quote-line{clip-path:inset(0 100% 0 0);transition:clip-path .9s cubic-bezier(.16,1,.3,1)}
.js .quote-line.in{clip-path:inset(0 0 0 0)}
```

Wrap each line in its own element and stagger `transition-delay` by about 120ms.

---

## Sites already inspected

### venetianspa.ca/about/ · 2026-08-03 · spa, Ottawa area

He flagged it for **the animations and how the site moves**.

Stack: GSAP + ScrollTrigger + Lenis + Swiper + Lottie, on WordPress and Elementor.

What it actually does, and the verdict for our mockups:

| Effect | Their numbers | Take it? |
|---|---|---|
| Clip-path image reveal, image scale 1.5 to 1 | trigger `top 65%`, once | **Yes.** Recipe 1. Best value on the page. |
| Top corners rounding on scroll | to 400px, scrubbed over 600px | **Yes.** Recipe 2. Distinctive, nearly free. |
| Heading split into characters | y 30, stagger 0.05, `power2.out` | **Yes, once per page.** Recipe 3. |
| Vertical blinds opening over the hero | `rotationY` to 0, stagger 0.005, scrubbed | Only when the hero photo can carry it. Recipe 4. |
| Lenis inertia scroll | duration 1.4, exponential ease | **No.** Recipe 5 explains why. |
| Carousel with a scaled centre slide | 1 vs 0.75 | Only if there are real photos to scroll. Recipe 6. |

Worth noticing: their reveals mostly fire at `top 65%` to `top 80%` and run `once`. The
page feels alive but never replays or fights the scroll. That restraint is as much of the
effect as the animations are.

### The 2026-08-04 batch

Seven sites he sent at once, with what he asked for in each. All inspected with `--deep`.

| Site | What he wanted | What it actually is | Take? |
|---|---|---|---|
| truekindskincare.com | "the way the claims are in bubbles around the image" | pills positioned around a photo, each on its own `translateY` loop, plus 67 parallax bindings and a marquee | **Yes.** Recipe 9. |
| racon360.com | "the dynamic anchor screen" | a pinned section whose inner track moves one panel per screen of scroll, with eased scroll-to on the anchors | **Yes.** Recipe 7. Best in the batch. |
| spenceltd.co.uk | "the navigation and cursor, the elevated feel" | cursor follower that lerps, then **snaps to the centre of whatever it hovers**, and skews with velocity | **Yes.** Recipe 8, desktop only. |
| jannataresort.com | "the comments section" | quote text revealed by an opening `inset()` clip-path, 122 magnetic-hover bindings, a marquee. Also loads all of animate.css, which is bloat | **Partly.** Recipe 11 only. |
| fluid.glass | (no note) | glassmorphism as the whole concept: 26 `backdrop-filter` rules, 10 sticky sections, gradient-masked text | **Sparingly.** Recipe 10. |
| luminouslabs.health | (no note) | GSAP counters that snap to whole numbers, image scale to 1.03 on hover, a width tween | Counter easing is worth copying, the rest we already do. |
| plumber-128.webflow.io | (no note) | plain Webflow IX2, 65 interactions, all standard fade and move-up on scroll | **Not for motion.** Its value is the **layout of a trades site**, which is the shape Alictro and Ouimette need. Look at it for structure, not animation. |

Two patterns worth noticing across the batch:

- Nobody is doing anything exotic. The whole set is `position:sticky`, `clip-path`,
  `transform`, and one lerp loop. Every effect above is 10 to 25 lines of vanilla code.
- The expensive feel comes from **restraint and timing**, not from the library. Reveals
  fire once, between `top 65%` and `top 80%`, and never replay.

**Budget for a mockup: two of these effects, not seven.** Pick the one that suits the trade
and one supporting move. Stacking a pinned deck, a custom cursor, floating bubbles and
glass panels on the same page produces exactly the overdesigned look he rejects.

## Reading a reference site's design tokens, not just its motion

`inspect_motion.py` answers "how does it move". When he says "make it more pared back like
X", the question is "how does it *look*", and a Webflow or Nuxt site's stylesheet answers
most of that without a single screenshot:

```bash
curl -sL URL -o ref.html
grep -oE 'href="[^"]+\.css[^"]*"' ref.html      # then fetch the big one
```

Then pull, in this order: `--custom-property` declarations (the author's own token names,
the most valuable thing in the file), the most frequent colours, `font-family`,
`border-radius`, and the `font-size` scale. Ten minutes of guessing replaced by facts.

**What it still cannot tell you:** section rhythm, whitespace, where the visual weight
sits, how the page is composed. That needs a screenshot in `inspiration/`.

### luminouslabs.health · 2026-08-04 · "quelque chose de plus épuré"

| Token | Value |
|---|---|
| Page | warm cream `#FCF8F1` |
| Surface | sand `#F2ECE2`, the most used colour on the site, 42 declarations |
| Strokes | `#DDD9D9`, very light |
| Dark | wine `#431616` |
| Accent | one, coral `#FF443A`, literally named `--highlight` |
| Type | Saans grotesque, plus **IBM Plex Mono** for micro-labels |
| Radii | 40 / 32 / 24 / 20px and 100px pills |
| Scale | 1rem base, ceiling 4.5rem |

**What "pared back" actually consists of here**, and what was reused on Divine: a warm
non-white background, exactly **one** accent colour, generously rounded corners, small
uppercase labels set in a **monospace**, restrained heading sizes, and almost no borders,
separation comes from surface changes instead. The mono label is the cheapest, most
distinctive borrow of the set.

### ristudio.in · 2026-08-04 · "inspire-toi mais garde-le épuré"

Supplied as screenshots, so this entry is about **composition**, which is the thing code
never tells you. A permanent-makeup studio in India.

What it does, and what was taken for Divine:

| Their device | Taken? |
|---|---|
| Large **italic serif set on the key word** of every heading, against an otherwise plain sans | **Yes**, the single most transferable idea. Fraunces italic 300, accent words only. |
| Big **photo tiles with the category word laid over the lower corner** (Eyelash, Eyebrow, Lips, Skin) | **Yes**, it became the services section: four tiles, the real service list under each. |
| Small images **overlapping the edge of a panel** | **Yes, once**, a rating card overlapping the portrait. Twice would be clutter. |
| Portrait beside a heavy near-black panel | **No.** Too dark for a page asked to stay pared back. Kept the cream. |
| Dense editorial mosaic on the blog | **No.** The opposite of pared back. |

**How to mix a maximalist reference into a pared-back brief:** take the *typographic* idea
and one composition device, leave the density and the dark panels. The restraint stays in
the palette and the spacing; the borrowed voice lives only in the accent words.

## Recovering a prospect's real photos when their site blocks you

Divine's live site answers 403 to everything. Their photos were still reachable through the
**Wayback Machine**, which is now the standard fallback:

```bash
curl -sL "https://archive.org/wayback/available?url=DOMAIN"
curl -sL "http://web.archive.org/cdx/search/cdx?url=DOMAIN%2Fwp-content%2Fuploads%2F*&output=text&fl=timestamp,original,statuscode&filter=statuscode:200&collapse=urlkey&limit=200"
```

Two traps that cost time:

1. **Each image has its own capture timestamp.** Building an image URL from the *page*
   snapshot timestamp returns 404 every time. Take the timestamp from the CDX row for that
   exact file.
2. Ask CDX for the uploads directory, not the page. Most captures are resized variants;
   filter out `-WxH` suffixes to find full-size originals, and fall back to the largest
   variant when no original was archived.

This recovered the founder's real professional portrait at 1365x2048, which is what finally
gave that build a face.

### rierastudio.com/en/ · 2026-08-04 · "inspire-toi des effets de ce site"

A landscape studio in Catalonia. Sent with a screenshot **and** the URL, so both channels
were available for once. His note: *"C'est beaucoup trop vert mais je veux quelque chose de
plus originale et moderne comme celui la... Tu viens de me fournir un autre site IA
generated."*

Stack: GSAP + ScrollTrigger (43 refs) + ScrollSmoother (18 refs), on WordPress.

| Their device | Take? |
|---|---|
| **Marquee, 17 of them** | **Yes.** The one motion effect actually worth lifting here. Was on the Q4 option list and had never been used in a build. |
| ScrollTrigger reveals, 43 bindings | Yes, but we already do this. Pair it with recipe 1 on photos. |
| ScrollSmoother inertia | **No.** Recipe 5 already says why. |
| `#pageTransition` overlay between pages | **No.** A one-page mockup has nothing to transition to. |
| One pinned section | No, and see the scroll-jacking note in SKILL.md. |

**The motion was not the point.** `inspect_motion.py` returned almost no numbers because the
calls sit inside GSAP's own minified internals. What makes the page look the way it does is
composition, and that only came from the screenshot:

| Their device | Taken for Envert? |
|---|---|
| **Zero border radius anywhere.** Every photo, panel and button is a hard rectangle | **Yes**, and this is the single biggest anti-AI move available. Rounded cards plus soft shadows plus pill buttons is the generic-template signature he keeps rejecting. |
| **Nav split into separate bordered cells** with 1px dividers, uppercase and letterspaced, the active cell filled | **Yes.** Distinct from every previous nav. |
| **Large hand-drawn botanical line art** in a bright green, laid over the background at big scale, bleeding off the edges | **Yes**, redrawn as our own SVG in the prospect's own logo green. Follows the validated "visuals drawn in code, not stock or AI photos" preference. |
| **Photos as hard rectangles scattered at different vertical offsets**, some running off the viewport edge | **Yes.** Replaces the two-column hero. |
| **An exposed column grid**, thin vertical rules left visible | **Yes**, once, in the materials band. |
| Near-black-green canvas across the whole site | **No.** He said too green. Bone canvas instead, near-black for dark blocks, green demoted to line art and accents. |
| Floating WhatsApp button | No. |

**How to take a very green reference for a prospect whose brand is also green:** keep the
structure and the illustration idea, move the green off the canvas and onto the line work.
The prospect's own `#00A651` sits in the same family as Riera's mint, so the borrowed device
lands as native brand rather than as a copy, and a second warm accent (clay) stops the page
reading as monochrome green.

---

## Quand il envoie un composant 21st.dev

Le prompt que 21st génère suppose un projet React avec shadcn, Tailwind et TypeScript, et il
demande de créer `/components/ui`, d'installer des paquets npm et de remplir les images avec
du stock Unsplash. **Rien de tout cela ne s'applique ici.** Notre livrable est un fichier HTML
autonome qui doit s'ouvrir hors ligne par double-clic, donc:

- pas de build, pas de `/components/ui`, pas de `npm install`
- `framer-motion`, `embla-carousel-react`, `lucide-react` et `class-variance-authority` sont
  hors budget, et un tag CDN casse le hors-ligne de toute façon
- **ignorer l'étape "fill image assets with Unsplash stock images"**, elle contredit
  directement la règle du skill: aucune photo stock dans une maquette, jamais
- les icônes `lucide-react` se redessinent à la main en SVG inline, 24x24, `stroke-width`
  autour de 1.4, `stroke-linecap="round"`. Une icône coûte une ligne.

Ce qu'il faut lire dans un composant React, c'est **les nombres et la structure**, pas le code.
Le JSX donne gratuitement les tailles, les délais et les états, ce qui est exactement ce
qu'on cherche à retrouver quand on inspecte un site en direct.

### Recette 10. Carrousel de cartes de service

Repris du composant `services-card.tsx` que 21st a produit, adapté en CSS et JS pur pour
Paramédika. Ce que le JSX donnait: carte de 450px, `rounded-3xl`, `p-8`, dégradé par carte,
numéro `( 001 )` en mono à 50 % d'opacité en haut, icône de 48px poussée en bas par
`mb-auto`, titre en capitales avec `tracking-wider` et description en bas, entrée
`opacity 0 → 1` et `y 50 → 0` sur 0,5 s avec un retard de `index * 0.1` s, voile
`bg-gradient-to-t from-background/20` par-dessus, et une flèche ronde de navigation.

**Le retard de 0,1 s par carte se branche sur l'observateur de `mechanics.html` sans rien
ajouter**, il suffit de monter le pas de 70 ms à 100 ms et le plafond de 350 ms à 500 ms.
La classe `.rv` fait déjà `translateY`, il faut juste passer de 22px à 50px.

**Embla se remplace par du `scroll-snap` natif**, ce qui est plus court et donne le glissement
tactile gratuitement:

```css
.ctrack{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
.ctrack::-webkit-scrollbar{display:none}
.scard{flex:0 0 calc((100% - 36px)/3);scroll-snap-align:start;height:450px}
```

```js
function step(){                       /* largeur d'une carte plus l'écart */
  var c=track.querySelector('.scard');
  var gap=parseFloat(getComputedStyle(track).columnGap)||18;
  return c.getBoundingClientRect().width+gap;
}
function maxScroll(){return track.scrollWidth-track.clientWidth;}
next.onclick=function(){                                  /* le loop:true d'embla */
  if(track.scrollLeft>=maxScroll()-4) track.scrollTo({left:0,behavior:'smooth'});
  else track.scrollBy({left:step(),behavior:'smooth'});
};
```

**La barre de progression vaut le détour**, elle remplace les points et dit combien il reste:

```js
var seen=track.clientWidth/track.scrollWidth;             /* 3 cartes sur 8 = 37,5 % */
bar.style.width=(seen*100)+'%';
bar.style.transform='translateX('+(track.scrollLeft/maxScroll())*((1/seen)-1)*100+'%)';
```

**Le piège des dégradés.** Le composant livre du violet, du vert, du rouge et du bleu, soit
exactement la palette arc-en-ciel que la base de design signale comme un marqueur IA. Il faut
les remplacer par des teintes tirées du logo du prospect, deux ou trois qui alternent, pas une
par carte. Sur Paramédika: blush, sable, mauve et pêche, toutes dans le voisinage du magenta.

**Le contenu des cartes doit rester réel.** Le composant invite à écrire une description par
carte. Sur un prospect médical, écrire 8 descriptions de traitements est une invention et
c'est interdit. Ce qui a marché: la carte porte le numéro, l'icône, la famille de soin et
**la liste des vrais noms de soins du prospect**. Zéro phrase inventée, et la carte est plus
dense qu'avec une ligne de marketing.

### Sites et composants déjà inspectés

| Source | Ce qui en est sorti |
|---|---|
| 21st.dev `services-card.tsx` | Recette 10, carrousel de cartes de service (Paramédika, 2026-08-05) |

---

## vicpark.com (Médispa Victoria Park), inspecté 2026-08-05

`inspect_motion.py` sans `--deep` ne rend **rien**: WordPress core seulement. Avec `--deep`
il rend tout. **Toujours refaire la passe profonde sur un site WordPress**, sinon on conclut
à tort qu'il n'y a pas de mouvement.

Pile: **GSAP 46, ScrollTrigger 66, SplitText 23, ScrollSmoother 17, Barba**. 20 épinglages,
3 scrubs.

Les appels qui valent la peine, avec leurs vrais nombres:

| Leur code | Ce que ça fait |
|---|---|
| `.to(".bk-mini-circle-reveal--container",{width:"100%",height:t+100+"px"})` | **Le cercle qui grandit.** C'est l'effet qu'il a remarqué. |
| `.from(t.lines,{x:100,opacity:.01,ease:"power3",stagger:.2,duration:1,delay:.5})` | Entrée du titre par lignes, depuis la droite. |
| `.fromTo(".trait-presentation .first",{x:"-60vw"},{x:"0",scrollTrigger:{start:"top 100%",end:"top 10%",scrub:!0}})` | Deux blocs qui entrent en sens inverse, scrubés. |
| `.to("header.header",{y:-110})` avec `start:"top 0",end:"+=210",scrub:!0` | La nav se rétracte sur 210px de défilement. |
| `.to(".arc-cream",{"--bg-pos":"-22vw"})` `start:"top 150%",end:"top 50%"` | Arc révélé par variables CSS scrubées. |
| `.from(e,{opacity:.01,y:20,stagger:.2,scrollTrigger:{start:"top 80%",end:"top 40%",scrub:1}})` | Fondu d'entrée scrubé, pas déclenché. |

### Recette 11. Le cercle scrubé qui grandit puis rétrécit

Leur version grandit seulement. La version ci-dessous **grandit et rétrécit selon la position
dans la fenêtre**, ce qui est ce qu'il a décrit et ce qui se sent mieux dans les deux sens de
défilement. Le `smoothstep` est ce qui empêche l'effet de paraître linéaire et mécanique.

```js
var r = section.getBoundingClientRect();
var c = r.top + r.height/2, vc = innerHeight/2;
var d = Math.abs(c - vc) / (vc + r.height/2);
var p = 1 - Math.min(Math.max(d,0),1);      // 1 au centre, 0 aux bords
var e = p*p*(3-2*p);                        // smoothstep
el.style.transform    = 'scale(' + (0.58 + e*0.42) + ')';
el.style.borderRadius = (50 - e*36) + '%';  // cercle en petit, bloc arrondi en grand
```

Le `border-radius` qui suit l'échelle est ce qui reproduit leur `circle-reveal`: petit c'est un
disque, plein écran c'est un bloc. Coûte un `requestAnimationFrame` sur `scroll`, zéro
bibliothèque, et `transform:none!important` sous `prefers-reduced-motion`.

### Sites et composants déjà inspectés

| Source | Ce qui en est sorti |
|---|---|
| vicpark.com | Recette 11 plus la structure complète, Paramédika v5, 2026-08-05 |
| clinique7.com | Recette 12, texte qui se matérialise au défilement. Envoyé comme référence pour Infinium, 2026-08-11 |

## clinique7.com, 2026-08-11, envoyé comme inspiration pour Clinique Infinium

Chirurgien solo de rhinoplastie à Montréal (Dr Zahi Abou Chacra), site Tilda. Demandé:
naviguer comme un humain et prendre des captures. **Impossible avec les outils de cette
session**, ni navigateur en direct (délai de 300s) ni volet d'aperçu (0x0, jamais peint), donc
tout ce qui suit vient du code, pas de pixels vus. Il faudra ses captures pour la composition
réelle, voir `inspiration/README.md`.

Pile: **GSAP + ScrollTrigger + Lenis**, glassmorphism lourd (22 `backdrop-filter`, `blur(15px)`
et `blur(26px)`), un curseur personnalisé signalé par le détecteur mais non localisé dans le
code accessible, une galerie horizontale en glisser-déposer (**ScrollBooster**, pas un vrai
effet, une librairie de drag-to-scroll que notre `scroll-snap` natif remplace déjà).

| Leur device | Ce que ça fait | Neuf? |
|---|---|---|
| **Texte qui se matérialise au défilement, caractère par caractère** | Chaque lettre d'un paragraphe est éclatée en `<span>`, et l'opacité de chaque span est recalculée en continu sur `scroll` à partir de sa position `top`/`left` réelle dans la fenêtre, pas d'un déclenchement unique par IntersectionObserver | **Oui, recette 12 ci-dessous.** Différent de la recette 3 (éclatement en lettres, une seule fois, `stagger`): ici c'est continu et scrubé, l'effet rejoue si on remonte. |
| **Avant/après par survol ou clic**, pas un curseur glissant | "HOVER OVER PHOTOS TO SEE THE BEFORE" / "CLICK ON PHOTOS TO SEE THE BEFORE" | Device alternatif à noter: nos cinq derniers prospects médicaux utilisent tous le curseur `input[type=range]`. Un simple `.on-hover{opacity:0}` au survol serait plus léger et casserait la répétition. |
| Lenis, `duration:1.2` | Inertie de défilement | **Non**, recette 5 déjà tranchée. |
| Glassmorphism, 22 occurrences | Panneaux flous sur fond sombre | Recette 10, déjà couverte. |
| Services numérotés 01 à 05 | Rhinoplastie primaire, de révision, ethnique, liquide, procédures complémentaires | Device déjà utilisé (Ouimette, Inovo), rien de neuf. |

**Palette et type, à prendre avec précaution sur Infinium.** Fond très majoritairement
`#000000`/`#111`/`#181818`, panneaux clairs `#eaeaea` en alternance, un seul accent corail
chaud `#ff8562`. Typo `Cormor` (probablement un nom local pour une serif fine, type
Cormorant) en titrage plus Arial en corps, et une police nommée `tfutura` par endroits.
Rayons mixtes: `3px` sur certains éléments, `100px`/`1000px` en pilule sur les boutons.

**Correction après captures d'écran, 2026-08-11.** L'analyse ci-dessus, faite sur les seuls
comptes de couleur du CSS, concluait à un site presque noir. **C'était faux, et c'est
exactement le piège que ce fichier lui-même met en garde contre** («ce que le code ne peut
pas dire: le rythme, l'espace blanc, où se pose le poids visuel»). Trois captures reçues,
sauvegardées dans `inspiration/clinique7-hero.png`,
`inspiration/clinique7-sculpture-busts-scattered.png` et
`inspiration/clinique7-philosophy-scrim.png`.

**La page rendue est en réalité claire.** Toile gris pierre très pâle (proche de leur
`#eaeaea`), texte encre quasi noire, un seul accent chaud. Le presque-noir compté dans le CSS
vient d'un **voile en dégradé posé sur UNE section photo** (`clinique7-philosophy-scrim.png`),
pas d'un fond de page. Une fois vu, le palette clash redouté n'existe pas: Infinium est déjà
sur une toile claire avec une encre foncée et un seul accent, c'est la même charpente avec
une teinte différente.

Ce que les captures montrent, que le code ne disait pas:

| Device | Description | Transférable à Infinium? |
|---|---|---|
| **Phrase en serif italique géant, au milieu d'une phrase en sans-serif** | "The brand behind **_beautiful_** noses": "beautiful" seul est démesuré (largeur proche de "brand behind" sur deux mots), en italique fine, au milieu d'une ligne autrement en grotesque noir plein. Pas un mot coloré comme sur Divine, un **changement de police et d'échelle** au milieu de la phrase. | **Oui, le plus transférable.** Plus audacieux que l'accent couleur simple déjà livré sur "Gatineau". |
| **Bustes classiques (sculptures gréco-romaines) en grille éparpillée**, décalage vertical irrégulier, traitements de teinte variés (sépia, N&B, fond noir, duoton bleu-teal) | Motif "le nez comme objet d'art / histoire de l'art", très spécifique à un chirurgien de rhinoplastie unique | **Non, pas tel quel.** C'est un habillage propre à leur spécialité et à leur philosophie déclarée ("l'Art de la Rhinoplastie"), pas à une clinique multi-services. Récupérer le *principe* (visuels abstraits/artistiques à la place de photos de personnes, puisqu'eux non plus n'ont pas de vraies photos exploitables) plutôt que le motif littéral. |
| **Objet abstrait sculptural/papier plié**, gris, en volume, posé derrière le titre du héros à la place d'une photo | Remplace élégamment l'absence de photo utilisable | **Oui, en principe.** Precedent direct pour Infinium, qui a aussi zéro photo utilisable: un objet dessiné en SVG (pas une image stock) à la place d'une photo de héros. |
| **Voile dégradé sombre sur UNE SEULE section photo**, pour porter une citation de philosophie en capitales à faible opacité | Le paragraphe exact repéré dans le code ("Dr. Chacra's philosophy is that...") est bien celui qui reçoit la recette 12 (matérialisation lettre par lettre au défilement) | **Oui.** Un bloc à fort contraste, une fois par page, est cohérent avec la règle "donner plus de poids visuel à une section que les autres". |
| **Badge circulaire du logo** (sceau "CLINIQUE 7 MONTRÉAL RHINOPLASTIE") | Le logo lui-même est un sceau rond | **Non.** Le logo d'Infinium est un mot-symbole horizontal, pas un sceau. Ne pas forcer une forme ronde sur une identité qui n'en a pas. |
| **Espacement de nav asymétrique**, grand vide entre "Learning Centre" et "Out Of Town" plutôt qu'une justification régulière | Détail typographique | Mineur, pas nécessaire de le reprendre. |
| **Boutons pilule noirs pleins** | Cohérent avec le rayon `100px`/`1000px` déjà repéré dans le CSS | Infinium est en rayon 0 par défaut (aucune référence arrondie envoyée au moment du build). À netrancher que si le choix devient conscient. |

**Verdict révisé: pas de conflit de palette à trancher.** Ce qu'il y a à décider, c'est
lequel de ces devices entre dans Infinium, pas si la couleur sombre doit remplacer le
gris-cyan déjà validé.

### Recette 12. Texte qui se matérialise au défilement, lettre par lettre

Contrairement à la recette 3 (éclatement en lettres, révélé une fois via IntersectionObserver
avec un `stagger` fixe), celle-ci **recalcule l'opacité de chaque lettre à chaque `scroll`**,
à partir de sa position réelle dans la fenêtre. L'effet est continu: il rejoue si on remonte,
et la vitesse de matérialisation suit la vitesse de défilement au lieu d'un minutage fixe.

```js
function splitCharsScrub(el){
  var text = el.textContent; el.textContent = '';
  text.split('').forEach(function(ch){
    var s = document.createElement('span');
    s.textContent = ch; s.style.display='inline-block';
    el.appendChild(s);
  });
  return Array.prototype.slice.call(el.querySelectorAll('span'));
}
function wireScrub(paragraphs){
  var spans = paragraphs.flatMap(splitCharsScrub);
  function reveal(){
    spans.forEach(function(s){
      var r = s.getBoundingClientRect();
      var top = r.top - window.innerHeight * 0.1 - 600;   /* tune the two constants per layout */
      var o = 0.5 - (top * 0.01 + r.left * 0.001);
      s.style.opacity = Math.max(0.1, Math.min(1, o)).toFixed(3);
    });
  }
  window.addEventListener('scroll', reveal, {passive:true});
  reveal();
}
```

Coûte un `scroll` non throttled sur leur site (pas de `requestAnimationFrame`, à corriger
dans notre version: enrober `reveal` d'un `requestAnimationFrame` pour rester fluide). Le
plus adapté à **un seul paragraphe long et important par page**, jamais à un titre court ni
à plusieurs blocs, sinon l'œil ne sait plus où regarder pendant le défilement.
