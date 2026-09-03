# -*- coding: utf-8 -*-
"""Convertit les paquets design-systems d'OpenDesign en mondes pour prospect-site.
Sortie: un .css par monde, plus MONDES.tsv, l'index qui se filtre par awk."""
import json, os, re, shutil, colorsys, math, sys

SRC, DST = sys.argv[1], sys.argv[2]

MARQUES = {
 "airbnb","airtable","ant","apple","arc","binance","bmw","bmw-m","bugatti","cal","canva",
 "cisco","claude","clickhouse","cloudflare-kumo","cohere","coinbase","composio","cursor",
 "discord","duolingo","elevenlabs","expo","ferrari","figma","framer","github","hashicorp",
 "huggingface","ibm","intercom","kraken","lamborghini","levels","linear-app","lingo","loom",
 "lovable","mastercard","material","meta","minimax","mintlify","miro","mistral-ai","mongodb",
 "nike","notion","nvidia","ollama","openai","opencode-ai","pacman","perplexity","pinterest",
 "playstation","posthog","raycast","renault","replicate","resend","revolut","runwayml","sanity",
 "sentry","shadcn","shopify","slack","spacex","spotify","starbucks","stripe","supabase",
 "superhuman","tesla","tetris","theverge","together-ai","uber","vercel","vodafone","voltagent",
 "warp","webex","webflow","wechat","wired","wise","x-ai","xiaohongshu","zapier",
}

# ---------- couleur ----------
def _clamp(x):
    return max(0.0, min(1.0, x))

def oklch_hex(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774*a + 0.2158037573*b) ** 3
    m_ = (L - 0.1055613458*a - 0.0638541728*b) ** 3
    s_ = (L - 0.0894841775*a - 1.2914855480*b) ** 3
    lin = ( 4.0767416621*l_ - 3.3077115913*m_ + 0.2309699292*s_,
           -1.2684380046*l_ + 2.6097574011*m_ - 0.3413193965*s_,
           -0.0041960863*l_ - 0.7034186147*m_ + 1.7076147010*s_)
    out = []
    for v in lin:
        v = _clamp(v)
        v = 12.92*v if v <= 0.0031308 else 1.055*(v**(1/2.4)) - 0.055
        out.append(round(_clamp(v)*255))
    return "#%02x%02x%02x" % tuple(out)

def hexa(v):
    """Rend un #rrggbb depuis hex, rgb(a) ou oklch. Vide si indechiffrable."""
    v = (v or "").split("/*")[0].strip()
    m = re.search(r'#([0-9A-Fa-f]{6})\b', v)
    if m:
        return "#" + m.group(1).lower()
    m = re.search(r'#([0-9A-Fa-f]{3})\b', v)
    if m:
        return "#" + "".join(c*2 for c in m.group(1).lower())
    m = re.search(r'rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)', v)
    if m:
        return "#%02x%02x%02x" % tuple(min(255, round(float(x))) for x in m.groups())
    m = re.search(r'oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)', v)
    if m:
        raw = float(m.group(1))
        L = raw / 100.0 if (m.group(2) or raw > 1.5) else raw
        return oklch_hex(L, float(m.group(3)), float(m.group(4)))
    return ""

def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

def lum(h):
    def c(x):
        return x/12.92 if x <= 0.03928 else ((x+0.055)/1.055)**2.4
    r, g, b = rgb(h)
    return 0.2126*c(r) + 0.7152*c(g) + 0.0722*c(b)

def temperature(h):
    if not h:
        return "?"
    r, g, b = rgb(h)
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    if ss < 0.12 or ll > 0.96 or ll < 0.04:
        return "neutre"
    d = hh * 360
    return ("rouge" if d < 16 or d >= 340 else "chaud" if d < 48 else "or" if d < 70
            else "vert" if d < 160 else "cyan" if d < 200 else "froid" if d < 260
            else "violet" if d < 300 else "rose")

# ---------- typo ----------
GROUPES = [
 ("mono", ("mono","menlo","courier","consolas","monaco")),
 ("serif", ("georgia","times","garamond","gelasio","lora","merriweather","spectral","playfair",
            "source serif","freight","tiempos","canela","recoleta","instrument serif","newsreader",
            "fraunces","dm serif","libre baskerville","crimson","eb garamond","argent")),
 ("condense", ("oswald","bebas","anton","condensed","narrow","teko","barlow semi")),
 ("geometrique", ("futura","poppins","montserrat","avenir","circular","gilroy","sofia","outfit",
                  "satoshi","cereal","gotham","nunito","quicksand","urbanist")),
 ("grotesque", ("inter","helvetica","arial","system-ui","-apple-system","roboto","plex sans",
                "suisse","neue haas","untitled","graphik","aeonik","haas","sf pro","segoe")),
]

