#!/usr/bin/env python3
"""
verifier_renvois_lettre.py : contrôle les numéros de ligne cités dans une lettre de réponse.

Le script repère dans la lettre toutes les mentions « line 123 », « lines 123–130 »
et « lines 120–122, 190 and 384 », puis affiche le texte trouvé à ces lignes
dans le manuscrit (fichier produit par pdf_lignes.py).
Il vérifie aussi que chaque phrase citée entre guillemets “…” dans la lettre
existe à l'identique dans le manuscrit (si --manuscrit est fourni).

Il ne juge pas à votre place : il vous montre ce qu'il faut relire.

Usage :
    python verifier_renvois_lettre.py lettre.docx lignes.txt
    python verifier_renvois_lettre.py lettre.docx lignes.txt --manuscrit manuscrit.docx
    python verifier_renvois_lettre.py lettre.txt lignes.txt --ignorer 300-304

--ignorer : plages qui renvoient à l'ANCIENNE version (citées par le reviewer), à ne pas contrôler.

Prérequis : pip install python-docx
"""
import argparse
import re


def lire_texte(chemin):
    if chemin.lower().endswith(".docx"):
        import docx
        return "\n".join(p.text for p in docx.Document(chemin).paragraphs)
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def lire_lignes(chemin):
    lignes = {}
    for l in open(chemin, encoding="utf-8"):
        m = re.match(r"\s*(\d+) \| (.*)", l)
        if m:
            lignes[int(m.group(1))] = m.group(2).rstrip()
    return lignes


def plages(texte):
    """Retourne la liste des (début, fin, contexte) cités dans la lettre."""
    res = []
    for m in re.finditer(r"\blines?\s+((?:\d+(?:\s*[–-]\s*\d+)?)(?:\s*(?:,|and|et)\s*\d+(?:\s*[–-]\s*\d+)?)*)", texte):
        ctx = texte[max(0, m.start() - 60):m.end() + 10].replace("\n", " ")
        for morceau in re.findall(r"\d+(?:\s*[–-]\s*\d+)?", m.group(1)):
            bornes = [int(x) for x in re.split(r"\s*[–-]\s*", morceau)]
            res.append((bornes[0], bornes[-1], ctx))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lettre", help="lettre de réponse (.docx ou .txt)")
    ap.add_argument("lignes", help="fichier de lignes produit par pdf_lignes.py (PDF FINAL)")
    ap.add_argument("--manuscrit", help="manuscrit .docx pour vérifier les citations entre guillemets")
    ap.add_argument("--ignorer", nargs="*", default=[], help="plages à ne pas contrôler, ex. 300-304")
    a = ap.parse_args()

    lettre = lire_texte(a.lettre)
    L = lire_lignes(a.lignes)
    ignore = {tuple(int(x) for x in p.split("-")) for p in a.ignorer}

    print("=== Renvois de ligne ===")
    for debut, fin, ctx in plages(lettre):
        if (debut, fin) in ignore:
            print(f"\n[ignoré] lignes {debut}-{fin} (ancienne version)")
            continue
        print(f"\n>>> lettre : …{ctx}…")
        for n in (debut, fin) if debut != fin else (debut,):
            print(f"    ligne {n:>4} : {L.get(n, '!!! LIGNE INTROUVABLE')}")

    if a.manuscrit:
        texte_ms = re.sub(r"\s+", " ", lire_texte(a.manuscrit))
        print("\n=== Citations entre guillemets ===")
        print("  (les commentaires des reviewers cités dans la lettre apparaîtront ABSENTE : c'est normal ;"
              " seules les phrases du MANUSCRIT citées dans vos réponses doivent être OK)")
        for c in re.findall(r"“([^”]{30,})”", lettre):
            c_norm = re.sub(r"\s+", " ", c).strip()
            ok = c_norm in texte_ms
            print(f"  {'OK ' if ok else 'ABSENTE'} : {c_norm[:100]}")
    print("\nRelisez chaque paire : le texte trouvé doit correspondre à ce que dit la lettre.")
