# Exemple de parcours complet (fictif)

Ce parcours est **inventé**. Les noms, numéros et chiffres sont fictifs.
Il montre comment enchaîner les skills, de la décision éditoriale à la soumission.

## Le contexte

- Article : « Diversité de gènes d'estérases dans deux étangs urbains » (fictif).
- Revue : *Journal of Example Microbiology* (fictive).
- Manuscrit : `MS-2099-0042`, version R1 déjà soumise une fois.
- Décision : *minor revision*. Un troisième reviewer (R3) écrit :
  > « The text at lines 300–304 still appears separately from the Figure 5 legend. This needs to be edited. »
- Échéance : 30 jours.

## Jour 1 : ouvrir le projet

**Skill : suivi-de-projet-et-decisions**

- Créer `JOURNAL.md` et `CHECKLIST_SOUMISSION.md` à partir des modèles du skill.
- Noter les décisions déjà prises lors des tours précédents. Exemple : « cadrage descriptif, pas de statistiques », « orthographe britannique ».
- Noter l'échéance.

## Jour 1 : comprendre la demande

**Skill : reponse-aux-reviewers (étapes 1 à 3)**

- Copier le commentaire de R3 **mot pour mot** dans un tableau.
- Retrouver le commentaire d'origine de R2 auquel R3 fait référence : « All of this should be in the figure caption, and in the methods, and cited correctly (not with websites). »
- Constat : la lettre R1 affirmait « moved to the legend and the Methods ». C'était faux. Il faudra le reconnaître avec humilité.

## Jour 1 : identifier le bon fichier

**Skill : comparaison-versions-et-suivi**

- Le dossier contient `manuscrit_R1.docx` (3 mai) et `soumis/Manuscript.docx` (5 mai).
- La comparaison montre : texte identique, mais le gras de quatre renvois et une image de la Figure 3 diffèrent.
- **Le fichier de référence est `soumis/Manuscript.docx`.** Tout le travail repart de lui.

## Jour 2 : état des lieux

**Skill : relecture-par-gravite**

- Relecture complète, rien n'est modifié.
- Rapport : 3 bloquants, 9 importants, 20 cosmétiques. Exemples :
  - bloquant : quatre outils cités avec des numéros de référence qui pointent vers d'autres articles ;
  - important : une métrique (« 4.2 versus 3.1 ») jamais définie, alors que la lettre R1 promettait de la définir ;
  - cosmétique : « color » au lieu de « colour ».
- L'auteur valide une partie des points et en refuse d'autres. Les refus sont notés dans le journal.

## Jour 2 : vérifier les chiffres

**Skill : verification-des-sources**

- La métrique « 4.2 versus 3.1 » est recalculée à partir du tableau brut `genes_par_genome.tsv`.
- Résultat : c'est une moyenne **par génome**, et non par échantillon comme l'affirmait la lettre.
- Une autre phrase parle de « 12 génomes non classés ». Le recalcul ne retrouve pas 12 avec un critère clair. On le signale à l'auteur plutôt que d'inventer une définition.

## Jour 3 : la légende de la Figure 5

**Skill : legende-vs-figure**

- La légende dit « secondary-structure elements are shown above the sequence ». L'image n'en montre aucun : phrase à retirer.
- Elle dit « similar residues highlighted in yellow ». L'image les montre en lettres rouges dans des cadres bleus : à corriger.
- Elle cite trois résidus, alors que l'image montre quatre symboles : retirer la liste ou corriger l'image.

## Jour 3 : modifier le manuscrit

**Skill : edition-docx-sans-casse**

- Sauvegarde : `.backup_avant_R3.docx`.
- Les modifications validées sont écrites dans un fichier JSON, puis appliquées avec `remplacer_texte.py` sur une **copie**.
- Après chaque passage : le nombre de champs Zotero et d'images est inchangé, et les italiques sont vérifiés.
- Piège rencontré : « (4.0% each) » a hérité de l'italique du nom d'espèce voisin. On corrige en ciblant « (4.0%) » seul.

## Jour 3 : les références

**Skill : controle-citations-zotero**

- Les quatre références manquantes sont importées dans Zotero par DOI et insérées à la place de balises jaunes.
- Refresh, puis audit : 3 appels affichent encore l'ancien numéro. Un deuxième Refresh règle le problème.
- La police de la bibliographie a été réinitialisée par Zotero. On met le style Word « Bibliography » en Times New Roman.

## Jour 4 : non-régression

**Skill : controle-non-regression**

- Chaque modification est comparée aux commentaires de R1 et R2 et aux promesses de la lettre.
- Alerte : un titre de section renommé ne correspond plus au titre annoncé à R2 dans la lettre précédente. On revient au titre d'origine.
- Alerte : une phrase ajoutée dans les Méthodes cite les Figures 4 et 6 avant la Figure 2. On retire les numéros.

## Jour 4 : la lettre

**Skill : reponse-aux-reviewers (étapes 4 à 8)**

- Réponse à R3 en trois points (légende, Méthodes, citations), avec les lignes exactes du PDF final.
- Un paragraphe « Additional corrections » ne décrit **que** ce qui est réellement dans le manuscrit.
- L'auteur a refusé deux corrections. Elles sont retirées de la lettre.

## Jour 5 : avant l'envoi

**Skills : comparaison-versions-et-suivi, puis controle-residus-avant-soumission**

- Le document suivi est généré contre `soumis/Manuscript.docx`.
- Résidus trouvés :
  - auteur « PC-Labo-03 » dans les métadonnées : à vider ;
  - chemin local `C:\Users\...` dans le modèle Word : à retirer ;
  - « [12] ) » avec une espace en trop : à corriger.
- Liste finale des fichiers à joindre, avec leurs dates. Les anciennes versions sont marquées obsolètes.

## Résultat

Quatre fichiers envoyés : le manuscrit (.docx), son PDF, le document avec suivi des modifications et la lettre de réponse.
Chaque affirmation de la lettre renvoie à une ligne vérifiée du PDF.
