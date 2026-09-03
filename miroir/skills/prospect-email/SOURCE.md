# D'ou viennent les prospects

## Etat au 2026-08-19

**Le CRM de FM Media n'est pas accessible.** Le compte Notion connecte
(`babaeyasouleman@gmail.com`) ne voit qu'un seul espace, "Espace de Souleman Baba", qui
porte le projet fintech de Libreville. Aucune base de prospects S-WEB dedans, ce qui
confirme ce que dit la memoire `sweb-contexte-de-travail`.

**Depuis le 2026-08-21, la file n'attend plus personne.** `moisson.py` la remplit depuis
Google Maps. Notion reste branchable, mais ce n'est plus un blocage.

```bash
python scripts/moisson.py "salon de coiffure" --ville "Gatineau QC" --courriels --max 12
```

Le binaire est `gosom/google-maps-scraper` (MIT, aucune cle API), attendu dans
`~/.local/bin/gmaps.exe`, ou a l'endroit que pointe `GMAPS_BIN`. Il pilote un Chrome sans
interface: environ 2 minutes par requete, le double avec `--courriels` qui va crawler
chaque site pour y trouver une adresse.

**Ce qui sort n'est pas une liste, c'est un classement.** Le score monte quand il n'y a
aucun site et que les avis sont nombreux: un commerce qui roule et qui n'a rien en ligne
est le meilleur prospect possible. `--seuil 6` ne garde que les sans-site, `--seuil 4`
garde aussi les sites a refaire, `--seuil 2` ratisse large.

Quatre filtres tournent avant l'ecriture:

- **les chaines**, qui n'achetent pas un site a un pigiste
- **les injoignables**, sans telephone ni courriel
- **les doublons**, par telephone, domaine et courriel, contre `FILE-ATTENTE.tsv`,
  `ENVOYES.tsv` et `NE-PAS-CONTACTER.txt`
- **les demos deja baties**, par mots distinctifs contre les dossiers du Bureau et
  `prospect-site/BUILT.tsv`. Le rapprochement se fait sur les mots qui identifient, pas
  sur le nom entier: le dossier dit `Clinique-Infinium`, Google dit
  `INFINIUM Medecine Esthetique | Aesthetic Medicine`. Zero prefixe commun, un seul mot
  qui compte. Sans ce filtre, Infinium et Paramedika sont revenues comme prospects neufs
  le jour meme ou il a ete ecrit.

**Toujours passer `--essai` la premiere fois sur un metier neuf.** Il affiche le classement
sans rien ecrire. Le CSV brut est conserve dans `Prospection/moisson/`, donc `--rejouer`
retrie sans rappeler Google.

Deux choses a savoir. Ca contrevient aux conditions d'utilisation de Google Maps, et un
usage soutenu fait bloquer l'IP quelques heures, jamais le compte. A six courriels par
jour, une moisson par semaine suffit largement.

---

La routine peut aussi tourner sur Notion, et bascule dessus des que la ligne
`DATA_SOURCE` ci-dessous est remplie. Rien d'autre a changer.

```
DATA_SOURCE:
VUE:
```

---

## Pour brancher Notion, une fois

1. FM Media ouvre la base des prospects dans Notion, bouton **Partager**, invite
   `babaeyasouleman@gmail.com` en **Peut modifier**. Le droit de modification est
   necessaire: la routine ecrit le statut apres l'envoi.
2. Copier l'URL de la base et la coller dans `DATA_SOURCE` ci-dessus.
3. Verifier: `notion-fetch` sur cette URL doit retourner une balise
   `<data-source url="collection://...">`. C'est ce `collection://` que les requetes
   utilisent.

Si FM Media refuse le partage, l'autre voie est un export CSV hebdomadaire de leur base
vers `FILE-ATTENTE.tsv`. C'est moins bon: deux sources de verite finissent toujours par
diverger.

---

## Comment la routine lit Notion, une fois branche

```
notion-fetch(id=<DATA_SOURCE>)              -> recuperer le collection://
notion-query-data-sources(mode=sql, data_source_urls=["collection://..."],
  query='SELECT * FROM "collection://..." WHERE Statut IS NULL OR Statut = ? LIMIT 3',
  params=["A contacter"])
```

Le plan Notion actuel limite `query_data_sources` (statut `available_with_limit`), donc
**une seule requete par execution**, jamais une par prospect. Sortir les 3 fiches d'un
coup, puis travailler hors ligne.

Apres l'envoi, `notion-update-page` sur la fiche: statut `Courriel envoye`, la date, et
la date de relance a J+3.

**Correspondance des colonnes.** Les neuf colonnes de son processus, etape A:

| FILE-ATTENTE.tsv | Notion FM Media |
|---|---|
| `nom` | Nom |
| `ville` | Ville |
| `metier` | Metier |
| `site` | Site |
| `courriel` | Courriel |
| `decideur` | Nom du decideur |
| `telephone` | Telephone |
| `statut` | Statut |
| `note` | Notes |

La colonne "qui appelle" de son processus reste dans Notion et n'est pas reprise ici: la
routine ecrit toujours au nom de Souleman. **Si une fiche est assignee a FM Media ou a
Pierre, la sauter.** Deux courriels de la meme agence au meme commerce, c'est le pire
resultat possible.
