---
name: agent-vocal
description: Monte une réceptionniste vocale IA pour un client, sur Vapi, à partir d'un gabarit unique. Un client est un formulaire de 28 champs, jamais un projet à refaire. Produit le prompt, l'assistant Vapi, la page de démo avec widget web, et la passe de tests. Utiliser quand il dit "monte un agent vocal pour ce client", "fais une réceptionniste IA", "réplique l'agent de ClimPure pour X", "ajoute un client à l'agent vocal", ou donne un métier et une entreprise en demandant un agent qui répond au téléphone.
---

# Agent vocal, réceptionniste IA

Monte une réceptionniste vocale qui répond vingt-quatre heures sur vingt-quatre, capte les appels que l'équipe manque, qualifie, et laisse un dossier propre.

**La règle qui décide de tout: un client est un formulaire, pas un projet.** Un seul `prompt-gabarit.md` pour tous. Ce qui change vit dans `clients/<id>.json`. Si un client semble exiger de modifier le gabarit, c'est qu'il manque un champ à sa fiche: ajoute le champ. Le jour où il existe deux gabarits, la marge est morte.

Mesuré sur deux métiers très différents, nettoyage de conduits et toiture: environ soixante-quinze pour cent du prompt est identique d'un client à l'autre.

## Ce qu'il faut avant de commencer

Un fichier `cles.local.txt` à la racine du dossier de travail, jamais partagé, jamais téléversé:

```
VAPI_API_KEY=
VAPI_PUBLIC_KEY=
```

La privée sert à créer l'assistant, la publique au widget web. Si elles manquent, demande-les et arrête-toi là.

## Le déroulé

**1. L'appel de cadrage.** Les vingt-huit champs de `clients/FICHE-VIERGE.json` sont exactement les questions à poser au propriétaire. Ne devine jamais: un service inventé ou une zone approximative se paie au premier vrai appel. Si le client a un site, lis-le d'abord et pré-remplis, puis fais confirmer.

Les champs qui font la différence entre un agent correct et un agent utile:

- `HORS_SERVICE`: ce que l'entreprise **ne** fait pas. Sans ça, l'agent accepte des ménages de cuisine chez un nettoyeur de conduits.
- `SYMPTOMES`: la table symptôme vers service. C'est ce qui rend l'agent intelligent au lieu d'être un formulaire parlant. La plupart des gens décrivent un problème, pas un service.
- `URGENCES`: ce qui compte comme urgence dans ce métier, et ce que l'agent fait alors.
- `PRIX_PUBLICS`: si un prix est affiché sur leur site, l'agent peut le citer, mais **avec le cadrage exact du site**. Si le site dit que ce sont des moyennes de marché et non ses prix, l'agent doit le dire aussi, sinon il engage le client sur un chiffre qui n'est pas le sien.

**2. Construire.**

```bash
python gabarit/monter-client.py <id>
```

Le script refuse de bâtir s'il manque un champ. Sortie dans `gabarit/sorties/<id>/`: le prompt lisible, la config complète, et un patch sans la voix.

**3. Relire à voix haute.** C'est la seule étape qui demande un cerveau. Lis `sorties/<id>/prompt.md` en entier. Tu cherches: un service inventé, une promesse de date, un ton qui ne ressemble pas au métier.

**4. Pousser.**

```bash
python gabarit/monter-client.py <id> --pousser
```

Crée l'assistant, ou le met à jour s'il en existe déjà un. **Il ne touche jamais à la voix ni au fond sonore**, pour ne pas écraser un réglage fait à la main dans le tableau de bord. Colle l'identifiant retourné dans la fiche, champ `vapi.assistantId`.

**5. Tester.** `gabarit/tester-agent.py` fait passer quinze scénarios par écrit et vérifie automatiquement les règles de forme. Voir la section Tests plus bas.

**6. La démo client.** `page/app-client.html` est le livrable qu'on envoie au propriétaire. Ce n'est pas une brochure avec un aperçu de tableau de bord: **c'est le tableau de bord qu'il aura s'il devient client**, avec le reste de l'information rangée dans ses propres écrans.

Six vues, une seule page, la navigation de gauche les commute:

