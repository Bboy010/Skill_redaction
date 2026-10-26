---
name: reponse-aux-reviewers
description: Analyser une décision éditoriale et rédiger la lettre de réponse aux reviewers, en citant chaque commentaire mot pour mot, avec un ton humble, des promesses limitées à ce qui est réellement fait et des renvois à des lignes exactes. À utiliser dès qu'on reçoit une décision (minor/major revision), qu'on prépare ou corrige une « response to reviewers », ou qu'un reviewer reproche qu'un point n'a pas été traité.
---

# Réponse aux reviewers

## Objectif
Produire une lettre qui convainc l'éditeur parce qu'elle est **vérifiable**.
Chaque commentaire est cité exactement. Chaque réponse renvoie à une modification réellement présente, à une ligne précise.

## Quand l'utiliser
- Vous recevez une décision éditoriale avec des commentaires.
- Vous devez écrire ou mettre à jour la lettre de réponse.
- Un reviewer dit qu'une demande précédente n'a pas été traitée.

## Prérequis
- La décision complète (PDF ou e-mail), avec tous les commentaires.
- Le manuscrit **réellement soumis** au tour précédent (voir le skill comparaison-versions-et-suivi).
- La lettre de réponse du tour précédent, s'il y en a une.
- Le PDF du manuscrit révisé, avec la numérotation des lignes.

## Étapes
1. **Lister les commentaires.** Copiez chaque commentaire **mot pour mot**, sans le résumer, dans un tableau à 3 colonnes : reviewer / commentaire / statut. Un commentaire qui contient deux demandes compte pour deux lignes.
2. **Retrouver l'historique.** Si un reviewer renvoie à un commentaire plus ancien (« one of the Reviewer 2 comments… »), retrouvez ce commentaire **et** ce que la lettre précédente avait promis.
3. **Vérifier la promesse précédente.** Comparez ce que la lettre disait avec ce que le manuscrit contient vraiment. Si la promesse n'était pas tenue, il faudra le reconnaître.
4. **Faire les modifications d'abord, écrire ensuite.** La lettre décrit le manuscrit final, pas des intentions. Utilisez les skills edition-docx-sans-casse et verification-des-sources.
5. **Rédiger chaque réponse** sur le modèle : remerciement bref, ce qui a été fait, où (section et lignes), citation exacte de la nouvelle phrase si elle est courte.
6. **Reconnaître les erreurs simplement.** « We thank the reviewer and apologise for the oversight. » Ne vous justifiez pas longuement, ne contredisez pas sèchement.
7. **Relever les numéros de ligne dans le PDF final**, après tout Refresh Zotero. Vérifiez chaque renvoi avec `scripts/verifier_renvois_lettre.py`.
8. **Ajouter un paragraphe « Additional corrections »** pour les changements faits sans demande d'un reviewer. N'y mettez que ce qui est réellement dans le manuscrit.

## Checklist de contrôle
- [ ] Chaque commentaire est cité mot pour mot, aucun n'est oublié.
- [ ] Chaque réponse renvoie à une ligne du PDF final, et le texte trouvé à cette ligne correspond.
- [ ] Chaque phrase citée entre guillemets se retrouve **à l'identique** dans le manuscrit.
- [ ] Aucune promesse ne décrit une modification refusée par l'auteur ou non faite.
- [ ] Les numéros de référence cités ([12], [20–23]…) sont ceux de la bibliographie finale.
- [ ] Aucune phrase du type « No other changes were made » si ce n'est pas vrai.
- [ ] Le ton est humble, sans contre-attaque.
- [ ] Les métadonnées du fichier de la lettre sont propres (auteur, outil de génération).

## Pièges fréquents (leçons apprises)
- **Promettre ce qui n'est pas fait.** Une lettre disait « moved to the legend and the Methods ». Le texte était resté à part et les Méthodes ne disaient rien. Le reviewer suivant l'a vu tout de suite.
- **Décrire une métrique de mémoire.** La lettre définissait un chiffre « par échantillon ». Le recalcul a montré une moyenne « par génome ». Recalculez avant d'écrire (skill verification-des-sources).
- **Réutiliser une ancienne formulation sans la revérifier.** Une phrase proposée plus tôt peut être fausse. Revérifiez-la dans les données avant de la reprendre.
- **Numéros de ligne relevés trop tôt.** Ils changent après un Refresh Zotero, l'ajout d'une phrase ou la fusion de deux paragraphes. Relevez-les en dernier, sur le PDF final.
- **Lettre désynchronisée du manuscrit.** Si l'auteur refuse une modification, retirez-la aussi de la lettre.
- **Un détail qui ne correspond plus.** La lettre disait « the tools used for Figures 2 and 5 » alors que ces numéros avaient été retirés du texte du manuscrit. Relisez la lettre après chaque changement du manuscrit.
- **Métadonnées d'outil.** Une lettre générée par script peut porter « python-docx » comme auteur. Videz les propriétés du fichier.

## Livrable attendu
- La lettre (.docx et .pdf) : en-tête (éditeur, numéro de manuscrit, titre), réponses par reviewer, « Additional corrections », formule finale.
- Un tableau de contrôle des renvois : ligne citée → texte trouvé dans le PDF → OK / à corriger.

## Exemple générique
> **Reviewer 3.** *« The text at lines 300–304 still appears separately from the Figure 5 legend. This needs to be edited. »*
>
> **Response.** We thank the reviewer for this careful check and apologise for the oversight. The paragraph has been merged into the Figure 5 legend (lines 312–318). While merging it, we checked each statement against the image and corrected two descriptions that did not match it. The alignment step is now also described in the Methods (lines 201–203): *“The candidates were aligned with the reference sequence using Tool A [41].”*

## Scripts
- `scripts/pdf_lignes.py` : reconstruit les lignes numérotées d'un PDF (numéros dans la marge droite ou gauche).
- `scripts/verifier_renvois_lettre.py` : liste chaque « line(s) N–M » de la lettre et affiche le texte trouvé à ces lignes, pour contrôle humain.
- `assets/modele_lettre.md` : squelette de lettre à copier.
