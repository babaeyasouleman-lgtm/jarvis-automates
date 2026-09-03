---
name: cagnotte-live-gala-mlm
description: "Projet gala-cagnotte pour la Fondation Million Little Miracles, gala du 30 août 2026, et ce qui manque encore pour le jour J."
metadata: 
  node_type: memory
  type: project
  originSessionId: 21241063-adb5-47e8-9acd-794f954ed194
  modified: 2026-08-29T03:20:24.261Z
---

Application construite le 28 août 2026, déplacée le 29 août dans `C:\gala-cagnotte`
(hors de OneDrive, dont la synchro peut verrouiller `state.json` en pleine soirée),
pour le gala MLM. **Conflit de date non résolu :** le PRD annonce dimanche 30 août 2026,
alors que `Strategie_Gala2026_Synthese_MLM.docx`, `MLM_Brief_Communication_Gala2026.docx`
et la configuration Zeffy disent tous **samedi 29 août 2026**. À trancher avec la fondation. Serveur Node local sur le laptop du
projecteur, `/` en salle et `/admin` sur le téléphone de l'opérateur, WebSocket, aucun
internet requis. PRD source : `C:\Users\Administrator\Downloads\PRD-Cagnotte-Live-Gala-MLM.md`.

La décision de design qui gouverne tout : **l'objectif de 5 000 $ ne paraît jamais sur
l'écran public**, ni pourcentage, ni plafond. Seulement le prochain palier et ce qu'il
débloque. L'objectif reste visible sur `/admin` uniquement. Ne jamais dupliquer l'écran
sur le projecteur, toujours l'étendre.

Restait à fournir au moment de la livraison, tout se règle dans `config.json` sans
toucher au code :
- ~~les libellés d'impact~~ faits le 29 août à partir de `Downloads\Les Graines _ The Seeds.docx`.
  Unité de référence : **500 $ CAD = une année scolaire complète pour un enfant** (programme
  Les Graines, volet Éducation, Togo, partenaire Unissons-nous ONG). Toute l'échelle en découle.
  Ce document fixe aussi l'objectif du gala à **3 000 $**, pas 5 000 $ comme le PRD ;
- ~~les polices~~ fait : Poppins et Cinzel Decorative en local. Le brief de communication
  désigne Cinzel Decorative comme l'équivalent numérique officiel de Trinstam, réservée aux
  capitales de prestige ; Poppins pour tout le corps de texte ;
- `public/audio/celebration.mp3` ;
- confirmation de Square (source désactivée par défaut) ;
- le total de départ, 0 ou dons déjà collectés en amont.

Le logo horizontal `public/img/logo-mlm.png` a été découpé au script depuis
`Downloads\LOGO MLM B.png` : fond noir passé en alpha, marque et bloc texte
recomposés côte à côte.

Rien à héberger : le soir du gala, l'hôte est le laptop du projecteur. Pour une démo à
distance, `npx --yes cloudflared tunnel --url http://localhost:3000` donne une URL publique
vers le laptop. Testé le 29 août : HTTPS et WSS passent, les mutations et les célébrations
arrivent côté distant. Cette URL donne aussi accès à `/admin`, donc ne la partager que
pendant la démo et refermer ensuite.

Voir [[sweb-contexte-de-travail]] et [[jamais-ancrer-la-valeur-sur-le-temps]].
