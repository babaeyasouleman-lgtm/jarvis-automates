# -*- coding: utf-8 -*-
"""Monte un client a partir du gabarit et de sa fiche.

    python monter-client.py climpure              # construit les fichiers
    python monter-client.py climpure --pousser    # construit ET envoie a Vapi

Un client = une fiche JSON dans clients/. Le gabarit ne change jamais.
Si un client demande une modification du gabarit, c'est qu'il manque un
champ a la fiche: ajoute le champ, ne forke pas le gabarit.

Sortie, dans sorties/<id>/ :
    prompt.md              le prompt final, lisible, pour relecture humaine
    assistant.json         la config complete, pour creer un assistant
    patch-sans-voix.json   pour mettre a jour sans ecraser la voix
"""
import json, io, os, re, sys, urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

ACQUIESCEMENTS = [
    "ouais", "oui", "ok", "okay", "d'accord", "daccord", "parfait", "correct",
    "c'est bon", "cest bon", "exact", "je comprends", "je vois", "hum", "hmm",
    "mhm", "mm-hmm", "ah oui", "ah ok", "bien sur", "certain", "voila",
    "yeah", "yes", "sure", "right", "alright", "got it", "gotcha", "i see",
    "i understand", "uh-huh", "mmhmm", "okay sure", "yeah okay",
]


def lire_cles():
    cles, chemin = {}, os.path.join(RACINE, "cles.local.txt")
    if os.path.exists(chemin):
        for ligne in io.open(chemin, encoding="utf-8"):
            m = re.match(r"^\s*([A-Z_]+)\s*=\s*(.+?)\s*$", ligne)
            if m:
                cles[m.group(1)] = m.group(2)
    return cles


def charger_fiche(cid):
    chemin = os.path.join(ICI, "clients", cid + ".json")
    if not os.path.exists(chemin):
        dispo = sorted(f[:-5] for f in os.listdir(os.path.join(ICI, "clients"))
                       if f.endswith(".json"))
        raise SystemExit("Fiche introuvable: %s\nDisponibles: %s" % (chemin, ", ".join(dispo)))
    return json.load(io.open(chemin, encoding="utf-8"))


def rendre_prompt(fiche):
    brut = io.open(os.path.join(ICI, "prompt-gabarit.md"), encoding="utf-8").read()
    corps = brut.split("---\n", 1)[1].strip()

    manquants = []
    for cle in sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", corps))):
        if cle not in fiche:
            manquants.append(cle)
        else:
            corps = corps.replace("{{%s}}" % cle, str(fiche[cle]))
    if manquants:
        raise SystemExit("Champs absents de la fiche: " + ", ".join(manquants))

    restants = re.findall(r"\{\{[^}]+\}\}", corps)
    if restants:
        raise SystemExit("Marqueurs non remplaces: " + ", ".join(restants))
    return corps


