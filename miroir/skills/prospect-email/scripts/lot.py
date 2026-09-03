#!/usr/bin/env python3
"""lot.py - la file de prospection, les plafonds et la liste de suppression.

    python lot.py init                     cree les fichiers du dossier Prospection
    python lot.py mode                     le mode d'envoi effectif, et pourquoi
    python lot.py quota                    ce qui reste aujourd'hui et cette semaine
    python lot.py suivants 3               les N prochaines fiches eligibles
    python lot.py verif <courriel>         OK, ou la raison du refus
    python lot.py marquer <id> <statut> [note]
    python lot.py envoye <id> <courriel> <langue> "<objet>" "<monde>" [image]
    python lot.py stop <courriel|domaine>
    python lot.py relances                 les fiches dont la relance J+3 est due

Les plafonds ci-dessous refletent ENVOI.md. Changer les deux ensemble.
"""
import csv, os, sys, datetime
from pathlib import Path

BASE = Path(r"C:\Users\Administrator\OneDrive\Bureau\Prospection")
FILE = BASE / "FILE-ATTENTE.tsv"
SENT = BASE / "ENVOYES.tsv"
STOP = BASE / "NE-PAS-CONTACTER.txt"
ENVOI_MD = Path(__file__).resolve().parent.parent / "ENVOI.md"

PAR_JOUR, PAR_SEMAINE, PAR_LOT = 6, 12, 3
HEURE_MIN, HEURE_MAX = 8, 20
RELANCE_JOURS = 3

COLS = ["id", "nom", "ville", "metier", "site", "courriel", "decideur",
        "telephone", "statut", "note"]
SENT_COLS = ["date", "heure", "id", "nom", "courriel", "langue", "objet",
             "monde", "image", "relance"]
BLOQUANTS = {"ENVOYE", "SAUTE", "IDENTITE", "RELANCE", "APPELER", "CLIENT"}


def lire(path, cols):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter="\t") if any(v for v in r.values())]


def ecrire(path, cols, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: (r.get(c) or "") for c in cols})


def ajouter(path, cols, row):
    neuf = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        if neuf:
            w.writeheader()
        w.writerow({c: (row.get(c) or "") for c in cols})


def config():
    conf = {}
    if ENVOI_MD.exists():
        for ln in ENVOI_MD.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            for k in ("MODE", "TELEPHONE", "ADRESSE POSTALE", "EXPEDITEUR", "COURRIEL"):
                if ln.upper().startswith(k + ":") and k not in conf:
                    conf[k] = ln.split(":", 1)[1].strip()
    return conf


def mode_effectif():
    c = config()
    m = (c.get("MODE") or "arret").lower()
    manque = [k for k in ("TELEPHONE", "ADRESSE POSTALE")
              if not c.get(k) or "A REMPLIR" in c.get(k, "").upper()]
    if m == "auto" and manque:
        return "brouillon", "coordonnees LCAP manquantes dans ENVOI.md: " + ", ".join(manque)
    h = datetime.datetime.now()
    if m == "auto" and (h.weekday() >= 5 or not (HEURE_MIN <= h.hour < HEURE_MAX)):
        return "brouillon", "hors fenetre d'envoi (lun-ven, %dh-%dh)" % (HEURE_MIN, HEURE_MAX)
    return m, "ENVOI.md"


