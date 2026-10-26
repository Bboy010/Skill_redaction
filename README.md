# Skill_redaction : méthode de révision d'un article scientifique

Ces skills décrivent une **méthode de travail** pour réviser un article après une décision éditoriale.
Ils marchent pour n'importe quel article et n'importe quelle revue.
Ils sont indépendants : vous pouvez en utiliser un seul.

Chaque skill est un dossier avec :
- un fichier `SKILL.md` (la méthode, pas à pas) ;
- parfois un dossier `scripts/` (des outils Python ou PowerShell, à lancer en ligne de commande) ;
- parfois un dossier `assets/` (des modèles à copier).

## Les 10 skills

| Skill | À quoi il sert |
|---|---|
| [reponse-aux-reviewers](reponse-aux-reviewers/SKILL.md) | Lire une décision, citer chaque commentaire mot pour mot, rédiger une réponse humble qui ne promet que ce qui est fait, avec des renvois à des lignes exactes. |
| [verification-des-sources](verification-des-sources/SKILL.md) | Recalculer chaque chiffre du texte à partir des données brutes et signaler ce qui ne peut pas être vérifié. |
| [legende-vs-figure](legende-vs-figure/SKILL.md) | Comparer chaque phrase d'une légende avec ce que l'image montre vraiment. |
| [controle-citations-zotero](controle-citations-zotero/SKILL.md) | Vérifier la numérotation des références : continuité, ordre, orphelines, numéros tapés à la main, citations restées à l'ancien numéro. |
| [edition-docx-sans-casse](edition-docx-sans-casse/SKILL.md) | Modifier un .docx sans casser la mise en forme, les italiques ni les champs Zotero. |
| [comparaison-versions-et-suivi](comparaison-versions-et-suivi/SKILL.md) | Comparer deux versions d'un manuscrit et produire le document avec suivi des modifications. |
| [relecture-par-gravite](relecture-par-gravite/SKILL.md) | Relire tout le manuscrit et classer chaque problème : bloquant, important, cosmétique. |
| [controle-non-regression](controle-non-regression/SKILL.md) | Vérifier qu'une nouvelle modification ne contredit ni les reviewers précédents ni la lettre de réponse. |
| [controle-residus-avant-soumission](controle-residus-avant-soumission/SKILL.md) | Chasser les restes techniques avant l'envoi : suivi de modifications, commentaires, surlignage, métadonnées, fichiers à joindre. |
| [suivi-de-projet-et-decisions](suivi-de-projet-et-decisions/SKILL.md) | Tenir un journal de décisions et une checklist de soumission. La version de l'auteur fait toujours foi. |

## Ordre conseillé dans un cycle de révision

```
 0. suivi-de-projet-et-decisions      ← à ouvrir dès le début, à tenir jusqu'à la fin
 1. reponse-aux-reviewers (étapes 1-3) ← lire la décision, lister chaque commentaire
 2. comparaison-versions-et-suivi     ← identifier le fichier RÉELLEMENT soumis
 3. relecture-par-gravite             ← état des lieux complet, sans rien modifier
 4. verification-des-sources          ← recalculer chaque chiffre concerné
 5. legende-vs-figure                 ← pour chaque figure touchée par les reviewers
 6. edition-docx-sans-casse           ← appliquer UNIQUEMENT ce qui est validé
 7. controle-citations-zotero         ← après tout ajout ou déplacement de référence
 8. controle-non-regression           ← les corrections n'ont rien cassé ?
 9. reponse-aux-reviewers (fin)       ← rédiger la lettre à partir du manuscrit final
10. comparaison-versions-et-suivi     ← document suivi contre la version soumise
11. controle-residus-avant-soumission ← dernier passage avant l'envoi
```

Le principe est simple : **on regarde, on vérifie, on fait valider, puis on modifie**. Jamais l'inverse.

## Mode d'emploi pour les apprenants

1. Lisez d'abord ce README, puis le [parcours complet d'exemple](EXEMPLE_PARCOURS.md).
2. Pour chaque étape, ouvrez le `SKILL.md` correspondant. Suivez les étapes numérotées dans l'ordre.
3. Cochez la **checklist** à la fin de chaque skill avant de passer au suivant.
4. Lisez la section **pièges fréquents**. Ce sont des erreurs réellement commises. Elles coûtent cher si on les découvre au dernier moment.
5. Travaillez **toujours sur une copie** de vos fichiers. Gardez une sauvegarde avant chaque modification.
6. Avec un assistant IA (Claude Code ou autre) : donnez-lui le chemin du dossier du skill et demandez-lui de suivre le `SKILL.md`.

## Installer les outils des scripts

Les scripts demandent Python 3.9 ou plus récent et quelques bibliothèques :

```
pip install python-docx pymupdf openpyxl
```

Le script de comparaison avec suivi des modifications utilise Microsoft Word (Windows, PowerShell).
Sans Word, utilisez la fonction « Comparer » de Word ou de LibreOffice à la main. La méthode reste la même.

Tous les scripts prennent leurs fichiers en arguments. Aucun chemin n'est écrit en dur.
Tapez `python nom_du_script.py --help` pour voir les options.

## Règles d'or (valables pour tous les skills)

- **La version de l'auteur fait foi.** On ne modifie jamais son fichier sans accord explicite.
- **On ne promet que ce qui est fait.** Chaque phrase de la lettre doit se retrouver dans le manuscrit.
- **On recalcule, on ne recopie pas.** Un chiffre repris d'une ancienne version n'est pas un chiffre vérifié.
- **On sauvegarde avant d'écrire**, et on contrôle après chaque modification.
- **On ne réécrit jamais un fichier ouvert dans Word.** Fermez-le d'abord.

## Utiliser ces skills avec Claude Code

Un skill est un dossier avec un fichier `SKILL.md`. Deux façons de l'utiliser :

1. **Dans un projet** : copiez le dossier `Skill_redaction/` dans votre projet, puis demandez à Claude Code :
   « Suis le skill `Skill_redaction/controle-citations-zotero/SKILL.md` sur mon manuscrit. »
2. **Pour tous vos projets** : copiez les dossiers des skills voulus dans `~/.claude/skills/`
   (sous Windows : `C:\Users\<vous>\.claude\skills\`). Claude Code les propose alors automatiquement.

Dans les deux cas, travaillez sur une **copie** de vos fichiers et gardez une sauvegarde avant chaque modification.

## Contenu du dépôt

```
Skill_redaction/
├── README.md              ce fichier
├── EXEMPLE_PARCOURS.md    un cycle de révision complet, étape par étape
└── <skill>/               10 dossiers : SKILL.md, parfois scripts/ et assets/
```

## Auteur

Koffi Anderson Hongo, doctorant en biologie aquatique et métagénomique environnementale (Université Nangui Abrogoua, Abidjan, Côte d'Ivoire).
Contact : hkoffianderson@gmail.com

Ces skills sont tirés d'une expérience réelle de révision d'un article scientifique, puis généralisés et anonymisés.
Les remarques, corrections et suggestions sont les bienvenues (issues GitHub ou e-mail).
