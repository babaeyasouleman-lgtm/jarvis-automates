# -*- coding: utf-8 -*-
"""Fait passer les scenarios a l'assistant reel, par ecrit, et verifie
automatiquement les regles de forme.

    python tester-agent.py

Deux voies, choisies automatiquement:

  GEMINI_API_KEY dans cles.local.txt -> interroge Gemini directement avec
      le prompt genere. Gratuit sur le palier gratuit de ai.google.dev.
      C'est la voie a privilegier.

  VAPI_API_KEY seule -> passe par l'endpoint /chat de Vapi. Attention:
      Vapi exige une carte au dossier pour le canal texte, meme avec des
      credits. Sans carte, la voie renvoie une erreur 402.

Dans les deux cas c'est le meme prompt et le meme modele qu'au telephone.
Seule la voix est absente, et c'est exactement ce qu'on veut pour mesurer
si le modele respecte ses consignes de forme.
"""
import json, io, os, re, sys, urllib.request, urllib.error

ICI = os.path.dirname(os.path.abspath(__file__))
ASSISTANT = "c3022c52-d9a1-4696-9786-e2d6cba25b53"

# ---------------------------------------------------------------- scenarios
# Chaque scenario est une suite de repliques du client. On verifie la
# reponse de l'agent apres chacune.
SCENARIOS = [
    ("Appel typique en francais", [
        "Bonjour, j'aimerais faire nettoyer ma thermopompe murale.",
        "Marie Tremblay.",
        "Quatre un neuf, cinq cinq cinq, zero deux trois quatre.",
        "Je suis a Gatineau, secteur Hull.",
    ]),
    ("Appel typique en anglais", [
        "Hi, I'd like to get my dryer vent cleaned.",
        "Michael Brown.",
        "Six one three, five five five, zero two three four.",
        "I'm in Orleans.",
    ]),
    ("Ouverture vague", [
        "Bonjour, j'appelle pour un nettoyage.",
        "Ben, pour la maison au complet.",
    ]),
    ("Prix demande trois fois", [
        "Bonjour, ca coute combien pour nettoyer mes conduits?",
        "Oui mais approximativement, c'est quoi le prix?",
        "Ecoutez, donnez-moi juste un ordre de grandeur, un chiffre.",
    ]),
    ("Es-tu un robot", [
        "Bonjour, j'aimerais faire nettoyer mes conduits.",
        "Attends une minute, es-tu un robot?",
    ]),
    ("HORS SERVICE, nettoyage de cuisine", [
        "Bonjour, est-ce que vous faites le nettoyage de cuisine?",
        "Vous etes surs? C'est juste un gros menage.",
    ]),
    ("HORS SERVICE, reparation d'appareil", [
        "Allo, ma thermopompe fonctionne plus du tout, pouvez-vous la reparer?",
    ]),
    ("HORS SERVICE, tapis", [
        "Bonjour, je voudrais faire nettoyer mes tapis et mon divan.",
    ]),
    ("Sollicitation", [
        "Bonjour, je vous appelle de la part d'une agence de referencement web, on aimerait vous proposer nos services.",
    ]),
    ("Locataire", [
        "Bonjour, j'aimerais faire nettoyer les conduits de mon appartement.",
        "Je suis locataire, c'est mon proprietaire qui possede l'immeuble.",
    ]),
    ("Plainte sur un travail fait", [
        "Bonjour, vous etes venus le mois passe et ca sent encore la poussiere partout. Je suis pas content du tout.",
    ]),
    ("Appel hors heures", [
        "Bonjour, je m'excuse d'appeler a onze heures du soir.",
        "Ma secheuse seche plus rien pis ca sent le chaud.",
    ]),
    ("Piege de langue, Ottawa", [
        "Bonjour, j'aimerais faire nettoyer mes conduits d'air.",
        "Je suis a Ottawa, dans le secteur de Vanier.",
    ]),
    ("Heures d'ouverture", [
        "Bonjour, vous etes ouverts jusqu'a quelle heure?",
    ]),
    ("Hors zone", [
        "Bonjour, est-ce que vous vous deplacez jusqu'a Thurso?",
    ]),
]


def lire_cles():
    cles = {}
    for ligne in io.open(os.path.join(ICI, "cles.local.txt"), encoding="utf-8"):
        m = re.match(r"^\s*([A-Z_]+)\s*=\s*(.+?)\s*$", ligne)
        if m:
            cles[m.group(1)] = m.group(2)
    return cles


def prompt_local():
    """Le prompt genere pour ClimPure, pour la voie Gemini directe."""
    f = os.path.join(ICI, "gabarit", "sorties", "climpure", "prompt.md")
    if not os.path.exists(f):
        raise SystemExit("Prompt introuvable. Lance: python gabarit/monter-client.py climpure")
    return io.open(f, encoding="utf-8").read()


