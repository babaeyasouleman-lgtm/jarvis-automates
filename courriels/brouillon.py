# -*- coding: utf-8 -*-
"""
Depot d'un brouillon dans Gmail. Phase 4 du Plan Jarvis.

Le seul script de cet automate qui ecrit dans Gmail, et il ne sait faire
qu'une chose : creer un brouillon. Il n'appelle jamais users.messages.send
ni users.drafts.send. Chercher "send" dans ce fichier ne donne rien d'autre
que cette phrase. Un brouillon ne part pas tout seul : Souleman l'ouvre sur
son telephone, corrige, et envoie lui-meme. La validation reste humaine,
pas la redaction.

Il ne marque rien comme lu, ne supprime rien, ne classe rien.

Le modele ecrit un petit fichier json dans le dossier travail, puis lance ce script
avec le chemin de ce fichier. Forme attendue :

    {
      "fil": "<identifiant du fil, ligne fil: du fichier de travail>",
      "repondre_a_id": "<ligne repondre_a_id: du fichier de travail>",
      "identite": "principal" ou "sweb",
      "a": "adresse@exemple.com",
      "sujet": "Re: ...",
      "corps": "le texte de la reponse, en clair"
    }

Le sujet et le destinataire peuvent etre omis : ils sont repris du message
auquel on repond. C'est le cas normal.

Usage :
    python brouillon.py <fichier.json>

Il ecrit une ligne sur la sortie standard : l'identifiant du brouillon cree,
ou la raison de l'echec. Un echec ici ne doit jamais faire perdre la capture
deposee dans le coffre, il se signale et c'est tout.
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from email.message import EmailMessage
from email.utils import formataddr, parseaddr

RACINE = "C:/Obsidian"
JETON = "https://oauth2.googleapis.com/token"
API = "https://gmail.googleapis.com/gmail/v1/users/me"
DELAI = 30


def identifiants(dossier):
    for c in (os.path.join(RACINE, "google.local.json"),
              os.path.join(dossier, "google.local.json")):
        if os.path.exists(c):
            with open(c, encoding="utf-8") as f:
                return json.load(f)
    return None


def acces(c):
    corps = urllib.parse.urlencode({
        "client_id": c["client_id"],
        "client_secret": c["client_secret"],
        "refresh_token": c["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request(JETON, data=corps, method="POST")
    with urllib.request.urlopen(req, timeout=DELAI) as r:
        return json.loads(r.read().decode("utf-8"))["access_token"]


def get(url, jeton):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + jeton})
    with urllib.request.urlopen(req, timeout=DELAI) as r:
        return json.loads(r.read().decode("utf-8"))


def poster(url, jeton, charge):
    donnees = json.dumps(charge).encode("utf-8")
    req = urllib.request.Request(url, data=donnees, method="POST",
                                 headers={"Authorization": "Bearer " + jeton,
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=DELAI) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 2:
        print("usage: brouillon.py <fichier.json>")
        return 2

    fichier = sys.argv[1]
    if not os.path.exists(fichier):
        print("ECHEC, fichier introuvable : " + fichier)
        return 1
    try:
        with open(fichier, encoding="utf-8-sig") as f:
            d = json.load(f)
    except Exception as e:
        print("ECHEC, json illisible, %s" % e)
        return 1

    corps = (d.get("corps") or "").strip()
    if not corps:
        print("ECHEC, corps vide, aucun brouillon cree")
        return 1

    base = os.path.dirname(os.path.abspath(fichier))
    conf = identifiants(base) or identifiants(os.path.dirname(base))
    if not conf:
        print("ECHEC, google.local.json introuvable")
        return 1

    try:
        jeton = acces(conf)
    except Exception as e:
        print("ECHEC, jeton refuse, %s" % e)
        return 1

    identites = conf.get("identites") or {}
    cle = d.get("identite", "principal")
    expediteur = identites.get(cle) or identites.get("principal") or ""
    if not expediteur:
        print("ECHEC, aucune identite d'expediteur dans google.local.json")
        return 1

    # Le message auquel on repond donne le destinataire, le sujet, et les
    # deux en-tetes qui rattachent la reponse au fil chez le destinataire.
    a = d.get("a", "")
    sujet = d.get("sujet", "")
    ref = ""
    fil = d.get("fil", "")
    mid = d.get("repondre_a_id", "")
    if mid:
        try:
            m = get(API + "/messages/" + mid + "?format=metadata"
                    + "&metadataHeaders=From&metadataHeaders=Subject"
                    + "&metadataHeaders=Message-ID&metadataHeaders=References", jeton)
            ent = {h["name"].lower(): h["value"] for h in m.get("payload", {}).get("headers", [])}
            if not a:
                a = ent.get("from", "")
            if not sujet:
                s = ent.get("subject", "") or ""
                sujet = s if s.lower().startswith("re:") else ("Re: " + s if s else "Re:")
            ref = ent.get("message-id", "")
            if not fil:
                fil = m.get("threadId", "")
        except Exception as e:
            print("avertissement, message d'origine illisible, %s" % e)

    if not a:
        print("ECHEC, aucun destinataire")
        return 1

    nom, adr = parseaddr(a)
    msg = EmailMessage()
    msg["To"] = formataddr((nom, adr)) if nom else adr
    msg["From"] = expediteur
    msg["Subject"] = sujet or "Re:"
    if ref:
        msg["In-Reply-To"] = ref
        msg["References"] = ref
    msg.set_content(corps)

    charge = {"message": {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")}}
    if fil:
        charge["message"]["threadId"] = fil

    try:
        r = poster(API + "/drafts", jeton, charge)
    except urllib.error.HTTPError as e:
        try:
            motif = e.read().decode("utf-8")[:300]
        except Exception:
            motif = ""
        print("ECHEC, Gmail a refuse le brouillon, HTTP %s %s" % (e.code, motif))
        return 1
    except Exception as e:
        print("ECHEC, brouillon impossible, %s" % e)
        return 1

    print("brouillon %s cree, de %s vers %s, sujet %s"
          % (r.get("id", "?"), re.sub(r"<.*>", "", expediteur).strip() or expediteur,
             adr, msg["Subject"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
