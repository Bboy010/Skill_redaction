#!/usr/bin/env python3
"""
statut_modifications.py : pour chaque modification proposée (ancien → nouveau), dit si elle est
GARDÉE, REFUSÉE, AUTRE ou AMBIGUË dans le fichier renvoyé par l'auteur. LECTURE SEULE.

  GARDÉE  : le nouveau texte est présent (et l'ancien a disparu) ;
  REFUSÉE : l'ancien texte est toujours là ;
  AUTRE   : ni l'un ni l'autre → l'auteur a réécrit le passage lui-même (à relire) ;
  AMBIGUË : le nouveau texte est trop court (moins de 20 caractères), vide (une suppression) ou existait déjà
            dans la version de départ, et il n'a pas été retrouvé à sa place → à relire.

Un nouveau texte court, vide ou déjà présent ne prouve rien à lui seul (« x » ou « Site B. » se trouvent partout).
Il est donc cherché dans son contexte : les 15 caractères avant et après l'ancien texte dans la
version de départ (--reference). Sans --reference, une telle proposition n'est GARDÉE que si son contexte
est retrouvé : elle est donc en général AMBIGUË.

Les numéros de citation [n] sont ignorés dans la comparaison (ils changent après un Refresh Zotero).

Si --reference est donnée, il liste aussi les paragraphes modifiés par l'auteur en dehors des propositions :
  +  un paragraphe qui ne correspond à aucune proposition (ajout ou réécriture de l'auteur) ;
  ~  un paragraphe qui contient une proposition, avec les autres changements de l'auteur dans ce même paragraphe.

Fichier de propositions (JSON) : le même format que pour remplacer_texte.py
  [{"ancien": "...", "nouveau": "..."}, {"ancien": "...", "segments": [["...", null], ...]}]
  (champ optionnel "id" pour nommer la proposition)

Usage :
  python statut_modifications.py version_auteur.docx propositions.json
  python statut_modifications.py version_auteur.docx propositions.json --reference version_soumise.docx

Prérequis : pip install python-docx
"""
import argparse
import sys as _sys
try:  # consoles Windows : afficher flèches et accents sans UnicodeEncodeError
    _sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import difflib
import json
import re
import docx

COURT = 20    # un nouveau texte plus court est cherché avec son contexte
CONTEXTE = 15  # caractères de contexte pris avant et après l'ancien texte

norm = lambda s: re.sub(r"\s+", " ", re.sub(r"\[[\d,–\- ]+\]", "[#]", s)).strip()


def texte(chemin):
    return [p.text for p in docx.Document(chemin).paragraphs if p.text.strip()]


def statut(ancien, nouveau, T, R):
    """Statut d'une proposition. ancien, nouveau : textes normalisés ; T : texte de l'auteur ; R : texte de départ (ou None)."""
    a_old = ancien in T and not (ancien in nouveau and nouveau in T)
    faible = len(nouveau) < COURT or (R is not None and nouveau in R)
    if not faible:
        if nouveau in T and not a_old:
            return "GARDÉE"
        return "REFUSÉE" if a_old else "AUTRE"
    # nouveau texte court, vide ou déjà présent : on le cherche à la place de l'ancien
    i = R.find(ancien) if R is not None else -1
    if i >= 0:
        sonde = R[max(0, i - CONTEXTE):i] + nouveau + R[i + len(ancien):i + len(ancien) + CONTEXTE]
        if len(sonde.strip()) >= COURT and sonde in T and not a_old:
            return "GARDÉE"
    if a_old:
        return "REFUSÉE"
    return "AMBIGUË" if (not nouveau or nouveau in T) else "AUTRE"


def changements_mots(a, b):
    """Différences mot à mot entre deux textes de paragraphe, avec trois mots de contexte à gauche."""
    wa, wb = a.split(), b.split()
    out = []
    for o, i1, i2, j1, j2 in difflib.SequenceMatcher(a=wa, b=wb, autojunk=False).get_opcodes():
        if o == "equal":
            continue
        gauche = " ".join(wa[max(0, i1 - 3):i1])
        tete = f"…{gauche} " if gauche else ""
        avant, apres = " ".join(wa[i1:i2]), " ".join(wb[j1:j2])
        out.append(f"{tete}+[{apres}]" if o == "insert" else f"{tete}-[{avant}]" if o == "delete"
                   else f"{tete}[{avant}] → [{apres}]")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("auteur", help="version renvoyée par l'auteur (.docx)")
    ap.add_argument("propositions", help="JSON des modifications proposées")
    ap.add_argument("--reference", help="version de départ (.docx) : contexte des textes courts, et autres changements de l'auteur")
    a = ap.parse_args()

    paras_auteur = texte(a.auteur)
    T = norm("\n".join(paras_auteur))
    paras_ref = texte(a.reference) if a.reference else None
    R = norm("\n".join(paras_ref)) if paras_ref else None
    props = json.load(open(a.propositions, encoding="utf-8"))
    bilan = {"GARDÉE": [], "REFUSÉE": [], "AUTRE": [], "AMBIGUË": []}
    paires = []
    for k, p in enumerate(props, 1):
        ancien = norm(p["ancien"])
        nouveau = norm(p.get("nouveau") or "".join(s[0] for s in p.get("segments", [])))
        paires.append((ancien, nouveau))
        bilan[statut(ancien, nouveau, T, R)].append((p.get("id", k), p["ancien"], nouveau))

    for st, items in bilan.items():
        print(f"\n===== {st} : {len(items)}")
        for ident, ancien, nouveau in items:
            print(f"  [{ident}] {ancien[:70]!r}  →  {nouveau[:70]!r}")
    if bilan["AMBIGUË"]:
        print("  (AMBIGUË : le nouveau texte est court, vide ou existait déjà, et n'a pas été retrouvé à sa place : à relire)")

    if a.reference:
        ref = [norm(x) for x in paras_ref]
        aut = [norm(x) for x in paras_auteur]
        print("\n===== Paragraphes modifiés par l'auteur en dehors des propositions")
        print("  (+ sans lien avec une proposition ; ~ contient une proposition, avec les autres changements de l'auteur)")
        sm = difflib.SequenceMatcher(a=ref, b=aut, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            for j in range(j1, j2):
                para = aut[j]
                lies = [k for k, (o, n) in enumerate(paires) if len(n) >= COURT and n[:40] in para]
                if not lies:
                    print(f"  + {para[:160]!r}")
                    continue
                if i1 == i2:
                    continue  # paragraphe entièrement nouveau, construit autour d'une proposition
                base = max(ref[i1:i2], key=lambda r: difflib.SequenceMatcher(a=r, b=para, autojunk=False).ratio())
                for k in lies:
                    base = base.replace(paires[k][0], paires[k][1])
                reste = changements_mots(base, para)
                if reste:
                    print(f"  ~ {para[:100]!r}")
                    for r in reste:
                        print(f"      autre changement : {r}")
    print("\nNotez les refus dans le journal du projet : ils ne doivent plus être proposés.")
