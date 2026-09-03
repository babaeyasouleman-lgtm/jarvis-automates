#!/usr/bin/env python3
"""Validate a single-file prospect demo before it is emailed to a client.

    python verify.py Prospect-demo.html

Exits non-zero if anything is wrong, so it can gate delivery.
"""
import base64
import os
import re
import sys

SIGS = {"jpeg": b"\xff\xd8\xff", "png": b"\x89PNG\r\n\x1a\n", "gif": b"GIF8"}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    # Une maquette montree a quelqu'un qu'il connait deja n'a pas besoin des
    # marques anti-copie. Le drapeau est EXPLICITE: le defaut reste strict, pour
    # qu'un build de prospect ne parte jamais sans filigrane par distraction.
    sans_marque = "--sans-marque" in sys.argv[1:]
    if not args:
        print("usage: verify.py <file.html> [--sans-marque]")
        sys.exit(2)
    path = args[0]
    if not os.path.exists(path):
        print("FAIL  file not found: %s" % path)
        sys.exit(1)

    html = open(path, encoding="utf-8").read()
    problems = []

    # 1. every embedded image must decode to a real image
    uris = re.findall(r"data:image/(png|jpeg|gif|svg\+xml);base64,([A-Za-z0-9+/=]+)", html)
    good = 0
    total_bytes = 0
    for kind, b64 in uris:
        try:
            raw = base64.b64decode(b64)
        except Exception as e:
            problems.append("undecodable %s data URI (%s)" % (kind, e))
            continue
        total_bytes += len(raw)
        sig = SIGS.get(kind)
        if sig is None or raw.startswith(sig):
            good += 1
        else:
            problems.append("%s data URI has a bad file signature" % kind)
    print("embedded images:   %d/%d valid  (%.0f KB decoded)"
          % (good, len(uris), total_bytes / 1024))
    if not uris:
        problems.append("no embedded images at all - did inlining run?")

    # 2. no local reference may survive, or it breaks once emailed
    leftover = re.findall(r"(?:src|href)=\"(?!data:|https?:|mailto:|tel:|#)([^\"]+)\"", html)
    leftover = [r for r in leftover if not r.startswith("//")]
    print("local refs left:   %s" % (leftover or "none"))
    if leftover:
        problems.append("unresolved local references: %s" % leftover)

    # 3. structure closed
    for tag in ("</body>", "</html>"):
        if tag not in html:
            problems.append("missing %s" % tag)

    # 4. no-JS fallback flag present
    has_flag = "classList.add('js')" in html or 'classList.add("js")' in html
    # mechanics.html standardise sur .rv, pas .reveal. Chercher les deux, sinon
    # ce controle sort faux sur tout build conforme au gabarit de plomberie.
    scoped = (".js .reveal" in html) or (".js .rv" in html)
    print("no-JS fallback:    flag=%s scoped-css=%s" % (has_flag, scoped))
    if not has_flag:
        problems.append("missing the js flag script - page may render blank without JS")

    # 5. counters must not ship reading zero
    zeros = re.findall(r'class="count"[^>]*data-count="(\d+)"[^>]*>\s*0\s*<', html)
    if zeros:
        problems.append("counter markup ships as 0 (targets %s) - put the real value in the HTML" % zeros)

    # 6. size sanity for email
    mb = os.path.getsize(path) / 1024 / 1024
    print("file size:         %.2f MB" % mb)
    if mb > 8:
        problems.append("%.1f MB is risky as an email attachment - optimize images harder" % mb)

    # 7. copy that reads as AI-written
    em = html.count("—")
    banned = re.findall(
        r"\b(seamless\w*|robust\w*|leverage\w*|elevat\w+|transformative|streamlin\w+|"
        r"unlock\w*|empower\w*|cutting-edge|harness\w*|delve\w*)\b", html, re.I)
    print("em dashes:         %d" % em)
    print("banned words:      %s" % (sorted(set(w.lower() for w in banned)) or "none"))
    if em:
        problems.append("%d em dash(es) U+2014 - zero is the rule" % em)
    if banned:
        problems.append("AI marketing vocabulary: %s" % sorted(set(w.lower() for w in banned)))

    # 8. i18n parity: every data-i18n key translated, no key unused.
    #    Match key:" anywhere, never anchored to line start, or keys sharing a line
    #    look falsely missing.
    used = set(re.findall(r'data-i18n="([^"]+)"', html))
    declared = set(re.findall(r'[\{,]\s*["\']?([A-Za-z0-9_.\-]+)["\']?\s*:\s*["\']', html))
    missing = sorted(k for k in used if k not in declared)
    print("i18n keys:         %d used" % len(used))
    if missing:
        problems.append("data-i18n keys with no translation: %s" % missing[:12])
    if used and len(used) > 90:
        problems.append("%d translatable strings - the cap for a mockup is 40 to 70" % len(used))

    # 9. No PHOTOGRAPH may appear twice: it is the clearest sign of an empty demo.
    #    Restricted to jpeg on purpose. A logo repeated in the header and the footer is
    #    normal and was flagged as a fault on Elite Beauty Lab, 2026-08-12.
    seen, dup = {}, []
    for kind, b64 in uris:
        if kind != "jpeg":
            continue
        h = hash(b64)
        if h in seen:
            dup.append(h)
        seen[h] = 1
    if dup:
        problems.append("%d photo(s) embedded twice - no photo may appear twice" % len(dup))

    # 10. structure counts, so a bulk edit that silently ate content is caught here
    counts = {t: len(re.findall(r"<%s\b" % t, html)) for t in ("section", "figure", "img")}
    print("structure:         %s" % counts)
    if counts["section"] < 4:
        problems.append("only %d <section> - a mockup carries 5 to 7" % counts["section"])

    # 11. fonts must not be fetched from the network, or the file is not offline-safe
    if re.search(r'<link[^>]+fonts\.googleapis|<link[^>]+fonts\.gstatic', html):
        problems.append("a Google Fonts <link> survives - the base64 @font-face already "
                        "covers it and the file must work offline")

    # 12. the S-WEB Agency ownership marks
    if "S-WEB" not in html and not sans_marque:
        problems.append("no S-WEB Agency mark - watermark, corner badge and footer line "
                        "are required on every build")

    print()
    if problems:
        print("FAIL (%d issue%s)" % (len(problems), "" if len(problems) == 1 else "s"))
        for p in problems:
            print("  - %s" % p)
        sys.exit(1)
    print("PASS - safe to email")


if __name__ == "__main__":
    main()
