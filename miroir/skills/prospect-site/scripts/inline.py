#!/usr/bin/env python3
"""Fold every local image reference in an HTML file into base64 data: URIs.

Produces a single self-contained file that works offline with no sibling folder.

    python inline.py --html index.html --assets assets-opt --out Prospect-demo.html
"""
import argparse
import base64
import os
import re
import sys

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
        ".mp4": "video/mp4", ".webm": "video/webm",
        ".woff2": "font/woff2", ".woff": "font/woff",
        ".ttf": "font/ttf", ".otf": "font/otf"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--assets", required=True,
                    help="folder holding the images (usually the optimized one)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefix", default="assets",
                    help="path prefix used inside the HTML (default: assets)")
    args = ap.parse_args()

    with open(args.html, encoding="utf-8") as f:
        html = f.read()

    # A linked LOCAL stylesheet becomes a real <style> block, not a data: URI.
    # fonts.css already carries its woff2 in base64, so this is the last hop
    # between "works beside its folder" and "works alone in an email".
    # Done BEFORE the image pass so any assets/ reference inside the CSS is
    # inlined too, instead of shipping as a dead link.
    def absorbe(m):
        chemin = os.path.join(args.assets, m.group(1))
        if not os.path.exists(chemin):
            print("ERROR: linked stylesheet missing: %s" % chemin)
            sys.exit(1)
        with open(chemin, encoding="utf-8") as fh:
            corps = fh.read()
        print("  inlined %-52s %6.0f KB (feuille de style)"
              % (m.group(1), os.path.getsize(chemin) / 1024))
        return "<style>\n%s\n</style>" % corps.strip()

    html, n_css = re.subn(
        r'<link[^>]*rel=["\']stylesheet["\'][^>]*href=["\']%s/([^"\']+\.css)["\'][^>]*>'
        % re.escape(args.prefix), absorbe, html)
    if not n_css:
        html, n_css = re.subn(
            r'<link[^>]*href=["\']%s/([^"\']+\.css)["\'][^>]*rel=["\']stylesheet["\'][^>]*>'
            % re.escape(args.prefix), absorbe, html)

    # Longest extension first so .jpeg never matches as .jpg and .woff2 never as .woff.
    exts = "|".join(sorted((e.lstrip(".") for e in MIME), key=len, reverse=True))
    # Fonts live in assets/fonts/, so the name may carry subdirectories.
    seg = r"[A-Za-z0-9._\-]+"
    pattern = re.compile(r"%s/((?:%s/)*%s\.(?:%s))(?![A-Za-z0-9])"
                         % (re.escape(args.prefix), seg, seg, exts))

    names = sorted(set(pattern.findall(html)))
    if not names:
        print("No %s/ references found - nothing to inline." % args.prefix)
        sys.exit(1)
    print("references found: %d" % len(names))

    missing = [n for n in names if not os.path.exists(os.path.join(args.assets, n))]
    if missing:
        print("ERROR: missing from %s:" % args.assets)
        for m in missing:
            print("   ", m)
        sys.exit(1)

    for n in names:
        path = os.path.join(args.assets, n)
        ext = os.path.splitext(n)[1].lower()
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        html = html.replace("%s/%s" % (args.prefix, n),
                            "data:%s;base64,%s" % (MIME[ext], b64))
        print("  inlined %-52s %6.0f KB" % (n, os.path.getsize(path) / 1024))

    # A preload hint carrying a megabyte-long data: URI is pure waste once inlined.
    html = re.sub(r'\n?<link rel="preload"[^>]*href="data:[^"]*"[^>]*>', "", html)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)

    print("\noutput: %s" % args.out)
    print("size:   %.2f MB" % (os.path.getsize(args.out) / 1024 / 1024))

    # Scan for the literal prefix, not just the extensions we know about: a ref to a
    # file type this script cannot inline must fail loudly, never report a false
    # all-clear. That is how three woff2 fonts once shipped un-inlined.
    needle = args.prefix + "/"
    leftover = []
    for lineno, line in enumerate(html.splitlines(), 1):
        start = 0
        while True:
            i = line.find(needle, start)
            if i < 0:
                break
            leftover.append((lineno, line[max(0, i - 40):i + 60].strip()))
            start = i + len(needle)

    if leftover:
        print("ERROR: %d leftover '%s' reference(s) in the output - NOT self-contained:"
              % (len(leftover), needle))
        for lineno, snippet in leftover:
            print("    line %d: ...%s..." % (lineno, snippet))
        sys.exit(1)
    print("leftover %s refs: none" % needle)


if __name__ == "__main__":
    main()
