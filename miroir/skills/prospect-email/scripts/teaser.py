#!/usr/bin/env python3
"""teaser.py - transforme une maquette HTML en UNE image de courriel.

Rend le haut de page en desktop et en mobile avec Chrome sans interface, puis
compose les deux dans un cadre ordinateur + telephone sur un fond tire de la
maquette elle-meme.

    python teaser.py --html index.html --out ../Prospect-teaser
        -> Prospect-teaser.png  (master 2x)
        -> Prospect-teaser.jpg  (piece jointe courriel, vise sous 500 Ko)

Aucune dependance hors Pillow.
"""
import argparse, os, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageStat

CHROMES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

IPHONE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
             "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")

# Injecte avant </head> pour la capture seulement. Sans ca, les elements en
# attente d'IntersectionObserver restent a opacite 0 et la photo sort vide.
FORCE_CSS = """<style id="teaser-capture">
*,*::before,*::after{transition-duration:0s!important;animation-duration:.001s!important;animation-delay:0s!important}
.rv,.reveal,[data-rv],[class*="rv-"],[class*="fade"],[class*="reveal"]{opacity:1!important;transform:none!important;visibility:visible!important;clip-path:none!important;filter:none!important}
html{scroll-behavior:auto!important}
</style>"""


def find_chrome():
    for p in CHROMES:
        if os.path.exists(p):
            return p
    raise SystemExit("Aucun Chrome ni Edge trouve. Modifier CHROMES dans teaser.py.")


def shoot(chrome, html_path, out_png, w, h, scale=2, mobile=False, budget=8000):
    cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--no-sandbox", "--disable-lcd-text",
           "--force-device-scale-factor=%d" % scale, "--window-size=%d,%d" % (w, h),
           "--virtual-time-budget=%d" % budget,
           "--screenshot=%s" % out_png, Path(html_path).absolute().as_uri()]
    if mobile:
        cmd.insert(2, "--user-agent=" + IPHONE_UA)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not os.path.exists(out_png):
        raise SystemExit("Capture ratee (%dx%d):\n%s" % (w, h, r.stderr[-800:]))
    im = Image.open(out_png).convert("RGB")
    sd = sum(ImageStat.Stat(im).stddev) / 3
    return im, sd


                                    # Chrome sans interface refuse un viewport sous ~477px:
                                    # --window-size=390 rend la page a 477 puis rogne l'image.
                                    # Une iframe de 390px donne le seul vrai viewport mobile.