| Vue | Ce qu'elle porte |
|---|---|
| Tableau de bord | la valeur rattrapée, les compteurs, le graphique, la qualité des leads, les motifs d'écart |
| Appels | le journal complet, plus une transcription d'appel en entier avec les notes qui expliquent l'agent |
| Rappels | la file des gens à rappeler |
| L'agent | ce qu'il fait et ce qu'il refuse, et le bouton pour lui parler tout de suite |
| Rapports | le mois résumé, et l'avis sur l'enregistrement des appels |
| Réglages | ce qui pilote les chiffres, et tout ce que l'agent sait de l'entreprise |

Le fait de ranger l'argumentaire dans des écrans de produit plutôt que dans des sections de brochure change la lecture: le propriétaire ne lit pas une promesse, il utilise son outil.

**Une seule ligne à changer pour habiller un autre client:** la variable `--h`, la teinte de son logo en OKLCH. Tout le thème en découle, fonds, cartes, texte, graphiques. Pour convertir un code hexadécimal:

```python
import math
def teinte(hexstr):
    r,g,b=[int(hexstr[i:i+2],16)/255 for i in (1,3,5)]
    def lin(v): return v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4
    r,g,b=lin(r),lin(g),lin(b)
    l=(0.4122214708*r+0.5363325363*g+0.0514459929*b)**(1/3)
    m=(0.2119034982*r+0.6806995451*g+0.1073969566*b)**(1/3)
    s=(0.0883024619*r+0.2817188376*g+0.6299787005*b)**(1/3)
    A=1.9779984951*l-2.4285922050*m+0.4505937099*s
    B=0.0259040371*l+0.7827717662*m-0.8086757660*s
    h=math.degrees(math.atan2(B,A))
    return round(h+360 if h<0 else h)
```

ClimPure donne deux cent trente-six. Le sélecteur de couleurs de la maquette d'origine a été retiré: un client ne choisit pas sa teinte, elle vient de son logo.

**La règle qui compte plus que l'apparence: la démo ne montre que ce que l'agent produit vraiment.** La maquette d'origine affichait des rendez-vous pris et confirmés. L'agent a interdiction de fixer un rendez-vous: cette carte aurait menti à chaque ligne. Remplacée par la file des rappels, qui est ce que l'agent laisse. Avant de garder un écran, vérifie que le prompt produit la donnée.

Les chiffres doivent aussi se tenir entre eux. Total des appels, somme du graphique, somme du beigne, somme des motifs d'écart: un seul jeu cohérent. Un tableau de bord dont les colonnes se contredisent se fait démonter en réunion.

**Ce qu'il faut adapter par client**, en plus de la teinte: le nom et le propriétaire, les services et le territoire dans Réglages, le journal d'appels et la transcription avec le vocabulaire du métier, les chiffres du mois, et le découpage horaire. Ce dernier n'est pas cosmétique: un couvreur ouvre du lundi au vendredi et sa fin de semaine est vide, ClimPure ouvre sept jours et son creux est la nuit.

Trois détails techniques qui coûtent une heure si on les découvre en direct. Le fichier a besoin de sa balise `charset`, absente de la maquette d'origine, sinon tous les accents cassent. Les compteurs animés ont un `setTimeout` de secours qui écrit la valeur finale, parce qu'un navigateur qui bride les images par seconde laisse le chiffre coincé à mi-chemin pendant que l'arc est déjà plein. Et le panneau du widget vocal est figé à 448 pixels de large: la routine qui le ramène dans l'écran et traduit ses textes anglais est incluse dans le fichier, garde-la.

## La config qui marche

Vérifiée contre le schéma officiel de Vapi. Plusieurs champs qu'on trouve dans les vieux tutoriels n'existent plus.

