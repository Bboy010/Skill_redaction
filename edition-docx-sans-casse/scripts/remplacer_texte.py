#!/usr/bin/env python3
"""
remplacer_texte.py : applique des corrections de texte dans un .docx sans casser la mise en forme
ni les champs (Zotero, renvois…).

Principes :
  * on ne touche jamais au texte situé DANS un champ (instruction ou résultat affiché) ;
  * le nouveau texte reprend la mise en forme du premier morceau remplacé,
    sauf si l'on impose la mise en forme avec "segments" ;
  * TOUT OU RIEN : si une correction n'est pas trouvée exactement n fois, rien n'est écrit ;
  * --simulation : vérifie tout sans écrire.

Fichier de corrections (JSON) : liste d'objets
  {"ancien": "...", "nouveau": "...", "n": 1}
  {"ancien": "...", "segments": [["texte", "gras"|"italique"|"normal"|null], ...], "n": 1}
  {"ancien": "...", "nouveau": "...", "surligner": true, "n": 1}

Usage :
  python remplacer_texte.py copie.docx corrections.json --simulation
  python remplacer_texte.py copie.docx corrections.json
  python remplacer_texte.py copie.docx corrections.json --sortie autre_copie.docx

Conseil : lancez-le sur une COPIE, jamais sur le fichier de l'auteur, et jamais sur un fichier ouvert dans Word.
Prérequis : pip install python-docx
"""
import argparse
import copy
import json
import sys
import docx
from docx.oxml.ns import qn

W = lambda t: qn("w:" + t)
XS = "{http://www.w3.org/XML/1998/namespace}space"


def runs_hors_champs(p):
    """Runs du paragraphe qui ne sont pas à l'intérieur d'un champ."""
    out, prof = [], 0
    for r in p._p.iter(W("r")):
        fc = r.find(W("fldChar"))
        if fc is not None:
            t = fc.get(W("fldCharType"))
            prof += 1 if t == "begin" else (-1 if t == "end" else 0)
            continue
        if prof == 0:
            out.append(r)
    return out


def texte_run(r):
    s = ""
    for c in r:
        if c.tag == W("t"):
            s += c.text or ""
        elif c.tag == W("tab"):
            s += "\t"
        elif c.tag in (W("br"), W("cr")):
            s += "\n"
    return s


def simple(r):
    """Run qui ne contient que du texte (pas de tabulation, d'image, de saut)."""
    return all(c.tag in (W("rPr"), W("t")) for c in r)


def ecrire_texte(r, s):
    for c in [c for c in r if c.tag != W("rPr")]:
        r.remove(c)
    t = r.makeelement(W("t"), {})
    t.text = s
    t.set(XS, "preserve")
    r.append(t)


def regler(r, style=None, surligner=False):
    rpr = r.find(W("rPr"))
    if rpr is None:
        rpr = r.makeelement(W("rPr"), {})
        r.insert(0, rpr)
    if style in ("gras", "italique", "normal"):
        for tag in ("b", "bCs", "i", "iCs"):
            e = rpr.find(W(tag))
            if e is not None:
                rpr.remove(e)
        if style == "gras":
            rpr.append(rpr.makeelement(W("b"), {})); rpr.append(rpr.makeelement(W("bCs"), {}))
        if style == "italique":
            rpr.append(rpr.makeelement(W("i"), {})); rpr.append(rpr.makeelement(W("iCs"), {}))
    if surligner and rpr.find(W("highlight")) is None:
        h = rpr.makeelement(W("highlight"), {})
        h.set(W("val"), "yellow")
        rpr.append(h)


def remplacer_dans(p, ancien, segments, surligner):
    """Remplace la première occurrence de `ancien` dans le paragraphe. Retourne True si fait."""
    rs = runs_hors_champs(p)
    textes = [texte_run(r) for r in rs]
    plein = "".join(textes)
    i = plein.find(ancien)
    if i < 0:
        return False
    j = i + len(ancien)
    couverts, pos = [], 0
    for r, t in zip(rs, textes):
        a, b = pos, pos + len(t)
        pos = b
        if b > i and a < j:
            couverts.append((r, a, b))
    for r, _, _ in couverts:
        if not simple(r):
            raise ValueError(f"le texte « {ancien[:40]} » chevauche une tabulation, une image ou un saut : "
                             "réduisez la portion à remplacer")
    premier, a0, _ = couverts[0]
    dernier, _, b1 = couverts[-1]
    tete = texte_run(premier)[: i - a0]
    queue = texte_run(dernier)[len(texte_run(dernier)) - (b1 - j):] if b1 > j else ""
    nouveaux = []
    if tete:
        r = copy.deepcopy(premier); ecrire_texte(r, tete); nouveaux.append(r)
    for texte, style in segments:
        r = copy.deepcopy(premier); ecrire_texte(r, texte); regler(r, style, surligner); nouveaux.append(r)
    if queue:
        r = copy.deepcopy(dernier); ecrire_texte(r, queue); nouveaux.append(r)
    for r in nouveaux:
        premier.addprevious(r)
    for r, _, _ in couverts:
        parent = r.getparent()
        parent.remove(r)
        if parent.tag == W("hyperlink") and not parent.findall(W("r")):
            parent.getparent().remove(parent)
    return True


def appliquer(d, corr):
    ancien = corr["ancien"]
    if "segments" in corr:
        segments = [(s[0], s[1]) for s in corr["segments"]]
    else:
        segments = [(corr["nouveau"], None)]
    n = 0
    for p in d.paragraphs:
        # une seule occurrence par paragraphe et par passage : évite les boucles
        # quand le nouveau texte contient l'ancien (changement de gras seulement)
        while True:
            avant = "".join(texte_run(r) for r in runs_hors_champs(p))
            if ancien not in avant:
                break
            remplacer_dans(p, ancien, segments, corr.get("surligner", False))
            n += 1
            nouveau_plein = "".join(s for s, _ in segments)
            if ancien in nouveau_plein:
                break
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx", help="COPIE de travail du manuscrit")
    ap.add_argument("corrections", help="fichier JSON des corrections")
    ap.add_argument("--sortie", help="écrire dans ce fichier au lieu d'écraser la copie")
    ap.add_argument("--simulation", action="store_true", help="vérifier sans rien écrire")
    a = ap.parse_args()

    with open(a.corrections, encoding="utf-8") as f:
        corrections = json.load(f)
    d = docx.Document(a.docx)
    erreurs = 0
    for k, c in enumerate(corrections, 1):
        try:
            n = appliquer(d, c)
        except ValueError as e:
            print(f"[{k}] ERREUR {e}"); erreurs += 1; continue
        attendu = c.get("n", 1)
        etat = "OK " if n == attendu else "ÉCHEC"
        if n != attendu:
            erreurs += 1
        print(f"[{n}/{attendu}] {etat} {c['ancien'][:70]!r}", flush=True)

    if erreurs:
        print(f"\n{erreurs} correction(s) en échec : AUCUN fichier écrit.")
        sys.exit(1)
    if a.simulation:
        print(f"\nSimulation : {len(corrections)}/{len(corrections)} corrections trouvées. Aucun fichier écrit.")
    else:
        cible = a.sortie or a.docx
        d.save(cible)
        print(f"\nÉcrit : {cible} ({len(corrections)} corrections)")
