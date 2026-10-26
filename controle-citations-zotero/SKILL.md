---
name: controle-citations-zotero
description: Contrôler les citations numérotées d'un manuscrit Word géré avec Zotero (numérotation continue, ordre de première citation, références orphelines ou manquantes, numéros tapés à la main, citations restées à l'ancien numéro après un Refresh, correspondance appel → bonne référence) et insérer proprement des références manquantes. À utiliser après tout ajout, déplacement ou suppression de citation, après un Refresh Zotero, ou avant toute soumission d'un manuscrit avec style numéroté (Vancouver, [1], [2]…).
---

# Contrôle des citations Zotero

## Objectif
Garantir que chaque appel [n] du texte renvoie au **bon** article de la bibliographie, et que la numérotation suit l'ordre de première citation, sans trou ni orpheline.

## Quand l'utiliser
- Après avoir ajouté, supprimé ou déplacé une phrase qui contient une citation.
- Après un Refresh Zotero.
- Quand une référence manque dans la bibliographie.
- Avant chaque soumission.

## Prérequis
- Le manuscrit .docx avec les champs Zotero actifs (pas une version « déliée » ou convertie en texte).
- Zotero et son extension Word, pour les corrections.
- `pip install python-docx`

## Étapes
1. **Fermer le document dans Word**, puis lancer `python scripts/audit_zotero.py manuscrit.docx`. Le script ne modifie rien.
2. **Lire le rapport :**
   - *numéros tapés à la main* : un « [14] » écrit au clavier n'est pas un champ Zotero et ne sera jamais renuméroté ;
   - *affiché ≠ enregistré* : le texte visible ne correspond plus aux données du champ ;
   - *appel → autre numéro* : le champ renvoie à un article qui porte un autre numéro dans la bibliographie (citation restée à l'ancien numéro) ;
   - *orphelines* : entrées de la bibliographie jamais citées ;
   - *manquantes* : numéros cités absents de la bibliographie ;
   - *ordre* : la première apparition des numéros doit être croissante.
3. **Insérer les références manquantes :**
   1. Dans Zotero, importez chaque référence par son DOI (bouton « baguette magique », *Add Item by Identifier*).
   2. Dans le .docx, repérez l'endroit exact. Si vous préparez le travail pour quelqu'un d'autre, mettez une balise **surlignée en jaune**, par exemple `[ZOTERO: Outil A]`.
   3. Dans Word, sélectionnez la balise, supprimez-la, puis faites Zotero → *Add/Edit Citation*.
4. **Faire un Refresh** (Zotero → *Refresh*). Si Zotero demande de garder une modification manuelle, refusez : vous voulez la valeur calculée par Zotero.
5. **Relancer l'audit.** S'il reste des numéros anciens, faites un **deuxième Refresh**, puis relancez l'audit.
6. **Contrôler la police de la bibliographie.** Un Refresh régénère la bibliographie avec le style Word « Bibliography ». Réglez la police de ce **style** (pas du texte sélectionné) pour qu'elle survive aux prochains Refresh.
7. **Contrôler les numéros cités hors du manuscrit** : matériel supplémentaire, lettre de réponse. Ils ne sont pas mis à jour par Zotero.
8. **Régénérer le PDF**, puis relever à nouveau les numéros de ligne (ils peuvent bouger).

## Checklist de contrôle
- [ ] 0 numéro tapé à la main.
- [ ] 0 « affiché ≠ enregistré ».
- [ ] Chaque appel renvoie à la bonne entrée (titre et DOI).
- [ ] Numérotation continue de 1 à N, sans trou.
- [ ] Ordre de première citation croissant.
- [ ] 0 orpheline, 0 manquante.
- [ ] Police de la bibliographie conforme, réglée dans le style « Bibliography ».
- [ ] Numéros cités dans le matériel supplémentaire et dans la lettre mis à jour.
- [ ] 0 balise `[ZOTERO: …]` restante, 0 surlignage.

## Pièges fréquents (leçons apprises)
- **Numéros tapés à la main.** Plusieurs outils étaient cités « [14]–[17] » au clavier. Ces numéros pointaient vers d'autres articles, et les vraies références manquaient.
- **Citations restées à l'ancien numéro après un Refresh.** Après refus de modifications suivies, plusieurs appels affichaient encore la numérotation précédente. Un deuxième Refresh les a corrigés. Contrôlez toujours après un Refresh.
- **Un Refresh peut réinitialiser la police de la bibliographie.** La police appliquée à la main disparaît. Réglez le style.
- **Les numéros de ligne changent après un Refresh.** Une balise longue remplacée par « [36] » raccourcit un paragraphe, et toutes les lignes suivantes remontent. Relevez les lignes de la lettre **après** le Refresh.
- **Balise coupée en plusieurs morceaux.** Après un enregistrement dans Word, une balise comme `[ZOTERO: …]` peut être découpée en plusieurs « runs » invisibles. Une recherche naïve ne la trouve plus en entier.
- **Matériel supplémentaire oublié.** « Tool B [42] » dans une légende supplémentaire devient faux quand la numérotation se décale.
- **Ne jamais modifier un document ouvert dans Word**, surtout pendant que Zotero est actif : les deux écritures se marchent dessus.

## Livrable attendu
Le rapport de l'audit (avant et après correction), et une phrase de conclusion : « N références, toutes citées, ordre croissant, 0 problème ».

## Exemple générique
```
Champs Zotero : 48 | références : 52 | orphelines : [20, 22] | manquantes : []
Ordre croissant : oui | Problèmes : 2
  appel → autre numéro | §2.3 | « Tool C… » affiché [18], correspond à l'entrée [20]
  appel → autre numéro | §2.3 | « Tool D… » affiché [19], correspond à l'entrée [22]
```
Action : deuxième Refresh, puis nouvel audit. Résultat : 0 problème, 0 orpheline.

## Script
`scripts/audit_zotero.py` : audit complet en lecture seule. Option `--json` pour garder une trace.
