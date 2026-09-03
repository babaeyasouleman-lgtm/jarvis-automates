---
name: note-du-matin
description: Prépare chaque matin la note du jour de Souleman dans son coffre Obsidian, avec agenda, décisions à revoir, relances et prochaines actions.
---

Tu prépares la note du jour de Souleman dans son coffre Obsidian. Tu travailles seul, sans lui poser de question. Le résultat est un fichier écrit sur son disque, pas un message.

# Le coffre

`C:\Obsidian\Second Brain`

Structure : `00 Inbox`, `01 Journal`, `02 Projets`, `03 Domaines`, `04 Ressources`, `05 Décisions`, `06 Personnes`, `07 Cartes`, `99 Archives`, `_Modèles`, `_Fichiers`.

Les notes ont un en-tête YAML entre deux lignes de tirets, avec des clés sans accent : `type`, `statut`, `date`, `revoir`, `relance`, `echeance`, `domaine`, `categorie`.

# Ce que tu produis

Le fichier `01 Journal/AAAA-MM-JJ.md` à la date du jour.

**Si le fichier existe déjà et contient du texte écrit par Souleman, ne l'écrase jamais.** Insère ta section préparée juste après le titre H1, et laisse tout le reste intact. En cas de doute, n'écris pas et signale-le.

# Comment tu le construis

Lis d'abord le coffre, puis assemble.

## 1. L'agenda du jour

Utilise le connecteur Google Agenda pour lister les évènements d'aujourd'hui. Donne l'heure et le titre. Si un évènement correspond à une personne ou un projet ayant une note dans le coffre, mets un lien `[[Nom de la note]]`.

Si le connecteur ne répond pas, écris « Agenda indisponible ce matin » et continue. N'invente jamais un rendez-vous.

## 2. Ce que j'avais prévu hier

Ouvre la note de la veille dans `01 Journal`. Reprends les cases non cochées de sa section « Demain ». Si la note de la veille n'existe pas, saute cette partie.

## 3. Décisions à revoir

Parcours `05 Décisions`. Retiens celles dont la clé `revoir` est une date passée ou égale à aujourd'hui, et dont le `statut` est `prise`. Pour chacune, donne le lien et une ligne rappelant ce qui devait être vérifié.

## 4. Personnes à relancer

Parcours `06 Personnes`. Retiens celles dont la clé `relance` est passée ou égale à aujourd'hui.

## 5. Prochaines actions

Parcours `02 Projets`. Pour chaque note avec `statut: actif`, prends la première case non cochée de sa section « Prochaine action ». Ignore les projets `en pause`.

Trie par urgence : d'abord ceux dont la clé `echeance` est proche ou dépassée.

## 6. Deux questions en attente

Ouvre `00 Inbox/À confirmer`. Choisis deux questions non cochées, en priorisant celles qui bloquent un projet actif. Recopie-les avec leur ligne `→` vide.

Change de questions chaque jour, ne repose pas les mêmes deux jours de suite.

# Le format du fichier

```
---
type: journal
date: AAAA-MM-JJ
---

# <Jour> <numéro> <mois> <année> en français, par exemple : Jeudi 27 août 2026

## Aujourd'hui

<agenda, ou « Rien au calendrier »>

## Repris d'hier

<cases non cochées de la section Demain de la veille>

## Décisions à revoir

<liens et rappels, ou rien du tout si la liste est vide>

## À relancer

<personnes, ou rien du tout si la liste est vide>

## Prochaines actions

<une case à cocher par projet actif>

## Deux questions

<deux questions de À confirmer, avec leur ligne →>

---

## Capture

- 

## Fait aujourd'hui

- 

## Décidé aujourd'hui

- 

## Demain

- [ ] 
```

# Règles d'écriture

- Français, tutoiement, phrases courtes.
- **Aucun tiret cadratin.** Ni dans le fichier, ni ailleurs.
- Pas de vocabulaire marketing, pas d'emoji, pas de formule d'encouragement.
- **Supprime toute section vide** plutôt que d'écrire « rien à signaler ». Une note du matin doit tenir sur un écran de téléphone.
- N'invente aucune donnée. Si une information manque, la section disparaît.
- Ne modifie aucun autre fichier du coffre.

# Après l'écriture

Termine par un résumé de trois lignes maximum : la date écrite, le nombre d'éléments dans chaque section, et tout ce qui a échoué.