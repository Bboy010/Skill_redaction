#!/usr/bin/env python3
"""
controles_langue.py : contrôles automatiques de langue et de typographie d'un manuscrit .docx (LECTURE SEULE).

Il ne remplace pas la relecture humaine : il repère les points à regarder.

Contrôles :
  * orthographe US à remplacer par la forme britannique (liste modifiable, --liste-us) ;
  * terminaisons -ise / -ize selon la politique choisie (--politique-ize garder|retirer|ignorer) ;
  * tiret cadratin « — » (souvent déconseillé) ;
  * doubles espaces, espace avant une ponctuation fermante, ponctuation doublée ;
  * intervalles numériques écrits avec un trait d'union (1-3 au lieu de 1–3) ;
  * mots interdits ou à surveiller (--interdits « soil » « significant »…) ;
  * paragraphes « Bibliography » ignorés par défaut (titres de références à ne pas corriger).

Usage :
  python controles_langue.py manuscrit.docx
  python controles_langue.py manuscrit.docx --lignes lignes.txt --interdits soil significant --politique-ize garder

--lignes : fichier produit par pdf_lignes.py, pour afficher le numéro de ligne de chaque point.
Prérequis : pip install python-docx
"""
import argparse
import re
import docx

US_UK = {
    "color": "colour", "colors": "colours", "colored": "coloured", "behavior": "behaviour", "favor": "favour",
    "gray": "grey", "aluminum": "aluminium", "analyze": "analyse", "analyzed": "analysed", "analyzing": "analysing",
    "catalog": "catalogue", "center": "centre", "fiber": "fibre", "liter": "litre", "meter": "metre",
    "tumor": "tumour", "modeling": "modelling", "modeled": "modelled", "labeled": "labelled", "labeling": "labelling",
    "program": "programme", "tons": "tonnes", "fertilizer": "fertiliser", "sulfur": "sulphur",
}
# mots en -ise qui ne sont PAS des verbes en -ize (à ne jamais signaler)
ISE_LEGITIMES = {"analyse", "analysed", "analyses", "hydrolyse", "hydrolysed", "hydrolyses", "catalyse", "catalysed",
                 "catalyses", "otherwise", "precise", "comprise", "comprised", "comprises", "comprising", "advise",
                 "expertise", "exercise", "surprise", "promise", "concise", "wise", "pairwise", "stepwise", "clockwise",
                 "noise", "rise", "raise", "arise", "revise", "revised", "supervise", "supervised", "devise", "enterprise",
                 "compromise", "franchise", "merchandise", "disguise", "televise", "improvise", "excise", "incise"}


def charger_lignes(chemin):
    L = {}
    if chemin:
        for l in open(chemin, encoding="utf-8"):
            m = re.match(r"\s*(\d+) \| (.*)", l)
            if m:
                L[int(m.group(1))] = m.group(2).replace("_", "")
    return L


def ligne_de(L, extrait):
    s = extrait.strip()[:25]
    for longueur in (25, 14):
        s2 = s[:longueur]
        for k in sorted(L):
            if s2 and s2 in L[k]:
                return k
    return "?"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("--lignes", help="fichier de lignes (pdf_lignes.py)")
    ap.add_argument("--interdits", nargs="*", default=[], help="mots à signaler (ex. soil significant novel)")
    ap.add_argument("--politique-ize", choices=["garder", "retirer", "ignorer"], default="garder",
                    help="garder = style Oxford (-ize) ; retirer = style -ise ; ignorer = pas de contrôle")
    ap.add_argument("--style-biblio", default="Bibliography")
    ap.add_argument("--pas-us-uk", action="store_true", help="désactiver le contrôle US/UK (revue en anglais américain)")
    a = ap.parse_args()

    L = charger_lignes(a.lignes)
    d = docx.Document(a.docx)
    regles = {
        "tiret cadratin": r"—",
        "double espace": r"(?<=\S)  +(?=\S)",
        "espace avant ponctuation fermante": r"\s+[\)\],;:](?!\d)|\s+\.(?!\d)",
        "ponctuation doublée": r"(?<!\.)\.\.(?!\.)|,,|;;",
        "point suivi d'une parenthèse '. ('": r"[a-z]\.\s\((?![a-z]\))",
        "intervalle avec trait d'union": r"(?<![\w/.-])\d[\d,]*-\d[\d,]*(?![\w/-])",
    }
    total = 0
    for p in d.paragraphs:
        if p.style.name == a.style_biblio or not p.text.strip():
            continue
        t = p.text
        trouves = []
        for nom, motif in regles.items():
            for m in re.finditer(motif, t):
                trouves.append((nom, m.start(), m.end()))
        if not a.pas_us_uk:
            for us, uk in US_UK.items():
                for m in re.finditer(rf"\b{us}\b", t, flags=re.I):
                    trouves.append((f"US → {uk}", m.start(), m.end()))
        if a.politique_ize != "ignorer":
            for m in re.finditer(r"\b\w+(?:is|iz)(?:e|ed|es|ing|ation|ations)\b", t):
                mot = m.group(0).lower()
                if mot in ISE_LEGITIMES or mot.endswith(("ase", "ases", "lysis", "ysis")):
                    continue
                if a.politique_ize == "garder" and "is" in mot[-8:] and "iz" not in mot[-8:]:
                    trouves.append(("-ise → -ize (Oxford)", m.start(), m.end()))
                if a.politique_ize == "retirer" and "iz" in mot[-8:]:
                    trouves.append(("-ize → -ise", m.start(), m.end()))
        for mot in a.interdits:
            for m in re.finditer(rf"\b{re.escape(mot)}\w*\b", t, flags=re.I):
                trouves.append((f"mot surveillé « {mot} »", m.start(), m.end()))
        for nom, i, j in trouves:
            total += 1
            ctx = t[max(0, i - 35):j + 25]
            print(f"L{ligne_de(L, t[max(0, i - 20):i + 5])!s:>5} | {nom:35s} | …{ctx}…")
    print(f"\n{total} point(s) à regarder. Vérifiez chacun : certains sont légitimes "
          "(noms propres, titres, mots en contexte).")
