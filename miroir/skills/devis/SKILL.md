---
name: devis
description: Produce S-WEB Agency business documents in editable Word format, in Canadian French, from a fixed price grid. Three document types, soumission (quote), facture (invoice) and contrat (service agreement), each generated from a JSON spec, watermarked, and verified by opening in Word. Use when the user asks for a devis, une soumission, un prix, une facture, un contrat, or says "fais-moi un devis pour ce client", "combien je charge", "envoie-lui une facture".
---

# Documents d'affaires, S-WEB Agency

Produit trois documents en **Word éditable**, en français du Québec, à partir d'une grille de
prix fixe. Il les modifie ensuite lui-même avant de les envoyer.

**Aucun montant ne s'invente.** Tout prix vient de `TARIFS.md`. S'il n'y est pas, on le
demande, on ne l'estime pas. C'est la règle qui compte le plus dans ce skill.

---

## Avant tout, lire deux fichiers

Un seul appel groupé:

- **`TARIFS.md`**, l'identité, les prix, les partenaires, les conditions. Source unique.
- **`HISTORIQUE.md`**, ce qui a déjà été émis, le prochain numéro, et ce qu'il a corrigé la
  dernière fois.

`MODELES.md` se lit seulement au moment de construire le JSON.

---

## Ce qui est déjà tranché, ne pas le redemander

| | |
|---|---|
| Langue | français du Québec. **Soumission**, pas devis. Courriel, main-d'œuvre |
| Format | **Word seulement.** PDF uniquement s'il le demande |
| Taxes | **aucune**, non inscrit. Ne jamais écrire « taxes en sus » |
| Filigrane | oui, injecté dans l'en-tête |
| Prix | grille fixe, appliquée sans demander confirmation |
| Rangement | `Bureau/Devis/<Client>/` |

---

## Les trois documents

### Soumission

Le document de vente. Structure qui a fonctionné, dans cet ordre:

1. **Bloc client et agence**, filet orange, titre, intro. L'intro porte le délai de deux
   semaines, parce que c'est un argument, pas un détail.
2. **Le produit et son prix**, en encadré. Ce que le client cherche en premier.
3. **Ce qui est compris sans frais additionnels.** Les partenaires nommés: 4 consultations de
   30 min par FM Media, 10 photos et 1 reel par Pose Ta Pierre. **C'est la page qui justifie
   l'écart avec un concurrent moins cher**, il ne faut pas la noyer.
4. **Les modules**, en tableau, avec une description par ligne qui dit ce que ça fait pour le
   client, pas ce que ça demande de travail.
5. **L'identité de marque** s'il y a lieu, avec le palier recommandé marqué.
6. **Récapitulatif** et total ponctuel.
7. **Entretien mensuel**, les trois paliers en grille comparative, plus la définition d'un
   changement de contenu et le 75 $ l'heure.
8. **Échéancier** qui commence par une ligne « Départ » listant ce que le client doit fournir.
   Le compteur ne part pas à la signature.
9. **De notre côté, de votre côté**, en deux cartes.
10. **Conditions**, puis **Pour aller de l'avant** en trois étapes, puis les signatures.

### Facture

Reprend la soumission acceptée. Diffère sur quatre points: numéro de facture distinct de
celui de la soumission, référence à la soumission d'origine, **montant dû et date
d'échéance**, et le lien de paiement Stripe. Pas de signatures, pas d'échéancier.

### Contrat

**Dire une fois, par dossier, que ce n'est pas un document rédigé par un juriste et qu'il
doit être relu avant d'être signé.** Une fois, pas à chaque message.

Reprend le périmètre de la soumission et ajoute: durée, propriété intellectuelle et moment du
transfert, confidentialité, résiliation de part et d'autre, limitation de responsabilité,
et ce qui arrive au dépôt si le client se retire.

---

## Construire le document

### 1. Numéro

Format `2026-001`. Le prochain est dans `HISTORIQUE.md`. Un numéro par document émis, jamais
réutilisé, même si le document est refait.

### 2. Écrire le JSON

