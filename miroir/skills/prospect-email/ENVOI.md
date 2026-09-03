# Les regles d'envoi

A lire avant chaque envoi, chaque fois, meme pour un seul prospect.

---

## L'interrupteur

```
MODE: auto
```

Trois valeurs possibles, ce fichier fait foi:

| Valeur | Ce qui se passe |
|---|---|
| `auto` | le courriel part tout seul, sans demander. C'est son choix du 2026-08-19 |
| `brouillon` | un brouillon Gmail est cree, rien ne part. A utiliser pour tester un gabarit |
| `arret` | rien n'est envoye ni redige. Les images sont quand meme produites |

**Changer une seule valeur ici suffit a couper le robinet.** Aucune autre modification
n'est necessaire nulle part.

---

## Les coordonnees, obligatoires

La Loi canadienne anti-pourriel exige que tout courriel commercial non sollicite porte
l'identite de l'expediteur, une adresse postale valide et un moyen de se desabonner.

```
EXPEDITEUR: Souleman Baba, S-WEB Agency
COURRIEL: babaeyasouleman@gmail.com
TELEPHONE: <A REMPLIR>
ADRESSE POSTALE: <A REMPLIR>
```

**Tant que `TELEPHONE` ou `ADRESSE POSTALE` vaut `<A REMPLIR>`, le mode bascule de force
sur `brouillon`.** Ce n'est pas une precaution excessive: une plainte LCAP se regle en
milliers de dollars, et l'adresse manquante est exactement ce qui est reproche.

---

## Les plafonds

| | |
|---|---|
| Par execution de la routine | **3** prospects |
| Par jour, toutes sources confondues | **6** premiers contacts |
| Par semaine | **12** premiers contacts |
| Relances | 1 par prospect, jamais 2 |

Une adresse Gmail ordinaire qui passe de 0 a 40 courriels froids par jour se fait limiter
en une semaine, et il perd la boite qui recoit aussi ses clients. Six par jour reste
sous le radar et suffit largement: son objectif est 4 contrats par mois, pas 400 envois.

**Fenetre d'envoi: entre 8 h et 20 h, heure de l'Est, du lundi au vendredi.** Aucun envoi
la fin de semaine ni la nuit. Un commerce qui recoit un courriel commercial a 3 h du matin
sait qu'il vient d'un robot.

---

## La liste de suppression

Trois fichiers dans `C:\Users\Administrator\OneDrive\Bureau\Prospection\`, verifies dans
cet ordre avant chaque envoi. `scripts/lot.py` le fait deja, mais la verification reste
due meme pour un prospect donne a la main.

| Fichier | Ce qu'il contient |
|---|---|
| `ENVOYES.tsv` | tout ce qui est deja parti. Une adresse ici ne recoit jamais un deuxieme premier contact |
| `NE-PAS-CONTACTER.txt` | les STOP, les refus, les clients actuels, les concurrents. Une adresse ou un domaine par ligne |
| `FILE-ATTENTE.tsv` | la file. Une ligne marquee `IDENTITE`, `SAUTE` ou `ENVOYE` ne repart pas |

**Une reponse contenant STOP, UNSUBSCRIBE, DESABONNER ou "ne plus me contacter" est
ajoutee a `NE-PAS-CONTACTER.txt` le jour meme.**

---

## Ce qui fait sauter un prospect, sans discuter

Chacune de ces conditions arrete le traitement de la fiche. On note la raison dans la file
et on passe a la suivante. Aucune ne se contourne.

1. Le numero de telephone dans Google renvoie un autre nom d'entreprise
2. La fiche Google dit "ferme definitivement"
3. Aucune adresse courriel trouvee **sur leur site ou leur fiche Google**. Une adresse
   devinee, du type `info@`, ne s'envoie pas
4. L'adresse ou son domaine figure dans `NE-PAS-CONTACTER.txt`
5. L'adresse figure deja dans `ENVOYES.tsv`
6. C'est une franchise, une chaine, ou un site refait dans les deux dernieres annees
7. L'image sort avec un ecart-type sous 12, ou elle a l'air cassee a l'oeil
8. Le nom du decideur est introuvable. **On ecrit a une personne, pas a "Bonjour"**

Le point 8 se contourne une seule fois: si le commerce porte le nom du proprietaire,
Barbier Gatineau inc. par exemple, le nom du commerce fait office de nom.

---

## Ce qui ne s'automatise jamais

Repris de son processus, section 10. La routine ne touche a aucun de ces points:

- l'appel et le Meet
- l'annonce du prix
- la reponse a un prospect qui repond au courriel. **Une reponse humaine se lit et se
  traite a la main**, la routine ne repond jamais a un fil en cours
- la decision d'envoyer une soumission

Une reponse arrive dans sa boite, elle y reste. La routine ne lit pas ses courriels
entrants, sauf pour une chose et une seule: relever les STOP.
