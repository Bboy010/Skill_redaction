---
name: suivi-de-projet-et-decisions
description: Tenir, pendant toute une révision d'article, un journal de session (décisions verrouillées, modifications refusées à ne plus proposer, fichier de référence, sauvegardes) et une checklist de soumission, en partant du principe que la version de l'auteur fait toujours foi. À utiliser dès le début d'une révision, à chaque reprise de travail après une pause, quand l'auteur accepte ou refuse des propositions, ou quand plusieurs versions et plusieurs personnes interviennent sur un manuscrit.
---

# Suivi de projet et décisions

## Objectif
Garder une **mémoire fiable** de la révision : ce qui est décidé, refusé, fait, et ce qui reste à faire.
On évite ainsi de refaire un débat déjà tranché, de reproposer une correction refusée, ou de travailler sur le mauvais fichier.

## Quand l'utiliser
- Au début de la révision : créer les deux fichiers.
- À chaque reprise de travail : relire le journal avant toute action.
- Quand l'auteur valide ou refuse des propositions.
- Avant la soumission : la checklist sert de liste finale.

## Prérequis
- Un dossier de projet, avec les deux modèles : `assets/modele_journal.md` et `assets/modele_checklist.md`.

## Étapes
1. **Créer `JOURNAL.md`** à partir du modèle. Remplissez l'en-tête : manuscrit, revue, échéance, **fichier de référence**.
2. **Écrire les décisions verrouillées** : orthographe imposée, cadrage (descriptif, sans tests statistiques…), termes à employer ou à éviter, logiciels réellement utilisés. Une décision verrouillée ne se rediscute pas sans l'auteur.
3. **Après chaque séance**, ajouter une entrée numérotée et datée : ce qui a été fait, les fichiers créés, les **sauvegardes**, ce qui reste.
4. **Quand l'auteur répond**, noter ce qu'il a **gardé**, **refusé** ou **ajouté**. Les refus vont dans la liste « à ne plus proposer ».
5. **Quand l'auteur renvoie son propre fichier**, il devient le fichier de référence. Notez-le en tête du journal. Les anciennes versions deviennent **obsolètes**.
6. **Tenir `CHECKLIST_SOUMISSION.md`** : fichiers à joindre (avec dates), actions restantes de l'auteur, points reportés, points en attente de validation.
7. **Avant toute modification d'un fichier**, relire : le fichier de référence, les décisions verrouillées, la liste des refus.

## Checklist de contrôle
- [ ] Le fichier de référence est écrit en tête du journal et à jour.
- [ ] Les décisions verrouillées sont listées.
- [ ] Les modifications refusées sont listées, avec la date.
- [ ] Chaque entrée indique les sauvegardes créées.
- [ ] La checklist de soumission liste les fichiers à joindre avec leur date, et les fichiers obsolètes.
- [ ] Les dates sont absolues (« 2099-03-14 », pas « jeudi dernier »).

## Pièges fréquents (leçons apprises)
- **La version de l'auteur fait toujours foi.** Ne la modifiez jamais sans son accord explicite. Préparez vos changements sur une copie.
- **Reproposer une correction refusée** fait perdre du temps et de la confiance. Consultez la liste des refus avant chaque rapport.
- **Changer d'avis sur un fait sans le noter.** Une décision corrigée (par exemple un logiciel mal identifié) doit être marquée « ANNULE la décision du [date] », sinon l'ancienne reviendra.
- **Travailler sur le mauvais fichier.** Toujours identifier le fichier réellement soumis et le noter (skill comparaison-versions-et-suivi).
- **Ne jamais écrire dans un fichier ouvert dans Word.** Avant d'écrire, demandez à l'auteur de le fermer, ou vérifiez son empreinte avant et après.
- **Les numéros de ligne changent après un Refresh** ou une retouche. Notez dans le journal sur quel PDF ils ont été relevés.
- **Ne pas noter les sauvegardes.** Sans nom de fichier de sauvegarde, impossible de revenir en arrière proprement.

## Livrable attendu
- `JOURNAL.md` : en-tête, décisions verrouillées, refus, entrées numérotées et datées.
- `CHECKLIST_SOUMISSION.md` : fichiers à joindre, actions de l'auteur, points reportés.

## Exemple générique
```
## FICHIER DE RÉFÉRENCE
manuscrit/Manuscript-edit.docx (auteur, 2099-03-14). Ne pas modifier sans accord.
Obsolètes : Manuscript_v2.docx, Manuscript_v2_suivi.docx

## DÉCISIONS VERROUILLÉES
- Orthographe britannique (Oxford, -ize conservé). Pas de tiret cadratin.
- Cadrage descriptif : aucun test statistique inférentiel.

## REFUSÉ PAR L'AUTEUR (ne plus proposer)
- 2099-03-14 : renommer la section 3.1 ; reformuler la phrase sur les 12 génomes.

## 12. (2099-03-14) Deuxième Refresh Zotero vérifié : 52 références, 0 problème.
   PDF et document suivi régénérés. Sauvegarde : .backup_avant_refresh.docx.
```

## Fichiers fournis
- `assets/modele_journal.md` : modèle de journal.
- `assets/modele_checklist.md` : modèle de checklist de soumission.