Voir `MODELES.md` pour les blocs disponibles et un exemple complet. Le ranger dans le dossier
du client, il sert de source si un prix change plus tard.

### 3. Générer

```bash
cd <dossier de travail>
npm install docx --silent          # une seule fois par dossier, pas globalement
node <skill>/scripts/build_docx.js spec.json "Soumission-Client.docx"
python <skill>/scripts/filigrane.py "Soumission-Client.docx"
```

### 4. Vérifier, toujours, en deux appels séparés

```bash
powershell -ExecutionPolicy Bypass -File <skill>/scripts/verifier.ps1 -Docx "Soumission-Client.docx"
powershell -ExecutionPolicy Bypass -File <skill>/scripts/apercu.ps1 -Dir "_apercu"
```

Puis **regarder la planche** dans `_apercu/planche.png`. Une seule lecture d'image montre les
six pages.

`verifier.ps1` fait ouvrir le document par Word, ce qui est la seule preuve solide qu'il
n'est pas corrompu, et exporte un PDF. `apercu.ps1` rend ce PDF en images et les assemble.

**Les deux doivent rester des processus distincts.** Word en COM et le moteur PDF de Windows
en WinRT dans le même processus PowerShell se bloquent mutuellement, sans erreur et sans fin.

Ce qu'on cherche sur la planche: une page qui déborde, un tableau dont les colonnes ont
glissé, un texte devenu invisible, un logo absent, un filigrane trop appuyé.

**Si un script reste bloqué**, ne pas rallonger le délai: aller lire les pièges en tête de
`verifier.ps1`. Ils sont tous documentés, et le plus vicieux est le point 5.

### 5. Livrer et consigner

Envoyer le `.docx`. Puis **écrire l'entrée dans `HISTORIQUE.md`**: numéro, client, date,
montant, et ce qu'il a demandé de changer. C'est ce qui fait progresser le skill.

---

## Erreurs déjà commises, à ne pas refaire

- **« Taxes en sus s'il y a lieu »** a été écrit sur une vraie soumission alors qu'il n'est
  pas inscrit. La formule sous-entend des taxes à venir. Ne jamais l'employer.
- **Aucun courriel ni téléphone sur le document.** La cliente ne savait pas où retourner le
  document signé. Le bloc de contact est obligatoire.
- **Les partenaires n'étaient pas nommés** et le contenu du forfait restait vague. « Une
  consultation » vaut bien moins que « 4 consultations de 30 minutes par FM Media ».
- **Un montant estimé de tête.** Chaque prix vient de `TARIFS.md`.
- **Un fait tiré d'un annuaire écrit comme un fait établi.** Le nom de son outil de
  réservation, « Fresha », est entré dans la 2026-003 depuis une fiche trouvée en recherche
  web, pas depuis son site ni depuis le client. Elle ne l'utilisait pas. **Ce qui vient d'un
  annuaire se signale comme à confirmer, ou ne s'écrit pas.** Même exigence que pour les
  montants: si ce n'est pas vérifié, on demande, on ne suppose pas.
- **Toute mention de taxes.** Ni « taxes en sus », ni « aucune taxe n'est facturée », ni la
  non-inscription. Le prix affiché est le prix, le document n'aborde pas le sujet.
- **Du texte blanc sur une cellule à fond clair** disparaît dans Word. Colorer le texte, pas
  le fond, quand on veut une pastille.
- **Chrome headless ne rend pas les PDF.** La capture sort vide. Passer par `apercu.ps1`.
- **Sur la fin d'un document, le saut se place avant le bloc de signature, pas avant les
  conditions.** Sans saut, le bloc de signature se scinde en deux pages, ce qui est pire qu'une
  page aérée. Avec le saut avant « Conditions », la page précédente tombe à 20 %. Constaté sur
  la 2026-012, trois positions essayées.
- **Ajouter une ligne à un tableau oblige à relire la note qui le suit.** Sur la 2026-012, une
  deuxième ligne d'option a fait porter « facturé au coût, sans marge » sur du travail interne.
  Erreur silencieuse qui ment sur la marge, invisible à la relecture de la planche.