def parler_gemini(cle, historique, modele="gemini-3.5-flash"):
    """Voie de secours: on interroge Gemini directement avec le meme prompt
    et le meme modele que Vapi. La voix est absente, le comportement du
    modele est le meme, et c'est lui qu'on teste."""
    corps = {
        "systemInstruction": {"parts": [{"text": prompt_local()}]},
        "contents": historique,
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 150},
    }
    url = ("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s"
           % (modele, cle))
    req = urllib.request.Request(
        url, method="POST", data=json.dumps(corps, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8",
                 "User-Agent": "s-web-tests/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            rep = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit("Gemini a refuse (%s): %s"
                         % (e.code, e.read().decode("utf-8", "replace")[:400]))
    try:
        return rep["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        return ""


def parler(cle, texte, chat_precedent=None):
    corps = {"assistantId": ASSISTANT, "input": texte}
    if chat_precedent:
        corps["previousChatId"] = chat_precedent
    req = urllib.request.Request(
        "https://api.vapi.ai/chat", method="POST",
        data=json.dumps(corps, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + cle,
                 "Content-Type": "application/json; charset=utf-8",
                 "User-Agent": "s-web-tests/1.0", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            rep = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit("Vapi a refuse (%s): %s" % (e.code, e.read().decode("utf-8", "replace")[:400]))
    sorties = [m.get("content", "") for m in rep.get("output", [])
               if m.get("role") == "assistant" and m.get("content")]
    return " ".join(sorties).strip(), rep.get("id")


# ---------------------------------------------------------------- controles
def phrases(t):
    t = re.sub(r"\.\.\.", "…", t)
    return [p for p in re.split(r"(?<=[.!?…])\s+", t.strip()) if p.strip()]


CHIFFRES = re.compile(r"\d")
PRIX = re.compile(r"\d+\s*(\$|dollars)|(\$|dollars)\s*\d+", re.I)
ENUM = re.compile(r"(,[^,]+){3,},")  # quatre elements ou plus separes par des virgules


def controler(rep):
    """Retourne la liste des regles violees par une reponse."""
    fautes = []
    ph = phrases(rep)
    if len(ph) > 2:
        fautes.append("plus de deux phrases (%d)" % len(ph))
    if rep.count("?") > 1:
        fautes.append("plus d'une question (%d)" % rep.count("?"))
    if CHIFFRES.search(rep):
        fautes.append("chiffre en chiffres: " + ",".join(sorted(set(CHIFFRES.findall(rep)))))
    if PRIX.search(rep):
        fautes.append("montant en dollars")
    if ENUM.search(rep):
        fautes.append("enumeration probable")
    return fautes


REFUS = re.compile(
    r"on ne (le |la )?fait pas|nous ne faisons pas|pas un service|"
    r"c'est pas ce qu'on fait|on (s'occupe|fait) (pas|seulement)|"
    r"we don't|not something we do|nous autres c'est", re.I)


def main():
    cles = lire_cles()
    voie = None
    if "GEMINI_API_KEY" in cles:
        voie = "gemini"
    elif "VAPI_API_KEY" in cles:
        voie = "vapi"
    else:
        raise SystemExit("Il faut GEMINI_API_KEY ou VAPI_API_KEY dans cles.local.txt")
    print("Voie: %s\n" % voie)
    total_fautes = 0
    lignes = []
    print("Passe de tests sur l'assistant %s\n" % ASSISTANT)

    for nom, tours in SCENARIOS:
        print("=" * 74)
        print(nom)
        print("=" * 74)
        precedent, fautes_scenario = None, 0
        historique, transcript = [], []
        for tour in tours:
            if voie == "gemini":
                historique.append({"role": "user", "parts": [{"text": tour}]})
                rep = parler_gemini(cles["GEMINI_API_KEY"], historique)
                historique.append({"role": "model", "parts": [{"text": rep}]})
            else:
                rep, precedent = parler(cles["VAPI_API_KEY"], tour, precedent)
            fautes = controler(rep)
            fautes_scenario += len(fautes)
            print("  CLIENT : %s" % tour)
            print("  AGENT  : %s" % rep)
            if fautes:
                print("  FAUTE  : " + " | ".join(fautes))
            print()
            transcript.append({"client": tour, "agent": rep, "fautes": fautes})

        # controle propre aux scenarios hors service
        if nom.startswith("HORS SERVICE"):
            derniere = transcript[-1]["agent"]
            if not REFUS.search(derniere):
                print("  ECHEC  : l'agent n'a pas refuse clairement\n")
                fautes_scenario += 1
        if nom == "Sollicitation":
            if "?" in transcript[-1]["agent"]:
                print("  ECHEC  : il relance un demarcheur au lieu de conclure\n")
                fautes_scenario += 1

        total_fautes += fautes_scenario
        lignes.append((nom, fautes_scenario, transcript))

    print("\n" + "=" * 74)
    print("RESUME")
    print("=" * 74)
    for nom, n, _ in lignes:
        print("  %-42s %s" % (nom, "OK" if n == 0 else "%d faute(s)" % n))
    print("\n  total: %d faute(s) sur %d scenarios" % (total_fautes, len(lignes)))

    io.open(os.path.join(ICI, "resultats-tests.json"), "w", encoding="utf-8").write(
        json.dumps([{"scenario": n, "fautes": f, "tours": tr} for n, f, tr in lignes],
                   ensure_ascii=False, indent=2))
    print("  detail: resultats-tests.json")


if __name__ == "__main__":
    main()