CADRE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#fff;overflow:hidden}
iframe{border:0;display:block;width:%dpx;height:%dpx}
</style></head><body><iframe src="%s" scrolling="no"></iframe></body></html>"""


def cadre_mobile(src_path, w, h):
    src = Path(src_path)
    tmp = src.with_name("__teaser_cadre__.html")
    tmp.write_text(CADRE % (w, h, src.name), encoding="utf-8")
    return tmp


def prepared(html_path, force):
    """Copie temporaire a cote du fichier source pour garder assets/ relatif."""
    src = Path(html_path)
    if not force:
        return src, None
    txt = src.read_text(encoding="utf-8", errors="ignore")
    i = txt.lower().find("</head>")
    txt = txt[:i] + FORCE_CSS + txt[i:] if i > -1 else FORCE_CSS + txt
    tmp = src.with_name("__teaser_capture__.html")
    tmp.write_text(txt, encoding="utf-8")
    return tmp, tmp


def shadow(size, radius, blur, dy, alpha=110):
    w, h = size
    pad = blur * 3
    lay = Image.new("L", (w + pad * 2, h + pad * 2), 0)
    ImageDraw.Draw(lay).rounded_rectangle(
        [pad, pad, pad + w, pad + h], radius=radius, fill=alpha)
    return lay.filter(ImageFilter.GaussianBlur(blur)), pad, dy


def rounded(im, radius):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1],
                                        radius=radius, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), m)
    return out


def backdrop(sample, size):
    """Fond tire de la maquette: sa couleur moyenne, desaturee et poussee."""
    r, g, b = ImageStat.Stat(sample.resize((40, 25))).mean[:3]
    lum = .2126 * r + .7152 * g + .0722 * b
    if lum < 128:                       # maquette sombre -> fond clair
        mix, k = (238, 238, 236), .82
    else:                               # maquette claire -> fond sourd
        mix, k = (26, 28, 32), .70
    top = tuple(int(c * (1 - k) + m * k) for c, m in zip((r, g, b), mix))
    bot = tuple(max(0, min(255, int(c * .88))) for c in top)
    bg = Image.new("RGB", size, top)
    d = ImageDraw.Draw(bg)
    for y in range(size[1]):
        t = y / size[1]
        d.line([(0, y), (size[0], y)],
               fill=tuple(int(a + (b2 - a) * t) for a, b2 in zip(top, bot)))
    return bg, lum


def compose(desk, mob, out_png, url_text=""):
    CW, CH = 2560, 1600
    bg, lum = backdrop(desk, (CW, CH))
    dark_ui = lum >= 128          # maquette claire -> fond sombre -> fenetre sombre

    dw = 1900
    dh = round(dw * desk.size[1] / desk.size[0])
    bar = 62
    win = Image.new("RGB", (dw, dh + bar), (34, 36, 40) if dark_ui else (243, 243, 241))
    dd = ImageDraw.Draw(win)
    dot = (108, 112, 118) if dark_ui else (196, 198, 200)
    for cx in (34, 68, 102):
        dd.ellipse([cx - 9, bar // 2 - 9, cx + 9, bar // 2 + 9], fill=dot)
    pill_w = min(560, dw - 320)
    px = (dw - pill_w) // 2
    dd.rounded_rectangle([px, 14, px + pill_w, bar - 14],
                         radius=17, fill=(52, 55, 60) if dark_ui else (255, 255, 255))
    if url_text:
        try:
            dd.text((px + 26, bar // 2 - 11), url_text[:52],
                    fill=(168, 172, 178) if dark_ui else (122, 126, 132))
        except Exception:
            pass
    win.paste(desk.resize((dw, dh), Image.LANCZOS), (0, bar))
    win = rounded(win, 26)

    # telephone monte avant le placement: il decide du cadrage de l'ensemble
    pw = 460
    ph = round(pw * mob.size[1] / mob.size[0])
    bez = 16
    body = Image.new("RGB", (pw + bez * 2, ph + bez * 2), (22, 23, 25))
    body.paste(mob.resize((pw, ph), Image.LANCZOS), (bez, bez))
    pd = ImageDraw.Draw(body)
    nw = pw // 3
    pd.rounded_rectangle([(body.size[0] - nw) // 2, bez + 8,
                          (body.size[0] + nw) // 2, bez + 34], radius=13, fill=(30, 31, 34))
    body = rounded(body, 54)
    bw, bh = body.size

    # le telephone deborde a droite de la fenetre, 45% de sa largeur dedans
    inside = int(bw * .45)
    group_w = dw - inside + bw
    wx = (CW - group_w) // 2
    wh = win.size[1]
    wy = (CH - wh) // 2 - 24

    sh, pad, dy = shadow(win.size, 26, 46, 26, 120)
    bg.paste((0, 0, 0), (wx - pad, wy - pad + dy), sh)
    bg.paste(win, (wx, wy), win)

    fx = wx + dw - inside
    fy = min(CH - bh - 56, wy + wh - int(bh * .74))
    fy = max(fy, 40)
    sh2, pad2, dy2 = shadow(body.size, 54, 54, 30, 135)
    bg.paste((0, 0, 0), (fx - pad2, fy - pad2 + dy2), sh2)
    bg.paste(body, (fx, fy), body)

    bg.save(out_png, "PNG", optimize=True)
    return bg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--out", required=True, help="chemin sans extension")
    ap.add_argument("--url", default="", help="texte de la barre d'adresse")
    ap.add_argument("--desktop", default="1440x900")
    ap.add_argument("--mobile", default="390x844")
    ap.add_argument("--no-force-reveal", action="store_true")
    ap.add_argument("--jpg-width", type=int, default=1600)
    ap.add_argument("--max-kb", type=int, default=500)
    a = ap.parse_args()

    chrome = find_chrome()
    src, tmp = prepared(a.html, not a.no_force_reveal)
    tdir = tempfile.mkdtemp()
    cadre = None
    try:
        dw, dh = (int(x) for x in a.desktop.lower().split("x"))
        mw, mh = (int(x) for x in a.mobile.lower().split("x"))
        desk, sd_d = shoot(chrome, src, os.path.join(tdir, "d.png"), dw, dh)

        cadre = cadre_mobile(src, mw, mh)
        brut, sd_m = shoot(chrome, cadre, os.path.join(tdir, "m.png"),
                           max(mw + 220, 700), mh + 60, mobile=True)
        mob = brut.crop((0, 0, mw * 2, mh * 2))
    finally:
        for f in (tmp, cadre):
            if f and f.exists():
                f.unlink()

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    png = str(out.with_suffix(".png"))
    canvas = compose(desk, mob, png, a.url)

    jpg = str(out.with_suffix(".jpg"))
    q, kb = 90, 0
    small = canvas.resize((a.jpg_width, round(a.jpg_width * canvas.size[1] / canvas.size[0])),
                          Image.LANCZOS)
    while True:
        small.save(jpg, "JPEG", quality=q, optimize=True, progressive=True)
        kb = os.path.getsize(jpg) / 1024
        if kb <= a.max_kb or q <= 62:
            break
        q -= 6

    print("desktop  %dx%d  ecart-type %.1f" % (desk.size[0], desk.size[1], sd_d))
    print("mobile   %dx%d  ecart-type %.1f" % (mob.size[0], mob.size[1], sd_m))
    print("PNG      %s  %.0f Ko" % (png, os.path.getsize(png) / 1024))
    print("JPG      %s  %.0f Ko  qualite %d" % (jpg, kb, q))
    for nom, sd in (("desktop", sd_d), ("mobile", sd_m)):
        if sd < 12:
            print("ALERTE: la capture %s est presque unie (ecart-type %.1f). "
                  "La page n'a probablement rien rendu. Ouvrir le PNG avant d'envoyer." % (nom, sd))
    print("Regarder le JPG une fois avant d'envoyer. Rien ne remplace ce coup d'oeil.")


if __name__ == "__main__":
    main()
