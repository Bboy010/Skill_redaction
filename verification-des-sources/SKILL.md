---
name: verification-des-sources
description: Recalculer chaque chiffre et vérifier chaque affirmation d'un manuscrit à partir des données brutes (tableaux, sorties d'outils, fichiers de versions, références citées) au lieu de reprendre un texte antérieur, et signaler clairement ce qui n'est pas vérifiable. À utiliser avant d'écrire ou de corriger un résultat chiffré, une définition de métrique, une version de logiciel, ou quand un reviewer demande « d'où vient ce chiffre ? ».
---

# Vérification des sources

## Objectif
Chaque chiffre du manuscrit doit pouvoir être **refait** à partir d'un fichier de données, avec une règle qu'on sait énoncer.
Si on ne peut pas le refaire, on le dit. On n'invente pas de définition pour qu'un chiffre « tombe juste ».

## Quand l'utiliser
- Avant d'ajouter ou de modifier un chiffre, un pourcentage ou une moyenne.
- Quand un reviewer demande de définir une métrique (« units? », « mean per what? »).
- Quand vous reprenez une phrase d'une ancienne version ou d'une ancienne lettre.
- Avant d'écrire une version de logiciel ou un paramètre dans les Méthodes.

## Prérequis
- Les données brutes : tableaux (TSV, CSV, XLSX), sorties d'outils, scripts d'analyse.
- Le fichier qui liste les versions des logiciels (ou les logs du pipeline).
- Les références citées (titre, DOI) pour les affirmations bibliographiques.

## Étapes
1. **Lister les affirmations à vérifier.** Pour chaque phrase : le chiffre, ce qu'il est censé mesurer, la section et la ligne.
2. **Trouver la source.** Quel fichier, quelle colonne, quel filtre ? Si le script d'analyse existe, lisez-le : il donne souvent la vraie règle (par exemple « filtre : valeur manquante »).
3. **Recalculer.** Utilisez `scripts/agreger_tableau.py` ou votre propre code. Notez la commande exacte : elle doit être reproductible.
4. **Comparer avec le texte.** Le chiffre est-il identique ? L'unité est-elle la même (par génome, par échantillon, par site) ? Le niveau taxonomique est-il le bon (genre ou espèce) ?
5. **Contrôler avec une deuxième source** quand c'est possible : par exemple un tableau dérivé, puis la sortie brute de l'outil.
6. **Vérifier la cohérence partout.** Le même chiffre peut apparaître dans le résumé, les résultats, la discussion, une légende, un tableau et la lettre.
7. **Classer chaque affirmation** : vérifiée / corrigée (avec la nouvelle valeur) / **non vérifiable** (avec la raison).
8. **Faire valider par l'auteur** avant de modifier le texte. Proposez la formulation, ne l'imposez pas.

## Checklist de contrôle
- [ ] Chaque chiffre a une source (fichier + colonne + filtre) et une commande de recalcul.
- [ ] L'unité de la métrique est écrite dans le texte (« per genome », « per sample »).
- [ ] Les doubles comptages sont exclus (par exemple, une ligne « genre » et une ligne « espèce » additionnées).
- [ ] Les versions de logiciels viennent d'un fichier de versions ou d'un log, pas de la mémoire.
- [ ] Le même chiffre est identique dans toutes les sections et dans la lettre.
- [ ] Les affirmations non vérifiables sont listées et signalées à l'auteur.

## Pièges fréquents (leçons apprises)
- **Ne jamais réutiliser une formulation proposée plus tôt sans la revérifier.** Une définition proposée lors d'une passe précédente (« taxa absent from the profiles ») s'est révélée fausse au recalcul : le genre était en fait très abondant.
- **Une colonne remplie à la main n'est pas une règle.** Un sous-ensemble défini par « valeur manquante dans le tableur » ne peut pas être décrit proprement si les valeurs ont été saisies sans critère. Proposez un critère reproductible, ou supprimez le chiffre.
- **Mauvais niveau.** Un texte dit « genus-level » alors que la valeur est celle d'une **espèce**. Vérifiez la ligne exacte de la table.
- **Double comptage.** Une valeur exactement égale à 2 × une autre est suspecte : deux lignes (agrégée et détaillée) ont peut-être été additionnées.
- **Métrique décrite de mémoire.** « Moyenne par compartiment » au lieu de « moyenne par génome » : l'erreur vient de la lettre, pas des données.
- **Version de logiciel inventée.** Si la version n'est pas dans les logs, écrivez « version non confirmée » dans vos notes, pas un numéro plausible.
- **Moyenne sur qui ?** Une moyenne « par génome » change selon qu'on compte les génomes sans le gène (valeur 0) ou seulement ceux qui le portent. Testez les deux (option `--manquant-zero`) et écrivez celle qui reproduit le texte.
- **Le chiffre juste, l'étiquette fausse.** « 500 hydrolase genes » quand ce sont des glycoside hydrolases : le nombre est exact, mais le mot change le sens.

## Livrable attendu
Un tableau :

| Ligne | Affirmation | Source et commande | Valeur recalculée | Verdict | Proposition |
|---|---|---|---|---|---|

## Exemple générique
- Texte : « Water samples had more esterase genes than sediment samples (4.2 versus 3.1). »
- Recalcul :
  `python agreger_tableau.py genes_par_genome.tsv --groupe compartiment --valeur CE --operation mean`
  → eau : 4.2 (n = 30 génomes) ; sédiment : 3.1 (n = 8 génomes).
- Verdict : chiffre exact, mais l'unité manque. C'est une moyenne **par génome**.
- Proposition : « Genomes recovered from water samples carried on average more esterase genes per genome (4.2, n = 30) than those from sediment samples (3.1, n = 8). »

## Script
`scripts/agreger_tableau.py` : somme, moyenne, compte ou médiane d'une colonne, par groupe, avec filtres. Lit TSV, CSV et XLSX. Format « long » (une ligne par élément × catégorie) : options `--pivot-cle` et `--pivot-valeur`.