def stops():
    if not STOP.exists():
        return set()
    return {l.strip().lower() for l in STOP.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")}


def bloque(courriel):
    e = (courriel or "").strip().lower()
    if not e or "@" not in e:
        return "adresse absente ou invalide"
    dom = e.split("@", 1)[1]
    s = stops()
    if e in s or dom in s:
        return "figure dans NE-PAS-CONTACTER.txt"
    for r in lire(SENT, SENT_COLS):
        if (r.get("courriel") or "").strip().lower() == e:
            return "deja contacte le " + (r.get("date") or "?")
    return None


def comptes():
    au, sem = 0, 0
    today = datetime.date.today()
    lundi = today - datetime.timedelta(days=today.weekday())
    for r in lire(SENT, SENT_COLS):
        try:
            d = datetime.date.fromisoformat(r["date"])
        except Exception:
            continue
        if d == today:
            au += 1
        if d >= lundi:
            sem += 1
    return au, sem


def cmd_init():
    BASE.mkdir(parents=True, exist_ok=True)
    if not FILE.exists():
        ecrire(FILE, COLS, [{"id": "ex1", "nom": "Exemple Clinique inc.", "ville": "Gatineau",
                             "metier": "esthetique", "site": "https://exemple.ca",
                             "courriel": "", "decideur": "", "telephone": "819-555-0100",
                             "statut": "", "note": "ligne d'exemple, la supprimer"}])
    if not SENT.exists():
        ecrire(SENT, SENT_COLS, [])
    if not STOP.exists():
        STOP.write_text("# une adresse ou un domaine par ligne\n", encoding="utf-8")
    print("dossier pret:", BASE)
    for p in (FILE, SENT, STOP):
        print("  ", p.name)


def cmd_suivants(n):
    au, sem = comptes()
    reste = min(n, PAR_LOT, max(0, PAR_JOUR - au), max(0, PAR_SEMAINE - sem))
    if reste <= 0:
        print("PLAFOND ATTEINT. %d aujourd'hui (max %d), %d cette semaine (max %d)."
              % (au, PAR_JOUR, sem, PAR_SEMAINE))
        return
    rows, pris = lire(FILE, COLS), []
    for r in rows:
        if len(pris) >= reste:
            break
        if (r.get("statut") or "").strip().upper() in BLOQUANTS:
            continue
        if r.get("courriel") and bloque(r["courriel"]):
            continue
        pris.append(r)
    if not pris:
        print("Aucune fiche eligible dans", FILE.name)
        return
    print("\t".join(COLS))
    for r in pris:
        print("\t".join((r.get(c) or "") for c in COLS))
    print("\n%d fiche(s). Reste aujourd'hui: %d. Cette semaine: %d."
          % (len(pris), PAR_JOUR - au - len(pris), PAR_SEMAINE - sem - len(pris)))


def cmd_marquer(pid, statut, note=""):
    rows = lire(FILE, COLS)
    for r in rows:
        if r.get("id") == pid:
            r["statut"] = statut.upper()
            if note:
                r["note"] = note
            ecrire(FILE, COLS, rows)
            print("%s -> %s" % (pid, statut.upper()))
            return
    sys.exit("id introuvable: " + pid)


def cmd_envoye(pid, courriel, langue, objet, monde, image=""):
    now = datetime.datetime.now()
    rel = (now.date() + datetime.timedelta(days=RELANCE_JOURS)).isoformat()
    ajouter(SENT, SENT_COLS, {"date": now.date().isoformat(),
                              "heure": now.strftime("%H:%M"), "id": pid, "nom": "",
                              "courriel": courriel, "langue": langue, "objet": objet,
                              "monde": monde, "image": image, "relance": rel})
    rows = lire(FILE, COLS)
    for r in rows:
        if r.get("id") == pid:
            r["statut"] = "ENVOYE"
            r["note"] = "envoye %s, relance %s" % (now.date().isoformat(), rel)
            if not r.get("courriel"):
                r["courriel"] = courriel
    ecrire(FILE, COLS, rows)
    au, sem = comptes()
    print("journalise. relance due le %s. %d/%d aujourd'hui, %d/%d cette semaine."
          % (rel, au, PAR_JOUR, sem, PAR_SEMAINE))


def cmd_relances():
    today = datetime.date.today()
    duses = [r for r in lire(SENT, SENT_COLS)
             if r.get("relance") and r["relance"] <= today.isoformat()]
    rows = {r.get("id"): r for r in lire(FILE, COLS)}
    if not duses:
        print("aucune relance due")
    for r in duses:
        st = (rows.get(r.get("id"), {}).get("statut") or "").upper()
        if st in ("RELANCE", "APPELER", "CLIENT", "SAUTE"):
            continue
        print("\t".join([r.get("relance", ""), r.get("id", ""), r.get("courriel", ""),
                         r.get("langue", ""), r.get("objet", "")]))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    c = sys.argv[1]
    if c == "init":
        cmd_init()
    elif c == "mode":
        m, why = mode_effectif()
        print("MODE EFFECTIF: %s   (%s)" % (m, why))
    elif c == "quota":
        au, sem = comptes()
        m, why = mode_effectif()
        print("mode %s (%s)" % (m, why))
        print("aujourd'hui %d/%d, cette semaine %d/%d, par lot %d"
              % (au, PAR_JOUR, sem, PAR_SEMAINE, PAR_LOT))
    elif c == "suivants":
        cmd_suivants(int(sys.argv[2]) if len(sys.argv) > 2 else PAR_LOT)
    elif c == "verif":
        r = bloque(sys.argv[2])
        print("REFUS: " + r if r else "OK")
    elif c == "marquer":
        cmd_marquer(*sys.argv[2:5])
    elif c == "envoye":
        cmd_envoye(*sys.argv[2:8])
    elif c == "stop":
        a = sys.argv[2].strip().lower()
        BASE.mkdir(parents=True, exist_ok=True)
        with STOP.open("a", encoding="utf-8") as f:
            f.write(a + "\n")
        print("ajoute a NE-PAS-CONTACTER.txt:", a)
    elif c == "relances":
        cmd_relances()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