| Réglage | Valeur | Pourquoi |
|---|---|---|
| Modèle | `gemini-3.5-flash`, temp 0.4, max 150 tokens | rapide, et 150 tokens force la brièveté |
| Transcription | Deepgram `nova-3`, langue `multi` | bascule français-anglais sans reconfiguration |
| Endpointing | `smartEndpointingPlan` provider `vapi` | `livekit` ne gère que l'anglais |
| Interruptions | `numWords` à 1, plus `acknowledgementPhrases` | à zéro, la liste d'acquiescements ne s'applique jamais |
| Fond sonore | `office` | le silence total est le plus gros indice qu'on parle à une machine |
| Enregistrement | `artifactPlan.recordingEnabled`, format mp3 | `recordingEnabled` à la racine n'existe plus |
| Fin d'appel | outil `endCall` dans `model.tools` | `endCallFunctionEnabled` a été retiré |

**N'existent plus, ne les cherche pas:** `backchannelingEnabled`, `fillerInjectionEnabled`, `silenceTimeoutSeconds`. Le backchanneling est remplacé par `stopSpeakingPlan.acknowledgementPhrases`, dont la liste par défaut est en anglais seulement: il faut fournir la sienne en français.

## Les pièges qui coûtent une heure chacun

**Le tableau de bord Vapi garde un brouillon.** Les modifications faites dans l'interface ne sont pas actives tant qu'on n'a pas cliqué sur Publish, et l'API renvoie l'ancienne version en attendant. Pire: publier un vieux brouillon écrase un patch envoyé par API entre-temps. Si le client a touché à l'interface, fais-lui publier d'abord, puis patche.

**Le canal texte de Vapi exige une carte au dossier.** L'endpoint `/chat` renvoie 402 même avec des crédits. Le banc d'essai a donc une voie Gemini directe, qui teste le même prompt avec le même modèle sans passer par Vapi.

**Un prompt qui grossit rend l'agent plus bête, pas plus fiable.** Constaté: en passant de sept mille à quatorze mille caractères pour couvrir des cas rares, l'agent est devenu moins bon sur ce que l'entreprise fait vraiment. Il applique des règles au lieu d'écouter. Vise neuf mille caractères. Si tu dois choisir entre une règle de plus et de la clarté, choisis la clarté.

**Le refus doit rester étroit.** « Tout ce qui n'est pas dans la liste se refuse » rend l'agent inutilisable. La bonne formulation: ce qui est manifestement à côté se refuse, le doute profite au client et l'équipe tranche. Refuser un vrai client coûte plus cher que trier un dossier de trop.

**Un nom de lieu n'est pas un changement de langue.** Sans règle explicite, « je suis à Ottawa » fait basculer l'agent en anglais au milieu d'une conversation française. Le champ `LIEUX_NEUTRES` liste les noms de la région.

**Le panneau du widget web fait 448 pixels de large, en dur.** Il déborde de tout téléphone. La page de référence contient la routine JavaScript qui le ramène dans l'écran et traduit ses textes, qui sont en anglais et que les attributs du widget ne couvrent pas.

**Le cache du navigateur ment.** Après un changement de page, si rien ne bouge, recharge avec un paramètre différent avant de conclure que c'est cassé.

## Les tests

```bash
python gabarit/tester-agent.py
```

Quinze scénarios en conversation multi-tours, avec vérification automatique: pas plus de deux phrases, pas plus d'une question, aucun chiffre écrit en chiffres, aucun montant, aucune énumération, et refus explicite sur les scénarios hors service.

Les scénarios sont écrits pour ClimPure. Adapte-les au métier du client avant de lancer, surtout les trois hors service.

Ce qu'aucun test écrit ne peut trancher, et qui demande un vrai appel: la détection de langue sur les premiers mots, la relecture d'un numéro de téléphone par la voix, et l'accent sur une ligne téléphonique en huit kilohertz, qui est bien moins flatteuse qu'un navigateur.

## Ce que l'agent ne doit jamais faire

Donner un prix qui n'est pas publié. Promettre une date, une heure ou un délai de rappel. Poser un diagnostic. Dire qu'il est fermé. Inventer un service. Prétendre être humain: si on lui demande s'il est un robot, il répond oui en une phrase, sans s'excuser, et il continue.

## Rappel légal

L'enregistrement des appels touche la loi 25 au Québec. Pour une démonstration entre nous, aucun enjeu. Le jour où ça passe sur la vraie ligne d'un client, il faut un avis en début d'appel. À régler avant la mise en production, pas après.
