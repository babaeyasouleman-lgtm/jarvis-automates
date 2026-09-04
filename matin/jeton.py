# -*- coding: utf-8 -*-
r"""
Renouvellement du jeton Google. Outil a la main, jamais lance par un automate.

Il refait le consentement OAuth une fois, avec la liste de scopes voulue, et
ecrit le nouveau refresh_token dans google.local.json. L'ancien est sauvegarde
a cote, sous google.local.json.avant-<horodatage>, couvert par la meme
exclusion git.

Pourquoi il existe : ajouter un scope dans la console Google ne suffit pas.
Un refresh_token ne porte que les scopes accordes le jour ou il a ete cree.
Pour en gagner un, il faut redemander le consentement, en redemandant aussi
tous les anciens, sinon on les perd.

Usage, depuis n'importe ou :
    python C:\Obsidian\matin\jeton.py
    python C:\Obsidian\matin\jeton.py calendar.events gmail.readonly

Sans argument, il reprend les scopes deja portes par le jeton actuel et y
ajoute gmail.readonly. C'est le cas de la phase 4.

Etat du projet openwa-agent, numero 710944925401, verifie le 3 septembre
2026, pour ne pas le rechercher :
  - Client OAuth de type Application de bureau. Google accepte les adresses
    de bouclage, il n'y a aucune URI de redirection a declarer.
  - Application En production, type Externe. Les jetons n'expirent pas au
    bout de sept jours.
  - Aucune portee declaree sur l'ecran de consentement, et pourtant
    calendar.events fonctionne. Dans ce projet, une portee n'a pas besoin
    d'etre declaree pour etre accordee.
  - La seule chose a faire avant de lancer ce script pour Gmail : activer
    l'API Gmail dans le projet. Aucun consentement ne contourne ca.
    console.cloud.google.com/apis/library/gmail.googleapis.com?project=710944925401
  - Si Google refuse malgre tout la portee, invalid_scope ou access_denied,
    c'est la seulement qu'il faudra la declarer sur l'ecran de consentement.
"""

import http.server
import json
import io
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime

PORT = 8765
REDIRECTION = "http://localhost:%d/" % PORT
AUTORISE = "https://accounts.google.com/o/oauth2/v2/auth"
JETON = "https://oauth2.googleapis.com/token"
BASE = "https://www.googleapis.com/auth/"

recu = {}


class Poignee(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        recu.update({k: v[0] for k, v in q.items()})
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        ok = "code" in recu
        msg = "C'est fait. Reviens dans le terminal." if ok else "Refus ou erreur. Reviens dans le terminal."
        self.wfile.write(("<html><body style='font-family:sans-serif;padding:3rem'>"
                          "<h2>%s</h2></body></html>" % msg).encode("utf-8"))

    def log_message(self, *a):
        pass


def scopes_actuels(c):
    """Demande a Google ce que le jeton actuel porte. Vide si on n'y arrive pas."""
    try:
        corps = urllib.parse.urlencode({
            "client_id": c["client_id"], "client_secret": c["client_secret"],
            "refresh_token": c["refresh_token"], "grant_type": "refresh_token"}).encode()
        r = json.loads(urllib.request.urlopen(
            urllib.request.Request(JETON, data=corps), timeout=20).read())
        return [s for s in r.get("scope", "").split() if s]
    except Exception:
        return []


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    chemin = os.path.join(base, "google.local.json")
    if not os.path.exists(chemin):
        print("ECHEC : google.local.json introuvable dans", base)
        return 1

    with io.open(chemin, encoding="utf-8") as f:
        c = json.load(f)
    for k in ("client_id", "client_secret"):
        if not c.get(k):
            print("ECHEC : champ", k, "vide dans google.local.json")
            return 1

    if len(sys.argv) > 1:
        scopes = [s if s.startswith("http") else BASE + s for s in sys.argv[1:]]
    else:
        anciens = scopes_actuels(c)
        if anciens:
            print("Scopes portes aujourd'hui :")
            for s in anciens:
                print("   ", s)
        else:
            anciens = [BASE + "calendar.events"]
            print("Scopes actuels illisibles, on repart de calendar.events.")
        scopes = list(dict.fromkeys(anciens + [BASE + "gmail.readonly"]))

    print()
    print("Scopes demandes :")
    for s in scopes:
        print("   ", s)
    print()
    print("Si ton client OAuth est de type Application Web, cette URI doit")
    print("figurer dans ses URI de redirection autorisees :")
    print("   ", REDIRECTION)
    print()
    # isatty() ment quand le script est lance depuis un shell non interactif,
    # sous PowerShell notamment. On attrape l'EOF plutot que de s'y fier.
    try:
        input("Appuie sur Entree pour ouvrir le navigateur, ou Ctrl+C pour arreter.")
    except EOFError:
        print("(entree non interactive, on ouvre le navigateur directement)")

    params = {
        "client_id": c["client_id"],
        "redirect_uri": REDIRECTION,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
    }
    url = AUTORISE + "?" + urllib.parse.urlencode(params)

    serveur = http.server.HTTPServer(("127.0.0.1", PORT), Poignee)
    threading.Thread(target=serveur.handle_request, daemon=True).start()

    print("Ouverture du navigateur. Choisis ton compte principal et accepte.")
    print("Si rien ne s'ouvre, colle cette adresse toi-meme :")
    print(url)
    webbrowser.open(url)

    for _ in range(300):
        if recu:
            break
        threading.Event().wait(1)
    serveur.server_close()

    if "code" not in recu:
        print("ECHEC : aucun code recu.", recu.get("error", "delai depasse, 5 minutes"))
        return 1

    try:
        corps = urllib.parse.urlencode({
            "code": recu["code"],
            "client_id": c["client_id"],
            "client_secret": c["client_secret"],
            "redirect_uri": REDIRECTION,
            "grant_type": "authorization_code"}).encode()
        r = json.loads(urllib.request.urlopen(
            urllib.request.Request(JETON, data=corps), timeout=20).read())
    except urllib.error.HTTPError as e:
        print("ECHEC de l'echange, HTTP", e.code)
        print(e.read().decode("utf-8", "replace")[:400])
        return 1

    neuf = r.get("refresh_token")
    if not neuf:
        print("ECHEC : Google n'a pas renvoye de refresh_token.")
        print("C'est le cas quand le consentement n'est pas redemande. Relance.")
        return 1

    horodatage = datetime.now().strftime("%Y-%m-%d-%H%M")
    sauvegarde = chemin + ".avant-" + horodatage
    with io.open(sauvegarde, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(c, indent=2, ensure_ascii=False))

    c["refresh_token"] = neuf
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(c, indent=2, ensure_ascii=False) + "\n")

    print()
    print("Fait. Nouveau refresh_token ecrit dans google.local.json.")
    print("Ancien garde dans", os.path.basename(sauvegarde))
    print("Scopes accordes :", r.get("scope", "inconnu"))
    print()
    print("Verifie tout de suite avec :")
    print("   python " + os.path.join(base, "agenda.py") + " " + base)
    return 0


if __name__ == "__main__":
    sys.exit(main())
