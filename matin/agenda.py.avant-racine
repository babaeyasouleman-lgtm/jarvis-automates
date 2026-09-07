# -*- coding: utf-8 -*-
"""
Pont vers Google Agenda. Phase 3 du Plan Jarvis.

Deterministe, aucun appel a un modele. Il lit les evenements du jour et
ecrit agenda.txt, que la note du matin lit ensuite comme un simple fichier.

Pourquoi ce pont existe : les connecteurs Google de l'app Claude ne sont
pas visibles en mode `claude -p`. Verifie le 3 septembre 2026, ni l'agenda
ni Gmail. Le CLI a sa propre configuration MCP, et aucun plugin Google n'y
figure. Plutot que d'ajouter un jeton de plus, on reutilise celui que
l'agent WhatsApp possede deja. Une seule identite Google, comme le plan
l'exige.

Il ne plante jamais. Si les identifiants manquent ou si Google refuse, il
ecrit statut=indisponible et sort en 0. La note du matin continue.

Identifiants attendus dans google.local.json, a cote de ce fichier :

    {
      "client_id": "...",
      "client_secret": "...",
      "refresh_token": "...",
      "calendriers": ["primary"],
      "fuseau": "America/Toronto"
    }

Ce nom de fichier est exclu du depot jarvis-automates par *.local.*, il ne
part donc ni sur GitHub ni dans le miroir. Ne le renomme pas.

Usage :
    python agenda.py <dossier> [AAAA-MM-JJ]
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

JETON = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/calendar/v3/calendars/%s/events?%s"
DELAI = 20


def ecrire(chemin, lignes):
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")


def poster(url, donnees):
    corps = urllib.parse.urlencode(donnees).encode("utf-8")
    req = urllib.request.Request(url, data=corps, method="POST")
    with urllib.request.urlopen(req, timeout=DELAI) as r:
        return json.loads(r.read().decode("utf-8"))


def lire(url, jeton):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + jeton})
    with urllib.request.urlopen(req, timeout=DELAI) as r:
        return json.loads(r.read().decode("utf-8"))


def heure(ev, cle):
    """Retourne HH:MM, ou 'journee' pour un evenement sans heure."""
    bloc = ev.get(cle, {})
    if "dateTime" in bloc:
        # 2026-09-04T09:00:00-04:00
        return bloc["dateTime"][11:16]
    return "journee"


def main():
    dossier = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    sortie = os.path.join(dossier, "agenda.txt")
    config = os.path.join(dossier, "google.local.json")

    if not os.path.exists(config):
        ecrire(sortie, ["statut=indisponible",
                        "raison=google.local.json absent, identifiants jamais deposes"])
        return 0

    try:
        with open(config, encoding="utf-8") as f:
            c = json.load(f)
    except Exception as e:
        ecrire(sortie, ["statut=indisponible", "raison=google.local.json illisible, %s" % e])
        return 0

    manque = [k for k in ("client_id", "client_secret", "refresh_token") if not c.get(k)]
    if manque:
        ecrire(sortie, ["statut=indisponible", "raison=champs manquants, %s" % ", ".join(manque)])
        return 0

    # 1. Echanger le refresh token contre un access token, valable une heure.
    try:
        rep = poster(JETON, {
            "client_id": c["client_id"],
            "client_secret": c["client_secret"],
            "refresh_token": c["refresh_token"],
            "grant_type": "refresh_token",
        })
        acces = rep["access_token"]
    except urllib.error.HTTPError as e:
        # Le corps de l'erreur Google peut contenir le motif, jamais le jeton.
        try:
            motif = json.loads(e.read().decode("utf-8")).get("error", "")
        except Exception:
            motif = ""
        ecrire(sortie, ["statut=indisponible",
                        "raison=Google a refuse le refresh token, HTTP %s %s" % (e.code, motif)])
        return 0
    except Exception as e:
        ecrire(sortie, ["statut=indisponible", "raison=echange du jeton impossible, %s" % e])
        return 0

    # 2. La journee, dans le fuseau du PC.
    if len(sys.argv) > 2:
        jour = datetime.strptime(sys.argv[2], "%Y-%m-%d").astimezone()
    else:
        jour = datetime.now().astimezone()
    debut = jour.replace(hour=0, minute=0, second=0, microsecond=0)
    fin = debut + timedelta(days=1)

    calendriers = c.get("calendriers") or ["primary"]
    fuseau = c.get("fuseau", "")

    lignes = []
    incidents = []
    for cal in calendriers:
        params = {
            "timeMin": debut.isoformat(),
            "timeMax": fin.isoformat(),
            "singleEvents": "true",
            "orderBy": "startTime",
            "maxResults": "50",
        }
        if fuseau:
            params["timeZone"] = fuseau
        url = API % (urllib.parse.quote(cal, safe=""), urllib.parse.urlencode(params))
        try:
            data = lire(url, acces)
        except Exception as e:
            incidents.append("%s, %s" % (cal, e))
            continue
        for ev in data.get("items", []):
            if ev.get("status") == "cancelled":
                continue
            titre = (ev.get("summary") or "sans titre").replace("\n", " ").strip()
            lignes.append("%s  %s" % (heure(ev, "start"), titre))

    lignes.sort()

    if incidents and not lignes:
        entete = ["statut=indisponible", "raison=" + " ; ".join(incidents)]
        ecrire(sortie, entete)
        return 0

    entete = ["statut=ok" if lignes else "statut=vide",
              "date=" + debut.strftime("%Y-%m-%d"),
              "agendas=%d" % len(calendriers)]
    if incidents:
        entete.append("incidents=" + " ; ".join(incidents))
    ecrire(sortie, entete + lignes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
