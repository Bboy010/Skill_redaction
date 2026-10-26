#!/usr/bin/env python3
"""
statut_modifications.py : pour chaque modification proposée (ancien → nouveau), dit si elle est
GARDÉE, REFUSÉE ou AUTRE dans le fichier renvoyé par l'auteur. LECTURE SEULE.

  GARDÉE  : le nouveau texte est présent (et l'ancien a disparu) ;
  REFUSÉE : l'ancien texte est toujours là ;
  AUTRE   : ni l'un ni l'autre → l'auteur a réécrit le passage lui-même (à relire).

Les numéros de citation [n] sont ignorés dans la comparaison (ils changent après un Refresh Zotero).

Il liste aussi, si --reference est donnée, les paragraphes que l'auteur a modifiés
et qui ne correspondent à AUCUNE proposition (ajouts personnels de l'auteur).

Fichier de propositions (JSON) : le même format que pour remplacer_texte.py
  [{"ancien": "...", "nouveau": "..."}, {"ancien": "...", "segments": [["...", null], ...]}]
  (champ optionnel "id" pour nommer la proposition)

Usage :
  python statut_modifications.py version_auteur.docx propositions.json
  python statut_modifications.py version_auteur.docx propositions.json --reference version_soumise.docx

Prérequis : pip install python-docx
"""
import argparse
import difflib
import json
import re
import docx

norm = lambda s: re.sub(r"\s+", " ", re.sub(r"\[[\d,–\- ]+\]", "[#]", s)).strip()


def texte(chemin):
    return [p.text for p in docx.Document(chemin).paragraphs if p.text.strip()]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("auteur", help="version renvoyée par l'auteur (.docx)")
    ap.add_argument("propositions", help="JSON des modifications proposées")
    ap.add_argument("--reference", help="version de départ (.docx) pour isoler les ajouts de l'auteur")
    a = ap.parse_args()

    paras_auteur = texte(a.auteur)
    T = norm("\n".join(paras_auteur))
    props = json.load(open(a.propositions, encoding="utf-8"))
    bilan = {"GARDÉE": [], "REFUSÉE": [], "AUTRE": []}
    nouveaux_textes = []
    for k, p in enumerate(props, 1):
        ancien = norm(p["ancien"])
        nouveau = norm(p.get("nouveau") or "".join(s[0] for s in p.get("segments", [])))
        nouveaux_textes.append(nouveau)
        a_new = bool(nouveau) and nouveau in T
        a_old = ancien in T and not (ancien in nouveau and a_new)
        statut = "GARDÉE" if a_new and not a_old else ("REFUSÉE" if a_old else "AUTRE")
        bilan[statut].append((p.get("id", k), p["ancien"], nouveau))

    for statut, items in bilan.items():
        print(f"\n===== {statut} : {len(items)}")
        for ident, ancien, nouveau in items:
            print(f"  [{ident}] {ancien[:70]!r}  →  {nouveau[:70]!r}")

    if a.reference:
        ref = [norm(x) for x in texte(a.reference)]
        aut = [norm(x) for x in paras_auteur]
        print("\n===== Paragraphes modifiés par l'auteur sans lien avec une proposition")
        sm = difflib.SequenceMatcher(a=ref, b=aut, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            for j in range(j1, j2):
                para = aut[j]
                if not any(n and n[:40] in para for n in nouveaux_textes):
                    print(f"  + {para[:160]!r}")
    print("\nNotez les refus dans le journal du projet : ils ne doivent plus être proposés.")
