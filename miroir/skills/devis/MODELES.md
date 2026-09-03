# Les blocs disponibles dans le JSON

`build_docx.js` lit un fichier JSON et n'y met aucun contenu de son cru. Ce fichier décrit ce
qu'on peut lui donner.

Dans toute chaîne de texte, `**ceci**` devient du gras.

---

## Enveloppe

```json
{
  "type": "soumission",
  "numero": "2026-001",
  "date": "6 août 2026",
  "agence": {
    "nom": "S-WEB Agency",
    "lignes": ["Conception et développement web", "Gatineau", "+1 613 410-9391", "s.webagencyca@gmail.com"],
    "contact": "Soumission 2026-001"
  },
  "client": {
    "libelle": "Présentée à",
    "nom": "Clinique Paramédika",
    "lignes": ["1183, rue Saint-Louis", "Gatineau (Québec)  J8T 2L7", "819 770-8290"]
  },
  "titre": "Nouveau site web et cartes cadeaux",
  "intro": "Texte d'ouverture, avec du **gras** si utile.",
  "blocs": []
}
```

`agence.contact` apparaît dans le pied de page à côté du numéro de page.
`type` s'affiche en majuscules dans l'en-tête de chaque page.

---

## Blocs

| Bloc | Sert à |
|---|---|
| `h2` | Titre de section |
| `sub` | Ligne d'explication sous un titre |
| `para` | Paragraphe. `"gris": true` pour le mettre en secondaire |
| `note` | Petite note grise, pour une nuance ou une mise en garde |
| `puces` | Liste à puces orange |
| `lignes` | Tableau description et montant, avec entête et total optionnels |
| `encadre` | Le prix mis en avant sur fond surface |
| `paliers` | Grille comparative de forfaits |
| `etapes` | Échéancier, colonne « quand » et colonne « quoi » |
| `deuxcartes` | Deux colonnes de puces côte à côte |
| `signature` | Deux lignes de signature |
| `notes` | Lignes vierges réglées, pour écrire à la main ou au clavier |
| `cases` | Liste à cases à cocher |
| `saut` | Saut de page |
| `espace` | Espace vertical, `"hauteur"` en vingtièmes de point |

### notes et cases

Ajoutés pour les documents de travail interne, comme une préparation d'appel.

```json
{ "type": "notes", "lignes": 6 }
{ "type": "cases", "items": ["Obtenir l'accès à la fiche Google", "Confirmer le compte Square"] }
```

Une ligne de `notes` occupe environ **0,33 pouce**. Compter large: sur un document où l'on
écrit, l'espace vide est utile, et une page aérée vaut mieux qu'une page pleine.

### lignes

```json
{ "type": "lignes",
  "entete": ["Module", "Prix"],
  "items": [
    { "titre": "Cartes cadeaux électroniques",
      "desc": "Achat en ligne, branché sur **votre compte marchand**.",
      "prix": "350 $" },
    { "titre": "Sous-total", "prix": "700 $", "fill": true, "gras": true }
  ],
  "total": { "libelle": "Total ponctuel", "montant": "2 499 $" } }
```

`fill` met la ligne sur fond surface. `total` ajoute un filet épais et une ligne en serif.

### encadre

```json
{ "type": "encadre", "libelle": "SITE WEB COMPLET",
  "sous": "Consultations et séance photo comprises", "montant": "1 499 $" }
```

### paliers

```json
{ "type": "paliers",
  "colonnes": [ { "nom": "Essentiel", "prix": "49,99 $ / mois" },
                { "nom": "Croissance", "prix": "99,99 $ / mois", "reco": true },
                { "nom": "Premium", "prix": "149,99 $ / mois" } ],
  "lignes": [ { "nom": "Hébergement, domaine, SSL", "valeurs": ["oui", "oui", "oui"] },
              { "nom": "Changements de contenu", "valeurs": ["2 par mois", "3 à 5 par mois", "Illimités*"] },
              { "nom": "Appel stratégique", "valeurs": ["non", "non", "30 min par mois"] } ] }
```

`"oui"` devient une coche orange, `"non"` devient un tiret gris pâle, tout le reste s'affiche
tel quel. La colonne `reco` reçoit un fond et la mention **▲ RECOMMANDÉ**.

**Ne pas mettre de texte blanc sur ces cellules**, le fond est clair et le texte disparaît.

### etapes

```json
{ "type": "etapes", "items": [
  { "quand": "Départ", "quoi": "Contenu, accès et autorisations réunis." },
  { "quand": "Sem. 1", "quoi": "Intégration et validation." } ] }
```

La première ligne devrait presque toujours être « Départ », pour que le client comprenne que
le compteur part de sa livraison à lui.

### deuxcartes

```json
{ "type": "deuxcartes",
  "gauche": { "titre": "De notre côté", "items": ["Conception et intégration"] },
  "droite": { "titre": "De votre côté", "items": ["Vos textes et vos photos"] } }
```

### signature

```json
{ "type": "signature", "gauche": "Pour la Clinique Paramédika", "droite": "Pour S-WEB Agency" }
```

---

## Tenir dans la page

Une page Lettre avec les marges du gabarit accepte environ **9,5 pouces de contenu**. Le
générateur ne coupe pas tout seul: c'est le `saut` qui décide.

Repères mesurés sur de vrais documents:

| Bloc | Hauteur approximative |
|---|---|
| En-tête de page | 1,2 po |
| `h2` plus `sub` | 0,7 po |
| Puce | 0,25 po |
| Ligne de tableau avec description | 0,7 po |
| `encadre` | 1,0 po |
| `paliers`, 8 lignes | 4,5 po |
| `etapes`, 4 lignes | 2,5 po |
| `deuxcartes`, 6 puces | 3,2 po |
| `signature` | 1,7 po |

**Ces repères surestiment le contenu réel d'environ 40 %**, mesuré sur la 2026-010. En cas de
doute, mettre un `saut` de MOINS: le contenu qui coule d'une page à l'autre remplit mieux qu'un
bloc forcé sur sa propre page, et un `saut` juste après un `lignes` produit une page ne portant
que la ligne de total. Voir « Erreurs déjà commises » dans `SKILL.md`.