- **Enchaîner génération et correction avec `&&`, jamais par retour à la ligne.** Sur la
  2026-012 un ancrage introuvable a fait échouer la correction, et la commande suivante a
  reconstruit le document depuis une source inchangée sans que rien ne le signale.
- **Quand le `saut` avant la signature laisse une page creuse, deplacer du contenu vers cette
  page plutot que retirer le saut.** Sur la 2026-013, la derniere page ne portait que trois
  etapes et le bloc de signature, aux deux tiers vide. Le bloc `deuxcartes` a ete remonte de
  l'avant-derniere page vers la derniere, sous son propre `h2`: les deux pages se remplissent
  et la signature reste d'un seul tenant. Suite directe du constat de la 2026-012.
- **Un rabais ecrit dans un tableau se lit comme un retrait de portee.** Sur la 2026-013, la
  ligne negative `-499 $` porte une description qui dit explicitement que rien n'est retire du
  contenu, et une `note` le repete sous la liste de ce qui est compris. Sans cette phrase, le
  client conclut qu'un prix reduit veut dire une livraison reduite.
- **Un client qui a deja paye ne doit jamais relire le montant global comme s'il restait du.**
  Sur la 2026-013, les versements sont un second tableau `lignes`, distinct du recapitulatif,
  avec la ligne encaissee en `fill: true` et un total intitule **Solde a regler**. Une note
  ajoutee sous un tableau unique ne suffit pas.
- **Un `saut` ne se place jamais juste après un bloc `lignes`, il se place avant.** Le tableau
  se coupe entre deux pages et le saut renvoie tout le reste à la page suivante, ce qui laisse
  une page ne portant que la ligne de total. Constaté sur la 2026-014, **reproduit à l'identique
  sur la 2026-015**. Le déplacer avant le titre du récapitulatif règle les deux cas.
- **Trop de `saut` produit dix pages remplies au tiers**, ce qui est aussi mauvais qu'un
  débordement et se voit moins. Les repères de hauteur de `MODELES.md` surestiment le contenu
  réel d'environ 40 %. **Compter les sauts avant de générer**: un document de sept pages n'en
  porte pas plus de cinq ou six, et le contenu qui coule d'une page à l'autre remplit mieux
  qu'un bloc forcé sur sa propre page. Constaté sur la 2026-010.

### Pièges techniques payés cher, tous déjà résolus dans les scripts

- **`ExportAsFixedFormat($chemin)` ne rend jamais la main**, alors que le même chemin écrit
  en littéral fonctionne. Une variable nue passée à une méthode COM de Word est marshalée
  d'une façon qu'il n'accepte pas. Écrire `"$chemin"` entre guillemets. Ce bug fait perdre
  des heures parce qu'il pousse à soupçonner le chemin, le dossier ou OneDrive.
- **Word et WinRT dans le même processus PowerShell** se bloquent l'un l'autre. D'où deux
  scripts.
- **Une instance Word tuée de force** laisse Word vouloir afficher son volet de récupération
  au démarrage suivant, ce qui bloque toute automatisation sans message.
- **`require('docx')` échoue** quand le script est appelé depuis un autre dossier. Node
  résout depuis le dossier du script. Le générateur reprend explicitement depuis
  `process.cwd()`.
- **Un script bloqué ne se règle pas en augmentant le délai.** Instrumenter avec des
  `Write-Host` entre chaque appel et isoler l'étape.

---

## Le skill se corrige tout seul

À la fin de chaque utilisation, sans qu'il ait à le demander:

1. **Un prix, une condition ou un partenaire a changé** → mettre à jour `TARIFS.md`, avec la
   date.
2. **Il a corrigé une formulation ou une structure** → l'écrire dans `HISTORIQUE.md` sous
   « Ce qui a été corrigé », avec ses mots.
3. **Un piège technique nouveau** → l'ajouter à « Erreurs déjà commises » ci-dessus.
4. **Une question posée deux fois** → sa réponse devient une valeur par défaut dans
   `TARIFS.md`, et la question disparaît.

Une préférence enregistrée une fois ne doit plus jamais être redemandée.
