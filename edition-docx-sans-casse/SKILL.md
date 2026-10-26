---
name: edition-docx-sans-casse
description: Modifier le texte d'un manuscrit Word (.docx) sans casser la mise en forme, les italiques, le gras ni les champs Zotero, en travaillant sur une copie sauvegardée et en vérifiant le résultat après chaque modification. À utiliser dès qu'on doit appliquer des corrections validées dans un .docx par programme ou en série, remplacer une phrase, fusionner des paragraphes ou corriger un manuscrit qui contient des citations Zotero.
---

# Édition d'un .docx sans casse

## Objectif
Appliquer des corrections **validées** dans un .docx, en gardant intacts : polices, italiques des noms latins, gras des renvois, champs Zotero, images.
Chaque modification doit être traçable, reproductible et réversible.

## Quand l'utiliser
- Vous avez une liste de corrections validées par l'auteur.
- Vous devez modifier un manuscrit qui contient des citations Zotero.
- Vous devez refaire les mêmes corrections sur une autre version du fichier.

## Prérequis
- La liste des corrections **validées** (pas des propositions).
- Le fichier de référence (la version de l'auteur), **fermé dans Word**.
- `pip install python-docx`

## Étapes
1. **Sauvegarder.** Copiez le fichier (`.backup_avant_X.docx`) et travaillez sur une **copie de travail**. Notez son empreinte (hash) avant modification.
2. **Écrire les corrections dans un fichier JSON** (voir l'exemple). Chaque correction donne : le texte exact actuel (`ancien`), le nouveau texte, et le nombre d'occurrences attendu (`n`). Le texte exact se copie depuis le .docx, pas depuis le PDF (les césures du PDF trompent).
3. **Lancer en simulation** : `python scripts/remplacer_texte.py copie.docx corrections.json --simulation`. Le script vérifie que chaque `ancien` est trouvé exactement `n` fois, sans rien écrire.
4. **Appliquer** : relancez sans `--simulation`. Le script écrit **tout ou rien** : si une seule correction échoue, le fichier n'est pas touché.
5. **Vérifier l'intégrité** : `python scripts/verifier_integrite.py avant.docx copie.docx`. Les champs Zotero, les images et la bibliographie doivent être identiques, et seuls les paragraphes prévus doivent avoir changé.
6. **Vérifier la mise en forme** des passages modifiés : italique, gras, police. Regardez le PDF régénéré.
7. **Remettre la copie à l'auteur.** Ne remplacez jamais sa version sans son accord.

## Format du fichier de corrections
```json
[
  {"ancien": "the bar color", "nouveau": "the bar colour", "n": 1},
  {"ancien": "(Table 1).", "segments": [["(", null], ["Table 1", "gras"], [").", "normal"]], "n": 1},
  {"ancien": "Tool A [12]", "nouveau": "Tool A [ZOTERO: Tool A]", "surligner": true, "n": 1}
]
```
- `segments` : pour imposer la mise en forme de chaque morceau (`gras`, `italique`, `normal`, ou `null` pour garder celle d'origine).
- `surligner` : surligne le nouveau texte en jaune (balises de travail).

## Checklist de contrôle
- [ ] Sauvegarde faite, empreinte notée.
- [ ] Le fichier n'était pas ouvert dans Word.
- [ ] La simulation trouve chaque correction le bon nombre de fois.
- [ ] Champs Zotero : même nombre avant et après, mêmes numéros affichés (sauf renumérotation voulue).
- [ ] Images : même nombre, mêmes empreintes.
- [ ] Italiques et gras des passages modifiés contrôlés.
- [ ] PDF régénéré et relu aux endroits modifiés.

## Pièges fréquents (leçons apprises)
- **Une modification peut hériter de l'italique ou du gras du mot voisin.** En remplaçant « exemplaris (4.0%) », le nouveau « (4.0% each) » est devenu italique comme le nom d'espèce *Bacillus exemplaris* (fictif). Ciblez le plus petit texte possible (« (4.0%), and »), ou imposez la mise en forme avec `segments`.
- **À l'inverse, on peut perdre un gras.** Réécrire une phrase entière a fait perdre le gras de « Table 1 ». Utilisez `segments` pour le rétablir.
- **Boucle infinie.** Si le nouveau texte contient l'ancien (seul le gras change), un remplacement naïf en boucle ne s'arrête jamais. Le script fait un remplacement par paragraphe, puis vérifie le compte.
- **Ne jamais écrire dans un fichier ouvert dans Word.** Word réécrit le fichier à l'enregistrement et peut annuler vos modifications, ou les vôtres annulent les siennes.
- **Word modifie le fichier à chaque enregistrement** : il découpe le texte en morceaux (runs), ajoute des balises de langue, change des identifiants Zotero. Revérifiez toujours après un passage dans Word.
- **Texte coupé entre plusieurs morceaux.** Un mot peut être réparti sur plusieurs runs. Le script travaille sur le texte complet du paragraphe et recolle les morceaux sans toucher aux champs.
- **Sortie qui semble « bloquée ».** Python peut retenir l'affichage quand sa sortie est redirigée. Lancez `python -u` pour voir la progression en direct.

## Livrable attendu
- La copie modifiée, la sauvegarde, le fichier JSON des corrections (trace).
- Le rapport d'intégrité, sans écart inattendu.
- La liste des modifications appliquées, avec leur ligne dans le nouveau PDF.

## Exemple générique
```
python remplacer_texte.py copie.docx corrections.json --simulation
  [1/1] OK  'the bar color'
  [1/1] OK  '(Table 1).'
Simulation : 2/2 corrections trouvées. Aucun fichier écrit.

python remplacer_texte.py copie.docx corrections.json
Écrit : copie.docx (2 corrections)

python verifier_integrite.py sauvegarde.docx copie.docx
Champs Zotero 48 → 48 | images 6 → 6 (identiques) | paragraphes modifiés : 2
```

## Scripts
- `scripts/remplacer_texte.py` : remplacements sûrs (tout ou rien, sans toucher aux champs, mise en forme contrôlée).
- `scripts/verifier_integrite.py` : compare deux .docx (champs, images, bibliographie, paragraphes modifiés).
