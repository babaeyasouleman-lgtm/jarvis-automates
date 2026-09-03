---
name: courriel-froid-avant-appel
description: "Depuis le 2026-08-19, Souleman fait preceder l'appel d'un courriel froid portant une image de maquette, envoye automatiquement par le skill prospect-email."
metadata: 
  node_type: memory
  type: project
  originSessionId: da719d84-6a09-49b1-b498-3a002649bb6f
  modified: 2026-08-19T15:16:16.738Z
---

Souleman a ajoute une etape **avant** l'appel de l'etape A de son processus: un courriel
froid qui porte **une image** de ce a quoi le site du prospect pourrait ressembler, plus
un appel a une rencontre de 15 minutes sans engagement. Automatise dans le skill
`prospect-email` (`~/.claude/skills/prospect-email/`) et dans la tache planifiee
`lot-prospection-courriel`, mardi et jeudi 12 h 05, 3 prospects par execution.

Trois choix qu'il a tranches lui-meme le 2026-08-19, contre les options proposees:

- **Envoi automatique**, pas des brouillons a relire. Les garde-fous sont dans `ENVOI.md`:
  6 par jour, 12 par semaine, fenetre lun-ven 8 h a 20 h, liste de suppression, et le
  mode bascule tout seul sur `brouillon` si les coordonnees LCAP manquent.
- **L'image montre la maquette dans un cadre ordinateur avec un telephone devant**, pas un
  avant/apres, pas une capture seule.
- **Source voulue: le CRM Notion de FM Media**, pas encore accessible depuis son compte.

**Pourquoi:** son processus dit que la maquette ne part jamais par courriel avant le Meet.
Ce skill respecte la regle, il envoie une capture et jamais le fichier HTML. Le courriel
ne vend pas le forfait, il rechauffe l'appel qui suit.

**Comment l'appliquer:** pour une URL de prospect avec un Meet deja fixe, c'est
[[prospect-demo-workflow]] et le skill `prospect-site`. Pour un premier contact froid,
c'est `prospect-email`. Le texte suit [[no-em-dashes-no-ai-voice]] et les creneaux
proposes suivent [[sweb-contexte-de-travail]].
