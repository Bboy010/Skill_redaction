#!/usr/bin/env python3
"""
agreger_tableau.py : recalcule un chiffre (somme, moyenne, compte, médiane) à partir d'un tableau brut.

But : remplacer « je reprends le chiffre de l'ancienne version » par « je le recalcule ».
La commande utilisée est affichée, pour pouvoir la recopier dans vos notes.

Formats lus : .tsv, .csv, .txt (tabulations), .xlsx (première feuille).
Si le fichier n'a pas d'en-tête, utilisez --colonnes pour nommer les colonnes.

Exemples :
  # moyenne de la colonne CE par compartiment
  python agreger_tableau.py genes.tsv --groupe compartiment --valeur CE --operation mean

  # somme de CE pour les lignes où genre est vide
  python agreger_tableau.py genes.tsv --valeur CE --operation sum --filtre "genre="

  # fichier long sans en-tête : genome, classe, nombre -> on pivote d'abord.
  # Regroupement par motif sur le nom : (?:...) = un seul groupe « correspond » / « autre » ;
  # (...) avec capture = un groupe par valeur capturée.
  python agreger_tableau.py long.tsv --colonnes genome classe nombre \
      --pivot-index genome --pivot-cle classe --pivot-valeur nombre \
      --valeur CE --operation mean --manquant-zero --groupe-regex "genome=^(?:SiteA_2|SiteB_1)"

Valeurs absentes après pivot : sans --manquant-zero elles sont ignorées (moyenne sur ceux qui ont la valeur) ;
avec --manquant-zero elles comptent pour 0 (moyenne sur tous). Les deux donnent des chiffres différents.

Filtres (--filtre, répétable) :
  col=valeur   égalité stricte (col= signifie « vide »)
  col!=valeur  différent
  col~regex    correspond à l'expression régulière
"""
import argparse
import csv
import re
import statistics
import sys
from collections import defaultdict


def lire(chemin, colonnes=None):
    if chemin.lower().endswith(".xlsx"):
        import openpyxl
        ws = openpyxl.load_workbook(chemin, read_only=True, data_only=True).active
        lignes = [["" if v is None else str(v) for v in r] for r in ws.iter_rows(values_only=True)]
    else:
        sep = "," if chemin.lower().endswith(".csv") else "\t"
        with open(chemin, encoding="utf-8", newline="") as f:
            lignes = [r for r in csv.reader(f, delimiter=sep)]
    if colonnes:
        entete, data = colonnes, lignes
    else:
        entete, data = lignes[0], lignes[1:]
    return [dict(zip(entete, r)) for r in data if any(c.strip() for c in r)]


def pivoter(rows, index, cle, valeur):
    """Format long -> large : une ligne par index, une colonne par valeur de 'cle'."""
    large = defaultdict(dict)
    for r in rows:
        large[r[index]][index] = r[index]
        large[r[index]][r[cle]] = r[valeur]
    return list(large.values())


def garder(r, filtres):
    for f in filtres:
        if "!=" in f:
            c, v = f.split("!=", 1)
            if r.get(c, "") == v:
                return False
        elif "~" in f:
            c, v = f.split("~", 1)
            if not re.search(v, r.get(c, "") or ""):
                return False
        elif "=" in f:
            c, v = f.split("=", 1)
            if (r.get(c, "") or "") != v:
                return False
    return True


def nombre(x):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichier")
    ap.add_argument("--colonnes", nargs="*", help="noms de colonnes si le fichier n'a pas d'en-tête")
    ap.add_argument("--pivot-index"); ap.add_argument("--pivot-cle"); ap.add_argument("--pivot-valeur")
    ap.add_argument("--valeur", help="colonne numérique à agréger (inutile pour --operation count)")
    ap.add_argument("--operation", choices=["sum", "mean", "count", "median", "min", "max"], default="sum")
    ap.add_argument("--groupe", help="colonne de regroupement")
    ap.add_argument("--groupe-regex", help="regroupement par motif : 'colonne=regex' (le 1er groupe capturé sert d'étiquette)")
    ap.add_argument("--filtre", action="append", default=[], help="voir l'aide en tête du fichier")
    ap.add_argument("--manquant-zero", action="store_true", help="compter une valeur absente comme 0 (sinon elle est ignorée)")
    a = ap.parse_args()

    rows = lire(a.fichier, a.colonnes)
    if a.pivot_cle:
        rows = pivoter(rows, a.pivot_index, a.pivot_cle, a.pivot_valeur)
    rows = [r for r in rows if garder(r, a.filtre)]

    groupes = defaultdict(list)
    for r in rows:
        if a.groupe_regex:
            col, rx = a.groupe_regex.split("=", 1)
            m = re.search(rx, r.get(col, "") or "")
            g = (m.group(1) if m and m.groups() else ("correspond" if m else "autre"))
        elif a.groupe:
            g = r.get(a.groupe, "")
        else:
            g = "(tout)"
        groupes[g].append(r)

    print("Commande :", " ".join(sys.argv))
    print(f"Lignes retenues après filtres : {len(rows)}")
    for g, rs in sorted(groupes.items()):
        if a.operation == "count":
            print(f"  {g!s:25s} n = {len(rs)}")
            continue
        vals = []
        for r in rs:
            v = nombre(r.get(a.valeur))
            if v is None and a.manquant_zero:
                v = 0.0
            if v is not None:
                vals.append(v)
        if not vals:
            print(f"  {g!s:25s} aucune valeur numérique"); continue
        f = {"sum": sum, "mean": statistics.mean, "median": statistics.median, "min": min, "max": max}[a.operation]
        print(f"  {g!s:25s} {a.operation} = {f(vals):.4g}   (n valeurs = {len(vals)}, n lignes = {len(rs)})")
