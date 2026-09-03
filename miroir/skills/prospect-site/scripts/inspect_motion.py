#!/usr/bin/env python3
"""
Read a site he likes and report HOW it moves.

    python scripts/inspect_motion.py https://example.com/page/
    python scripts/inspect_motion.py https://example.com/ --deep

Prints the animation stack, the actual motion calls with their numbers, and the CSS
motion properties in use. That is the recipe.

--deep also downloads the page's own JS and CSS bundles and scans those. Needed for
Webflow, Nuxt, Next and any site that keeps its animation code in an external file,
which is most of them. Without --deep those sites report "none detected".

We rebuild each effect in vanilla CSS and JS. The deliverable is one offline HTML
file: a CDN copy of GSAP would fail the moment the owner double-clicks it with no
network, and their JavaScript is theirs, not ours to ship.

Standard library only.
"""
import re
import sys
import urllib.request
import urllib.parse

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-CA,en;q=0.9,fr;q=0.8",
    "Accept-Encoding": "identity",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}

MAX_ASSETS = 10
MAX_ASSET_BYTES = 1_500_000

LIBS = [
    ("GSAP",            r"gsap(?:\.min)?\.js|\bgsap\.(?:to|from|fromTo|timeline|set|utils)"),
    ("ScrollTrigger",   r"ScrollTrigger"),
    ("ScrollSmoother",  r"ScrollSmoother"),
    ("SplitText",       r"SplitText|Splitting|splitType|SplitType"),
    ("Lenis",           r"lenis(?:\.min)?\.js|new Lenis"),
    ("Locomotive",      r"locomotive"),
    ("Swiper",          r"swiper(?:\.min)?\.js|new Swiper"),
    ("Barba (page tx)", r"barba"),
    ("AOS",             r"aos\.js|data-aos"),
    ("anime.js",        r"anime(?:\.min)?\.js"),
    ("Motion One",      r"motion-?one|framer-motion|\bmotion\.(?:animate|scroll)"),
    ("ScrollReveal",    r"scrollreveal"),
    ("Lottie",          r"lottie"),
    ("Three.js / WebGL", r"three(?:\.min)?\.js|THREE\.|WebGLRenderer|createShader"),
    ("Rive",            r"rive-"),
    ("Webflow IX2",     r"data-w-id|webflow\.[a-f0-9]+\.js|ix2"),
]

# the specific effects he keeps asking for, detected by their tell-tale code
EFFECTS = [
    ("Custom cursor",        r"cursor\s*:\s*none|cursor-follow|\.cursor\b[^{]{0,40}\{[^}]*translate"),
    ("Magnetic hover",       r"magnet|magnetic"),
    ("Sticky / pinned",      r"position\s*:\s*sticky|pin\s*:\s*true|ScrollTrigger\.create"),
    ("Scroll-linked (scrub)", r"scrub\s*:\s*(?:true|[0-9.]+)"),
    ("Anchor / section nav", r"ScrollToPlugin|scrollIntoView|scrollTo\s*\(|IntersectionObserver"),
    ("Clip-path reveal",     r"clip-?path"),
    ("Glass / blur",         r"backdrop-filter|backdrop-blur"),
    ("Floating loop",        r"@keyframes\s+(?:float|bob|drift)|animation[^;]*\b(?:float|bob|drift)\b"),
    ("Marquee",              r"@keyframes\s+(?:marquee|scroll|ticker)|marquee"),
    ("Scroll snap",          r"scroll-snap-type"),
    ("Counter",              r"innerText\s*:|countUp|data-count"),
    ("Parallax",             r"parallax|translate3d\(0px?,\s*-?\d"),
    ("Mask / gradient text", r"-webkit-background-clip|mask-image"),
]

CSS_HINTS = [
    ("clip-path",       r"clip-path\s*:\s*[^;\"}]{3,70}"),
    ("backdrop-filter", r"backdrop-filter\s*:\s*[^;\"}]{3,60}"),
    ("transition",      r"transition\s*:\s*[^;\"}]{3,60}"),
    ("animation",       r"animation\s*:\s*[^;\"}]{3,60}"),
    ("scroll-snap",     r"scroll-snap-[a-z]+\s*:\s*[^;\"}]{2,30}"),
    ("position:sticky", r"position\s*:\s*sticky"),
    ("mix-blend-mode",  r"mix-blend-mode\s*:\s*[^;\"}]{3,24}"),
]

