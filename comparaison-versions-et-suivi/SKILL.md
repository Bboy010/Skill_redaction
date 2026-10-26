---
name: comparaison-versions-et-suivi
description: Comparer deux versions d'un manuscrit Word (texte, mise en forme, champs Zotero, images, mise en page) après avoir identifié le fichier réellement soumis, puis produire le PDF et le document avec suivi des modifications par rapport à cette version soumise, sans toucher au fichier de l'auteur. À utiliser quand plusieurs versions d'un manuscrit circulent, quand la revue demande un « marked-up » ou « tracked changes » manuscript, ou avant de reprendre un travail sur un fichier dont on n'est pas sûr.
---

# Comparaison de versions et document avec suivi

## Objectif
1. Savoir **quel fichier a vraiment été soumis**, et ce qui le distingue des autres versions.
2. Produire un document avec suivi des modifications qui montre **uniquement** les vrais changements depuis cette version.

## Quand l'utiliser
- Plusieurs fichiers portent des noms proches (`final`, `final2`, `soumis`, `-edit`…).
- La revue demande une version avec suivi des modifications.
- Vous reprenez un travail : avant toute modification, il faut savoir sur quelle base on part.
- L'auteur vous renvoie son propre fichier : il faut savoir ce qu'il a gardé, refusé ou ajouté.

## Prérequis
- Les fichiers à comparer, **fermés dans Word**.
- `pip install python-docx`
- Pour le document suivi automatique : Microsoft Word sous Windows (script PowerShell). Sinon : Word ou LibreOffice → *Comparer les documents*, à la main.

## Étapes
1. **Identifier le fichier soumis.** Regardez le dossier d'envoi, les dates, les e-mails de confirmation. En cas de doute, demandez à l'auteur. Écrivez la réponse dans le journal de projet.
2. **Comparer le contenu** : `python scripts/comparer_docx.py ancien.docx nouveau.docx`. Le rapport donne :
   - le texte : paragraphes ajoutés, supprimés, modifiés (au mot près) ;
   - la mise en forme visible : gras, italique, police effective ;
   - les champs : nombre, contenu, numéros affichés ;
   - les images : empreinte de chaque image (une image remplacée se voit même si sa taille est identique) ;
   - les marges et la numérotation des lignes.
3. **Expliquer chaque différence.** Pour chacune : voulue ou non ? qui l'a faite ? Classez-les en *gardées / refusées / ajoutées par l'auteur*.
4. **Choisir la base.** Si le fichier soumis contient des améliorations absentes de votre version de travail, refaites vos corrections **sur le fichier soumis**, plutôt que l'inverse.
5. **Produire le PDF et le document suivi** : `scripts/word_comparer.ps1` (Word en lecture seule). La comparaison se fait toujours contre le fichier **réellement soumis**.
6. **Vérifier que le fichier de l'auteur n'a pas bougé** : même empreinte avant et après. Le script l'affiche.
7. **Relire le document suivi.** Repérez les révisions de « mise en forme » inattendues, par exemple une langue de vérification ajoutée par Word.

## Checklist de contrôle
- [ ] Le fichier réellement soumis est identifié et noté dans le journal.
- [ ] Chaque différence entre versions est expliquée.
- [ ] Le document suivi compare **la version soumise** → **la version finale**.
- [ ] L'empreinte du fichier de l'auteur est inchangée.
- [ ] Le PDF est plus récent que le .docx dont il provient.
- [ ] Les révisions de mise en forme inattendues sont expliquées.
- [ ] Les métadonnées du document suivi sont propres (voir le skill controle-residus-avant-soumission).

## Pièges fréquents (leçons apprises)
- **Toujours identifier le fichier réellement soumis avant de comparer.** Le fichier pris pour base datait de deux jours avant la soumission. La vraie version contenait du gras, des polices harmonisées et une image remplacée. Sans comparaison, la révision les aurait annulés sans le dire.
- **Des empreintes différentes ne veulent pas dire des textes différents.** Comparez le contenu, pas seulement le fichier.
- **Comparer contre une mauvaise base** fait apparaître de faux changements (polices, images) dans le document suivi. L'éditeur les verra.
- **Word modifie le fichier qu'il enregistre** : langue de vérification (« Français »), découpage du texte, identifiants Zotero. Ces changements apparaissent comme des révisions de mise en forme.
- **Ne jamais écrire dans un fichier ouvert dans Word.** Ouvrez-le en lecture seule pour exporter, ou fermez-le.
- **Un PDF plus ancien que le .docx est faux.** Régénérez-le après chaque modification.

## Livrable attendu
- Un rapport de comparaison : identique / différent, avec la liste des différences classées.
- Le PDF de la version finale et le document avec suivi, datés et nommés clairement.
- Une note dans le journal : « base = [fichier soumis], suivi généré le [date] ».

## Exemple générique
```
python comparer_docx.py soumis/Manuscript.docx travail/Manuscript_v2.docx
== paragraphes : 210 vs 210 | différences de texte : 0
== champs identiques : oui | images identiques : NON (image n°7 différente)
== mise en forme : 4 passages en gras seulement dans la version soumise
```
Conclusion : la version de travail est périmée. On refait les corrections sur `soumis/Manuscript.docx`.

## Scripts
- `scripts/comparer_docx.py` : comparaison détaillée en lecture seule (texte, forme, champs, images).
- `scripts/word_comparer.ps1` : export PDF et document avec suivi, par Word, en lecture seule, avec contrôle d'empreinte.
