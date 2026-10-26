---
name: legende-vs-figure
description: Comparer chaque phrase d'une légende de figure avec ce que l'image montre réellement (couleurs, symboles, panneaux, nombre d'éléments, axes, positions), et proposer une légende exacte. À utiliser quand on rédige, fusionne ou corrige une légende, quand un reviewer dit qu'une légende est incomplète ou inexacte, ou avant de soumettre un article avec figures.
---

# Légende contre figure

## Objectif
Une légende doit décrire **ce que l'on voit**, pas ce que l'on avait l'intention de montrer.
Le lecteur doit pouvoir comprendre la figure sans lire le texte : source des données, unités, couleurs, symboles.

## Quand l'utiliser
- Vous écrivez ou modifiez une légende.
- Un reviewer demande de déplacer du texte dans une légende, ou dit qu'une légende ne correspond pas.
- Une figure a été régénérée, mais la légende date de l'ancienne version.

## Prérequis
- L'image de la figure en **pleine résolution** (extraite du .docx, pas une capture du PDF réduit).
- Le texte de la légende.
- Si possible, les données ou le fichier source de la figure (alignement, tableau, script de tracé).

## Étapes
1. **Extraire l'image** avec `scripts/extraire_figures.py`. Ouvrez-la en grand.
2. **Découper la légende en affirmations.** Une phrase = une ou plusieurs affirmations. Exemple : « Orange stars mark the catalytic triad (Ser1, Asp2, His3) » donne 2 affirmations : des étoiles orange, et 3 résidus nommés.
3. **Vérifier chaque affirmation sur l'image :**
   - les couleurs (rouge, jaune, cadre bleu) ;
   - les symboles et leur **nombre** (3 étoiles ? 4 cercles ?) ;
   - leur **position** exacte (sur quel résidu, quelle colonne, quel échantillon) ;
   - les panneaux (a), (b), (c) et leur ordre ;
   - les axes, les unités, l'échelle de couleurs, les libellés de la légende intégrée ;
   - les éléments décrits mais absents (structure secondaire, barres d'erreur…).
4. **Vérifier sur les données** quand c'est possible : par exemple, retrouver dans l'alignement le résidu sous chaque symbole.
5. **Vérifier les termes** : la légende dit « reference », l'image dit « Control ». Les deux doivent concorder avec le texte.
6. **Rédiger la légende corrigée.** Gardez le titre en gras. Retirez ce qui n'est pas visible. Ne nommez pas d'éléments que vous n'avez pas pu vérifier.
7. **Signaler séparément les défauts de l'image** : lettres rognées, symbole mal placé, fond noir, faute dans la légende intégrée. Ils se corrigent dans le logiciel d'origine, pas dans le .docx.

## Checklist de contrôle
- [ ] Chaque phrase de la légende correspond à un élément visible.
- [ ] Le nombre de symboles cités = le nombre de symboles visibles.
- [ ] Les couleurs citées = les couleurs affichées.
- [ ] Les termes de l'image (légende intégrée, axes) concordent avec ceux de la légende et du texte.
- [ ] La source des données (lectures, génomes, catalogue) et les unités sont indiquées.
- [ ] Les outils sont cités par une référence numérotée, pas par une URL.
- [ ] La légende forme **un seul paragraphe**, sans texte resté à part sous la figure.
- [ ] Orthographe cohérente (par exemple « colour » et « grey » en anglais britannique).

## Pièges fréquents (leçons apprises)
- **Décrire l'intention, pas l'image.** « Secondary-structure elements are shown above the sequence » alors qu'aucun n'apparaît.
- **Mauvaise couleur.** « Similar residues highlighted in yellow » alors qu'ils sont en lettres rouges dans des cadres bleus.
- **Liste qui ne colle pas.** Trois résidus nommés pour quatre cercles dessinés, dont deux mal placés. Sans possibilité de vérifier, décrivez sans lister.
- **Texte orphelin.** Une partie de la légende reste un paragraphe séparé sous la figure. Un reviewer le relève, même après une révision.
- **Une modification de légende peut changer l'ordre des renvois.** Citer « Figure 4 » dans les Méthodes avant la Figure 2 casse l'ordre de citation.
- **Image extraite trop petite.** Les petits symboles sont mal positionnés ou illisibles. Travaillez sur l'image d'origine.

## Livrable attendu
Un tableau par figure :

| Affirmation de la légende | Ce que montre l'image | Verdict | Correction proposée |
|---|---|---|---|

Puis la légende corrigée complète, et la liste des défauts de l'image à corriger à la source.

## Exemple générique
- Légende : « Red bars show taxa enriched at site A; the dashed line marks p < 0.05. »
- Image : barres rouges et bleues ; la ligne pointillée est à LFC = 2. L'axe des y est « mean abundance (%) ». Il n'y a aucune p-value.
- Verdict : la ligne pointillée est mal décrite, et la notion de « p < 0.05 » est fausse (aucun test statistique).
- Correction : « Red bars show taxa with a log2 fold change above 2 (dashed line), a descriptive threshold; no statistical test was applied. »

## Script
`scripts/extraire_figures.py` : extrait toutes les images d'un .docx en pleine résolution, avec le début de la légende la plus proche, pour les ouvrir une à une.