MOTION_CALLS = [
    r"new Lenis\s*\([^)]{0,200}\)",
    r"gsap\.(?:timeline|to|from|fromTo)\s*\([^;]{0,230}",
    r"scrollTrigger\s*:\s*\{[^}]{0,180}\}",
    r"clipPath\s*:\s*[\"'][^\"']{0,110}[\"']",
    r"@keyframes\s+[\w-]+\s*\{[^}]{0,150}",
    r"stagger\s*:\s*[0-9.]+",
    r"scrub\s*:\s*(?:true|[0-9.]+)",
    r"pin\s*:\s*true",
]


def fetch(url, binary=False):
    """urllib first; several hosts answer 403 to it, so fall back to curl."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=45) as r:
            data = r.read(MAX_ASSET_BYTES)
    except Exception:
        import subprocess
        out = subprocess.run(
            ["curl", "-sL", "--max-time", "45", "-A", UA, url],
            capture_output=True,
        )
        if out.returncode != 0 or not out.stdout:
            raise
        data = out.stdout[:MAX_ASSET_BYTES]
    return data if binary else data.decode("utf-8", errors="replace")


def section(title):
    print("\n" + title)
    print("-" * len(title))


def gather_assets(html, base, deep):
    """Return concatenated text of the page's own JS and CSS bundles."""
    if not deep:
        return ""
    refs = re.findall(r'<script[^>]+src="([^"]+)"', html)
    refs += re.findall(r'<link[^>]+href="([^"]+\.css[^"]*)"', html)
    host = urllib.parse.urlparse(base).netloc
    picked, blob = [], []
    for r in refs:
        full = urllib.parse.urljoin(base, r)
        p = urllib.parse.urlparse(full)
        if p.netloc and p.netloc != host:
            continue                      # same origin only
        if re.search(r"jquery|gtag|analytics|gtm|recaptcha|hotjar|clarity|polyfill",
                     full, re.I):
            continue
        if full in picked:
            continue
        picked.append(full)
        if len(picked) >= MAX_ASSETS:
            break
    for f in picked:
        try:
            blob.append(fetch(f))
        except Exception:
            pass
    if picked:
        print("  fetched %d bundle(s):" % len(blob))
        for f in picked[:len(blob)]:
            print("      " + f.split("/")[-1][:70])
    return "\n".join(blob)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    deep = "--deep" in sys.argv
    if not args:
        print(__doc__)
        return 1
    url = args[0]

    try:
        html = fetch(url)
    except Exception as e:
        print("could not fetch %s: %s" % (url, e))
        return 1

    print("inspected: %s  (%d KB of HTML)%s" %
          (url, len(html) // 1024, "  [deep]" if deep else ""))

    if deep:
        section("Bundles")
    assets = gather_assets(html, url, deep)
    corpus = html + "\n" + assets

    section("Animation stack")
    hits = [(n, len(re.findall(p, corpus, re.I))) for n, p in LIBS]
    hits = [h for h in hits if h[1]]
    if hits:
        for n, c in sorted(hits, key=lambda x: -x[1]):
            print("  %-20s %d" % (n, c))
    else:
        print("  none detected. Plain CSS, or the code is not reachable.")
        if not deep:
            print("  >> re-run with --deep to scan the site's own JS and CSS bundles")

    section("Effects present")
    any_fx = False
    for name, pat in EFFECTS:
        c = len(re.findall(pat, corpus, re.I))
        if c:
            any_fx = True
            print("  %-24s %d" % (name, c))
    if not any_fx:
        print("  nothing recognised")

    section("Motion calls with their numbers")
    seen, shown = set(), 0
    for pat in MOTION_CALLS:
        for m in re.finditer(pat, corpus, re.I):
            frag = re.sub(r"\s+", " ", m.group(0))[:210].strip()
            key = frag[:64]
            if key in seen:
                continue
            seen.add(key)
            print("  * " + frag)
            shown += 1
            if shown > 34:
                break
        if shown > 34:
            break
    if not shown:
        print("  none found in reachable code")

    section("CSS motion properties")
    for name, pat in CSS_HINTS:
        vals = re.findall(pat, corpus, re.I)
        if vals:
            uniq = sorted({re.sub(r"\s+", " ", v)[:74] for v in vals})
            print("  %s  (%d)" % (name, len(vals)))
            for v in uniq[:3]:
                print("      " + v)

    section("Next step")
    print("  Rebuild each effect with the vanilla recipes in INSPIRATION.md,")
    print("  then add this site to its table. Never ship their JavaScript.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