def construire(fiche, prompt):
    v = fiche.get("vapi", {})
    return {
        "name": "%s, demo" % fiche["ENTREPRISE"],
        "firstMessage": fiche["SALUTATION"],
        "firstMessageMode": "assistant-speaks-first",
        "model": {
            "provider": "google",
            "model": "gemini-3.5-flash",
            "temperature": 0.4,
            "maxTokens": 150,
            "messages": [{"role": "system", "content": prompt}],
            "tools": [{"type": "endCall"}],
        },
        "transcriber": {
            "provider": "deepgram", "model": "nova-3",
            "language": "multi", "smartFormat": True,
        },
        "voice": v.get("voice", {
            "provider": "vapi", "voiceId": "Savannah",
            "version": "2", "language": "fr-CA", "speed": 1,
        }),
        "startSpeakingPlan": {
            "waitSeconds": 0.4,
            "smartEndpointingPlan": {"provider": "vapi"},
        },
        "stopSpeakingPlan": {
            "numWords": 1, "voiceSeconds": 0.2, "backoffSeconds": 0.8,
            "acknowledgementPhrases": ACQUIESCEMENTS,
        },
        "backgroundSound": "office",
        "backgroundSpeechDenoisingPlan": {"smartDenoisingPlan": {"enabled": True}},
        "voicemailDetection": {"provider": "vapi"},
        "artifactPlan": {
            "recordingEnabled": True, "recordingFormat": "mp3",
            "loggingEnabled": True, "transcriptPlan": {"enabled": True},
        },
        "maxDurationSeconds": 420,
        "endCallPhrases": ["bonne journee", "have a good day", "au revoir", "goodbye"],
        "analysisPlan": {
            "summaryPlan": {"enabled": True, "messages": [{
                "role": "system",
                "content": "Resume l'appel en trois lignes maximum: ce que la "
                           "personne veut, sa ville, et ses coordonnees.",
            }]},
            "structuredDataPlan": {"enabled": True, "schema": {
                "type": "object",
                "properties": {
                    "langue": {"type": "string", "enum": ["fr", "en"]},
                    "nom": {"type": "string"},
                    "telephone": {"type": "string"},
                    "ville": {"type": "string"},
                    "service": {"type": "string"},
                    "urgence": {"type": "boolean"},
                    "hors_heures": {"type": "boolean"},
                    # Les memes categories que la colonne "pourquoi les non
                    # retenus" du tableau de bord, pour que l'agent produise
                    # vraiment la donnee que le tableau affiche.
                    "motif_non_retenu": {"type": "string", "enum": [
                        "aucun", "hors_zone", "locataire", "hors_service",
                        "sollicitation", "plainte"]},
                },
            }},
        },
    }


def pousser(assistant, fiche, cles):
    if "VAPI_API_KEY" not in cles:
        raise SystemExit("VAPI_API_KEY absente de cles.local.txt")
    aid = fiche.get("vapi", {}).get("assistantId")
    corps = {k: v for k, v in assistant.items() if k not in ("voice", "backgroundSound")} \
        if aid else assistant
    url = "https://api.vapi.ai/assistant" + ("/" + aid if aid else "")
    req = urllib.request.Request(
        url, method="PATCH" if aid else "POST",
        data=json.dumps(corps, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + cles["VAPI_API_KEY"],
                 "Content-Type": "application/json; charset=utf-8",
                 # Sans User-Agent explicite, urllib envoie "Python-urllib"
                 # et le pare-feu devant l'API de Vapi renvoie 403.
                 "User-Agent": "s-web-monter-client/1.0",
                 "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            rep = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit("Vapi a refuse (%s): %s" % (e.code, e.read().decode("utf-8", "replace")[:500]))
    if aid:
        print("  assistant %s mis a jour, voix laissee intacte" % rep["id"])
    else:
        print("  assistant CREE, id = %s" % rep["id"])
        print("  colle cet id dans la fiche, champ vapi.assistantId")
    return rep


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    cid = sys.argv[1]
    fiche = charger_fiche(cid)
    prompt = rendre_prompt(fiche)
    assistant = construire(fiche, prompt)

    dossier = os.path.join(ICI, "sorties", fiche["id"])
    os.makedirs(dossier, exist_ok=True)
    io.open(os.path.join(dossier, "prompt.md"), "w", encoding="utf-8").write(prompt)
    io.open(os.path.join(dossier, "assistant.json"), "w", encoding="utf-8").write(
        json.dumps(assistant, ensure_ascii=False, indent=2))
    sans = {k: v for k, v in assistant.items() if k not in ("voice", "backgroundSound")}
    io.open(os.path.join(dossier, "patch-sans-voix.json"), "w", encoding="utf-8").write(
        json.dumps(sans, ensure_ascii=False, indent=2))

    print("%s : prompt de %d caracteres, %d champs injectes" %
          (fiche["ENTREPRISE"], len(prompt),
           len([k for k in fiche if k.isupper()])))
    print("  -> " + dossier)

    if "--pousser" in sys.argv:
        pousser(assistant, fiche, lire_cles())


if __name__ == "__main__":
    main()
