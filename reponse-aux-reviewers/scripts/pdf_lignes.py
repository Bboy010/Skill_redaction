#!/usr/bin/env python3
"""
pdf_lignes.py : reconstruit les lignes numérotées d'un manuscrit PDF.

Les revues demandent souvent une numérotation continue des lignes dans la marge.
Ce script associe chaque numéro de marge au texte situé à la même hauteur,
et écrit un fichier texte du type :
    123 | texte de la ligne 123

Les italiques sont signalés entre _soulignés_ (utile pour contrôler les noms latins).

Usage :
    python pdf_lignes.py manuscrit.pdf lignes.txt
    python pdf_lignes.py manuscrit.pdf lignes.txt --marge gauche

Prérequis : pip install pymupdf
"""
import argparse
import fitz  # PyMuPDF


def extraire(pdf, sortie, marge="auto", tolerance=3.5):
    doc = fitz.open(pdf)
    with open(sortie, "w", encoding="utf-8") as out:
        for no_page, page in enumerate(doc, 1):
            largeur = page.rect.width
            lignes = []
            for bloc in page.get_text("dict")["blocks"]:
                for l in bloc.get("lines", []):
                    texte = "".join(s["text"] for s in l["spans"])
                    if not texte.strip():
                        continue
                    x0, y0, x1, y1 = l["bbox"]
                    lignes.append(((y0 + y1) / 2, x0, texte, l["spans"]))

            def est_numero(x, t):
                if not t.strip().isdigit():
                    return False
                if marge == "droite":
                    return x > largeur * 0.85
                if marge == "gauche":
                    return x < largeur * 0.15
                return x > largeur * 0.85 or x < largeur * 0.15

            numeros = [(y, t.strip()) for y, x, t, _ in lignes if est_numero(x, t)]
            corps = [(y, x, t, sp) for y, x, t, sp in lignes if not est_numero(x, t)]
            out.write(f"\n##### PAGE {no_page}\n")
            for y, n in sorted(numeros):
                morceaux = []
                for yy, x, t, sp in sorted(corps, key=lambda c: c[1]):
                    if abs(yy - y) < tolerance:
                        for s in sp:
                            tx = s["text"]
                            if s["flags"] & 2 and tx.strip():  # bit 2 = italique
                                tx = "_" + tx + "_"
                            morceaux.append(tx)
                out.write(f"{n:>5} | {''.join(morceaux)}\n")
    print(f"Lignes écrites dans {sortie}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", help="PDF du manuscrit, avec numérotation des lignes")
    ap.add_argument("sortie", help="fichier texte à créer")
    ap.add_argument("--marge", choices=["auto", "droite", "gauche"], default="auto",
                    help="côté des numéros de ligne (défaut : auto)")
    ap.add_argument("--tolerance", type=float, default=3.5,
                    help="écart vertical maximal (en points) entre le numéro et le texte")
    a = ap.parse_args()
    extraire(a.pdf, a.sortie, a.marge, a.tolerance)
