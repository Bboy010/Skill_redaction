---
name: controle-non-regression
description: Vérifier que les nouvelles modifications d'un manuscrit ne contredisent pas, n'annulent pas et n'affaiblissent pas les demandes des reviewers précédents ni les promesses de la lettre de réponse, qu'elles sont exactes et qu'elles ne fragilisent pas l'article (sur-affirmation, contradiction avec les figures, le matériel supplémentaire ou les dépôts de données). À utiliser après une série de corrections, avant de rédiger la lettre finale, ou quand l'auteur renvoie sa propre version pour savoir ce qu'il a gardé ou refusé.
---

# Contrôle de non-régression

## Objectif
S'assurer que chaque modification **améliore** l'article sans casser ce qui avait été promis ou corrigé aux tours précédents.

## Quand l'utiliser
- Après avoir appliqué une série de corrections.
- Avant de rédiger ou de mettre à jour la lettre de réponse.
- Quand l'auteur renvoie son fichier : savoir ce qu'il a gardé, refusé ou ajouté.

## Prérequis
- La version réellement soumise au tour précédent et la version actuelle.
- Les commentaires des reviewers de **tous** les tours, mot pour mot.
- La ou les lettres de réponse précédentes (toutes leurs promesses).
- Le journal du projet (décisions verrouillées, refus de l'auteur).
- Les données brutes, pour vérifier les chiffres ajoutés.

## Étapes
1. **Lister les modifications** entre la version soumise et la version actuelle (skill comparaison-versions-et-suivi). Regroupez-les en modifications logiques : une phrase réécrite = une modification.
2. **Si l'auteur a renvoyé sa version**, classez vos propositions avec `scripts/statut_modifications.py` : gardée, refusée, autre (réécrite par l'auteur). Isolez aussi ce que l'auteur a ajouté lui-même.
3. **Pour chaque modification, poser 4 questions :**
   1. **Accord avec les reviewers.** Contredit-elle une demande passée ? Annule-t-elle une correction déjà faite ? Affaiblit-elle une précaution promise (cadrage descriptif, « putative », absence de tests statistiques) ?
   2. **Accord avec la lettre.** La lettre précédente citait-elle une phrase ou un titre de section que la modification change ?
   3. **Exactitude.** Chaque chiffre ou affirmation ajouté est-il recalculé dans les données (skill verification-des-sources) ?
   4. **Fragilité.** Nouvelle sur-affirmation ? Contradiction avec une figure, le matériel supplémentaire, la Data Summary ou un dépôt public ? Ordre des renvois cassé ?
4. **Contrôler aussi la forme** : orthographe imposée, typographie, italiques, champs Zotero intacts, ordre des citations.
5. **Donner un verdict par modification** : OK / risque / à corriger, avec la justification.
6. **Présenter le rapport** et attendre la validation avant toute correction.

## Checklist de contrôle
- [ ] Chaque modification a été comparée aux commentaires de **tous** les reviewers.
- [ ] Les phrases et titres cités dans les anciennes lettres existent toujours, ou leur changement est expliqué.
- [ ] Aucune précaution promise n'a disparu (« putative », « descriptive », « in silico »).
- [ ] Chaque chiffre ajouté est recalculé.
- [ ] Aucune contradiction avec les figures, le supplémentaire, la Data Summary ou les dépôts.
- [ ] L'ordre des renvois aux figures, tableaux et éléments supplémentaires est respecté.
- [ ] Les refus de l'auteur sont notés pour ne plus être proposés.

## Pièges fréquents (leçons apprises)
- **Renommer un titre annoncé dans la lettre précédente.** La lettre disait « a new Section 3.1 (Data processing) ». Renommer la section rendait la promesse visiblement fausse.
- **Corriger en ajoutant une définition invérifiable.** Une définition proposée (« taxa absent from the profiles… ») s'est révélée fausse au recalcul. Une correction peut être pire que l'original.
- **Faire réapparaître ce qu'un reviewer avait fait retirer.** Par exemple le mot « reservoir », ou une donnée que le reviewer jugeait non pertinente, remise en avant dans la conclusion.
- **Ne pas voir ce que l'auteur a refusé.** Après le retour de l'auteur, la lettre décrivait encore des corrections refusées. Mettez la lettre à jour.
- **Toujours identifier le fichier réellement soumis** avant de comparer (voir comparaison-versions-et-suivi).
- **Une modification de mise en forme peut passer inaperçue** : gras perdu sur un renvoi, italique ajouté par héritage.

## Livrable attendu
Un rapport `NON_REGRESSION.md` :
- en tête, ce qui est **bloquant** ;
- puis un tableau par modification : ligne, avant → après, verdict (OK / risque / à corriger), justification ;
- puis la liste des modifications gardées, refusées et ajoutées par l'auteur.

## Exemple générique
| Ligne | Avant → après | Verdict | Justification |
|---|---|---|---|
| 198 | « 3.1. Data processing » → « 3.1. Assembly » | **à corriger** | La lettre précédente annonçait ce titre exact au reviewer |
| 340 | « 12 unclassified genomes » → « 12 genomes absent from the profiles » | **à corriger** | Recalcul : un des genres est très abondant dans les profils |
| 120 | « (Table 1) » perd son gras | à corriger (cosmétique) | Style des renvois de la version soumise |
| 58 | « color » → « colour » | OK | Orthographe britannique demandée |

## Script
`scripts/statut_modifications.py` : à partir d'une liste de propositions (ancien → nouveau, en JSON), indique pour chacune si elle est **gardée**, **refusée** ou **autre** dans le fichier de l'auteur.
