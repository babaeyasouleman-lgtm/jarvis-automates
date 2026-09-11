---
name: jarvis-cout-des-sessions
description: "Ce qui coute vraiment dans une session Jarvis, mesure le 10 septembre 2026 sur les transcriptions : porter le contexte, pas le lire. Les regles qui en sortent et le fichier d'entree C:\\Obsidian\\ENTREE.md."
metadata: 
  node_type: memory
  type: project
  originSessionId: eee27d88-f723-4809-8264-1500fd32fce5
  modified: 2026-09-11T03:43:57.801Z
---

Mesure du 10 septembre 2026 sur onze sessions Jarvis. Session de reference, la phase 8 : 350 M tokens, 680 appels, 34 prompts, contexte de 68 k a 966 k sans compaction, 98,9 % en relecture de cache. Etalonnage : 1 Ko de ses fichiers vaut 620 tokens.

**Ce qui coute.** Chaque appel renvoie tout le contexte. Un fichier lu tot est refacture a chaque appel qui suit. Les 15 % d'appels de la fin pesent 24 % de chaque session. Classement phase 8 : code lu par cat 28 %, socle fixe de 66 k tokens par appel 13 %, Plan Jarvis 10 %, automates 10 %, prose de l'assistant 9 %. Les commentaires du code pesent 5 %. CLAUDE.md du depot (77 Ko) et BUILT.tsv ne sont jamais lus dans une session Jarvis : ce sont des couts de prospect-site.

**Ce qu'il paie.** Abonnement Max. Ce qui lui fait mal, c'est buter sur la limite en pleine session, et c'est la fin des sessions longues qui la consomme. Les nuits du bibliothecaire (1,5 M en moyenne) et prospect-site (44 % du total) sont acceptes, hors chantier.

**Les regles, ecrites dans `C:\Obsidian\ENTREE.md`** : une phase par session, fermer a 300 k de contexte, exploration du code par sous-agent, plage exacte avant d'editer, un test a la fois, compte rendu en 40 lignes. Le prompt d'ouverture d'une session Jarvis est cinq lignes dont la premiere est « Lis C:\Obsidian\ENTREE.md ». La session met ce fichier a jour en dix lignes avant de fermer ; le recit va dans Plan Jarvis.md.

**Why:** il a pose ces regles apres la mesure, en disant qu'il accepte de perdre du detail en route et de ne pas voir ce qu'un sous-agent lit, tant que le compte rendu ne ment pas.
**How to apply:** ne jamais lire Plan Jarvis.md, un fichier memoire ou un journal.log en entier. Ne pas proposer de deplacer les commentaires du code hors des fichiers, il tient a cette histoire et elle coute 5 %. Voir [[agent-whatsapp-modules]] et [[coffre-automatisations]].
