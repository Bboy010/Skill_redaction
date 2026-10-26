---
name: relecture-par-gravite
description: Relire intégralement un manuscrit, section par section et phrase par phrase, et produire un rapport classé par gravité (bloquant / important / cosmétique) avec, pour chaque point, la ligne, le texte actuel, la correction proposée et la justification, sans rien modifier avant validation par l'auteur. À utiliser avant une soumission ou une resoumission, quand on demande une « relecture complète », un « état des lieux » ou un « audit » du manuscrit.
---

# Relecture classée par gravité

## Objectif
Donner à l'auteur une vue complète et hiérarchisée des problèmes, pour qu'il **décide** de ce qui est corrigé.
On ne modifie rien pendant la relecture.

## Quand l'utiliser
- Avant une soumission ou une resoumission.
- Après une décision éditoriale, pour faire l'état des lieux.
- Quand un manuscrit a beaucoup changé et qu'on veut tout revérifier.

## Prérequis
- Le manuscrit de référence (.docx) et son PDF avec numéros de ligne.
- Les règles de la revue (orthographe, style de références, structure).
- Les décisions déjà prises (journal du projet), pour ne pas reproposer ce qui a été refusé.
- La lettre de réponse précédente, s'il y en a une.

## Étapes
1. **Extraire les lignes du PDF** : `python scripts/pdf_lignes.py manuscrit.pdf lignes.txt`. Vous citerez ainsi des lignes exactes.
2. **Lancer les contrôles automatiques** : `python scripts/controles_langue.py manuscrit.docx --lignes lignes.txt`. Ils repèrent l'orthographe (US/UK), les tirets cadratins, les doubles espaces, les intervalles avec un trait d'union, les mots interdits.
3. **Relire section par section**, dans l'ordre : résumé, introduction, méthodes, résultats, discussion, conclusion, légendes, tableaux, matériel supplémentaire, références.
4. **Pour chaque phrase, vérifier :**
   - la langue : grammaire, accords, phrases trop longues ou bancales ;
   - la cohérence : le même chiffre est-il identique partout (résumé, résultats, discussion, tableaux) ?
   - l'exactitude : l'affirmation est-elle soutenue par les données ou par la référence citée ?
   - la prudence : pas de sur-affirmation (« demonstrates », « first », « reservoir ») sans preuve ;
   - les renvois : chaque figure, tableau et élément supplémentaire est cité, dans l'ordre ;
   - les citations : la référence dit-elle vraiment ce que la phrase lui attribue ?
5. **Classer chaque point :**
   - **Bloquant** : erreur factuelle, chiffre faux, référence fausse, promesse de la lettre non tenue. Un reviewer le verrait.
   - **Important** : imprécision, sur-affirmation, méthode incomplète, incohérence entre sections.
   - **Cosmétique** : orthographe, typographie, style.
6. **Rédiger le rapport** (modèle ci-dessous). Une ligne par point : ligne, texte actuel, correction proposée, justification.
7. **Présenter le rapport et attendre la validation.** L'auteur choisit ce qui est appliqué. Notez ses refus dans le journal.

## Checklist de contrôle
- [ ] Toutes les sections ont été lues, y compris les légendes, les tableaux et les références.
- [ ] Chaque point a une ligne, un texte actuel, une proposition et une justification.
- [ ] Les chiffres répétés ont été comparés entre sections.
- [ ] L'ordre des renvois (figures, tableaux, supplémentaires) a été vérifié.
- [ ] Aucune modification refusée auparavant n'est reproposée.
- [ ] Rien n'a été modifié dans le manuscrit.

## Pièges fréquents (leçons apprises)
- **Modifier avant de faire valider.** L'auteur peut refuser une grande partie des propositions. Travailler sur une copie, et seulement après validation.
- **Corriger une erreur d'une façon qui en crée une autre.** Ajouter une phrase dans les Méthodes qui cite « Figure 4 » avant la Figure 2 casse l'ordre des renvois.
- **Classer trop haut.** Si tout est « bloquant », plus rien ne l'est. Réservez « bloquant » à ce qui est faux ou vérifiable par un reviewer.
- **Supposer qu'une phrase est vraie parce qu'elle vient d'une version déjà relue.** Les erreurs anciennes survivent aux révisions.
- **Oublier le matériel supplémentaire.** Il contient des légendes, des références numérotées et des chiffres qui doivent concorder avec le texte principal.
- **Reproposer ce qui a été refusé.** Consultez le journal du projet avant de rédiger.

## Livrable attendu
Un fichier `RELECTURE.md` :

```
# Relecture — [manuscrit], [date]
Bilan : X bloquants · Y importants · Z cosmétiques.
## Vérifié et conforme
## Bloquant
| # | Ligne | Texte actuel | Correction proposée | Justification |
## Important
## Cosmétique
```

## Exemple générique
| # | Ligne | Texte actuel | Correction proposée | Justification |
|---|---|---|---|---|
| B1 | 142–145 | « Tool A [21] was used… » ([21] = un article sans rapport) | Insérer la bonne référence via Zotero | Citation qui pointe vers le mauvais article |
| I3 | 310 | « These results demonstrate degradation… » | « These results suggest a potential for degradation… » | Aucune mesure d'activité : sur-affirmation |
| C7 | 64 | « color » | « colour » | Orthographe britannique demandée par la revue |

## Scripts
- `scripts/pdf_lignes.py` : lignes numérotées du PDF.
- `scripts/controles_langue.py` : contrôles automatiques configurables (orthographe, typographie, mots interdits).