def classe_typo(fam):
    f = (fam or "").lower()
    for nom, cles in GROUPES:
        if any(k in f for k in cles):
            return nom
    if "serif" in f and "sans-serif" not in f:
        return "serif"
    return "sans"

def premiere(fam):
    return (fam or "").split(",")[0].strip().strip('"').strip("'")

def px(v):
    v = (v or "").split("/*")[0]
    m = re.search(r'(-?[\d.]+)px', v)
    if m:
        return m.group(1)
    return "0" if re.match(r'^\s*0\s*$', v) else ""

# ---------- lecture ----------
def racine(css):
    """Premier bloc :root seulement, commentaires retires.
    Sinon un bloc [data-theme=dark] ecrase les valeurs claires."""
    sansc = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    m = re.search(r':root\s*\{(.*?)\}', sansc, re.S)
    d = {}
    for k, v in re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', m.group(1) if m else sansc):
        d.setdefault(k, v.strip())
    return d

def prem(t, *cles):
    for c in cles:
        if t.get(c):
            return t[c]
    return ""

BOX = "─━│═╔╗╚╝█—–"

def allure(css, manifest_desc):
    """Une phrase qui decrit l'allure du monde, tiree de l'entete du fichier."""
    entete = css.split("*/")[0]
    lignes = []
    for l in entete.splitlines():
        l = l.lstrip().lstrip("/").lstrip("*").strip().strip(BOX).strip()
        if not l or l.startswith("design-systems/"):
            continue
        if len(re.findall(r'[A-Za-z]', l)) < 12:
            continue
        lignes.append(l)
    # "Structured token bindings for X" est un titre, la ligne suivante decrit vraiment
    for i, l in enumerate(lignes):
        if l.lower().startswith("structured token bindings"):
            suite = [x for x in lignes[i+1:i+3]
                     if not x.lower().startswith(("brand identity", "official sources", "source:"))]
            if suite:
                return " ".join(suite)
            continue
        return l
    return manifest_desc or ""

lignes = []
os.makedirs(DST, exist_ok=True)
for slug in sorted(os.listdir(SRC)):
    d = os.path.join(SRC, slug)
    tk, mf = os.path.join(d, "tokens.css"), os.path.join(d, "manifest.json")
    if not os.path.isfile(tk):
        continue
    css = open(tk, encoding="utf-8").read()
    shutil.copyfile(tk, os.path.join(DST, slug + ".css"))

    t = racine(css)
    nom, cat, mdesc = slug, "", ""
    if os.path.isfile(mf):
        try:
            j = json.load(open(mf, encoding="utf-8"))
            nom = j.get("name") or slug
            cat = j.get("category") or ""
            mdesc = j.get("description") or ""
        except Exception:
            pass

    bg  = hexa(prem(t, "--bg", "--background", "--surface", "--canvas"))
    acc = hexa(prem(t, "--accent", "--primary", "--accent-1", "--brand"))
    fg  = hexa(prem(t, "--fg", "--text", "--foreground", "--ink"))
    lignes.append([
        slug, nom, cat, "MARQUE" if slug in MARQUES else "libre",
        "sombre" if (bg and lum(bg) < 0.35) else "clair",
        temperature(acc), acc, bg, fg,
        classe_typo(t.get("--font-display", "")), premiere(t.get("--font-display", "")),
        classe_typo(t.get("--font-body", "")),    premiere(t.get("--font-body", "")),
        px(t.get("--text-3xl", "")), px(t.get("--text-base", "")),
        px(t.get("--radius-md", "")), px(t.get("--section-y-desktop", "")),
        px(t.get("--container-max", "")),
        re.sub(r'\s+', ' ', allure(css, mdesc))[:160],
    ])

ENTETE = ["slug", "nom", "categorie", "usage", "fond", "temperature", "accent", "bg", "fg",
          "classe_titre", "police_titre", "classe_corps", "police_corps",
          "titre_px", "corps_px", "rayon_px", "section_y_px", "conteneur_px", "allure"]
with open(os.path.join(DST, "MONDES.tsv"), "w", encoding="utf-8", newline="") as f:
    f.write("\t".join(ENTETE) + "\n")
    for l in lignes:
        f.write("\t".join(str(x) for x in l) + "\n")
print("mondes ecrits:", len(lignes))
