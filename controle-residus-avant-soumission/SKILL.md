---
name: controle-residus-avant-soumission
description: Faire le dernier contrôle technique d'un manuscrit et de sa lettre avant l'envoi à la revue (modifications suivies, commentaires, texte masqué, surlignage, balises de travail, champs cassés, espaces et ponctuation, polices, ordre des renvois, métadonnées révélant un nom ou un chemin local) et établir la liste exacte des fichiers à joindre. À utiliser juste avant de soumettre ou resoumettre, ou quand on demande « est-ce que tout est prêt ? », « contrôle final », « vérifie les résidus ».
---

# Contrôle des résidus avant soumission

## Objectif
Envoyer des fichiers **propres** : rien d'oublié du travail en cours, rien qui révèle des informations privées, et les **bons** fichiers.

## Quand l'utiliser
- Juste avant l'envoi dans le système de soumission de la revue.
- Après les dernières retouches de l'auteur.

## Prérequis
- Le manuscrit final (.docx) et son PDF, le document avec suivi, la lettre de réponse (.docx et .pdf).
- Les fichiers **fermés dans Word**.
- `pip install python-docx pymupdf`

## Étapes
1. **Contrôle technique du .docx** : `python scripts/residus_docx.py manuscrit.docx --lignes lignes.txt`. Il recherche :
   - modifications suivies non acceptées, commentaires, texte masqué, surlignage, trame de fond ;
   - balises de travail (`[ZOTERO: …]`, `TODO`, `XX`, `???`, `à vérifier`) ;
   - champs incomplets ou affichant « Error! », signets ;
   - doubles espaces, espace avant une ponctuation fermante, ponctuation doublée, parenthèses non appariées ;
   - polices effectives différentes de la police attendue ;
   - langue de vérification (par exemple « fr-FR » sur une partie du texte) ;
   - ordre de première citation des figures et tableaux.
2. **Contrôle des citations** : skill controle-citations-zotero (audit complet).
3. **Contrôle des métadonnées** : `python scripts/metadonnees.py fichier1.docx fichier2.pdf …`. Il cherche l'auteur, le dernier modificateur, le titre, le modèle Word, les **chemins locaux** et les noms de compte.
4. **Nettoyer les métadonnées** dans Word : *Fichier → Informations → Inspecter le document → Propriétés du document et informations personnelles → Supprimer*. Remplacez le modèle (*Développeur → Modèle de document*) s'il pointe vers un chemin local.
5. **Contrôler la lettre** : chaque renvoi de ligne et de référence correspond au PDF final (skill reponse-aux-reviewers). Pas de reste d'une version antérieure.
6. **Contrôler la cohérence des fichiers** : chaque PDF est plus récent que son .docx, le document suivi est basé sur la version réellement soumise.
7. **Dresser la liste finale des fichiers à joindre**, avec leur date. Marquez les anciennes versions comme **obsolètes** pour ne pas les envoyer par erreur.

## Checklist de contrôle
- [ ] 0 modification suivie, 0 commentaire, 0 texte masqué, 0 surlignage.
- [ ] 0 balise de travail, 0 « Error! », champs complets.
- [ ] Typographie propre (espaces, ponctuation, parenthèses).
- [ ] Police conforme dans le corps **et** dans la bibliographie.
- [ ] Figures, tableaux et éléments supplémentaires cités dans l'ordre.
- [ ] Métadonnées : aucun nom de compte, aucun chemin local, titre correct ou vide.
- [ ] Lettre : renvois exacts, rien de périmé.
- [ ] Liste des fichiers à joindre établie, versions obsolètes signalées.

## Pièges fréquents (leçons apprises)
- **Métadonnées révélatrices.** L'auteur du fichier était le nom générique du compte de l'ordinateur du laboratoire. Le modèle Word pointait vers `C:\Users\…\Downloads\…`.
- **Titre de document hérité d'un modèle.** Le titre des propriétés était une phrase du gabarit d'une autre revue, sans rapport avec l'article.
- **Lettre générée par un script.** Auteur « python-docx », date de création fictive (2013). À vider.
- **Espace laissée par une insertion de citation** : « for clustering [12] ) ». Elle vient souvent du remplacement d'une balise.
- **Ponctuation doublée après une fusion de texte** : « *species name*. (Code 1ABC). ».
- **Langue de vérification ajoutée par Word.** Invisible dans le PDF, mais elle crée des révisions « Français » dans le document suivi.
- **Envoyer une ancienne version.** Les noms se ressemblent (`final`, `final2`, `-edit`). Vérifiez les dates et marquez les fichiers obsolètes.
- **Ne jamais écrire dans un fichier ouvert dans Word.** Le contrôle est en lecture seule ; les corrections se font dans Word, fichier par fichier, puis on recontrôle.

## Livrable attendu
Un tableau (fichier, ligne, résidu, gravité **bloquant / à corriger / cosmétique**, correction proposée), avec en tête ce qui empêche la soumission. Puis la liste finale des fichiers à joindre.

## Exemple générique
| Fichier | Ligne | Résidu | Gravité | Correction |
|---|---|---|---|---|
| manuscrit.docx | — | Auteur « PC-LABO-03 » | à corriger | Inspecteur de document → supprimer les propriétés |
| manuscrit.docx | — | Modèle `file:///C:/Users/…/gabarit.dot` | à corriger | Remplacer par Normal.dotm |
| manuscrit.docx | 143 | « [12] ) » | cosmétique | « [12]) » |
| lettre.docx | — | Auteur « python-docx » | cosmétique | Vider les propriétés |

**Fichiers à joindre :** manuscrit.docx (date), manuscrit.pdf (date), manuscrit_suivi.docx (date), lettre.pdf (date). **Ne pas envoyer :** manuscrit_v1.docx (obsolète).

## Scripts
- `scripts/residus_docx.py` : contrôle technique complet du .docx (lecture seule).
- `scripts/metadonnees.py` : métadonnées des .docx et .pdf, chemins locaux, noms de compte.
