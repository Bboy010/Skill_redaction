#!/usr/bin/env python3
"""
extraire_figures.py : extrait les images d'un .docx en pleine résolution,
avec la légende la plus proche (« Figure N. … »), écrite en entier dans un fichier .txt à côté de chaque image.

Le .docx n'est jamais modifié (lecture seule).
Chaque image est écrite dans le dossier de sortie sous un nom du type :
    fig_p046_image1.png      (p046 = numéro du paragraphe qui contient l'image)
    fig_p046_image1.txt      (texte complet de sa légende)

Usage :
    python extraire_figures.py manuscrit.docx dossier_images/
    python extraire_figures.py manuscrit.docx dossier_images/ --fenetre 8

Prérequis : pip install python-docx
"""
import argparse
import sys as _sys
try:  # consoles Windows : afficher flèches et accents sans UnicodeEncodeError
    _sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import docx
from docx.oxml.ns import qn


def extraire(chemin, sortie, fenetre=6):
    os.makedirs(sortie, exist_ok=True)
    d = docx.Document(chemin)
    paras = d.paragraphs
    n = 0
    for i, p in enumerate(paras):
        for blip in p._p.iter(qn("a:blip")):
            rid = blip.get(qn("r:embed"))
            if rid not in d.part.related_parts:
                continue  # image liée (non incorporée) : rien à extraire
            part = d.part.related_parts[rid]
            nom = part.partname.split("/")[-1]
            fichier = os.path.join(sortie, f"fig_p{i:03d}_{nom}")
            with open(fichier, "wb") as f:
                f.write(part.blob)
            # légende : premier paragraphe « Figure … » dans la fenêtre qui suit l'image
            legende = next((q.text for q in paras[i:i + fenetre]
                            if q.text.strip().startswith(("Figure", "Fig.", "Table"))), None)
            txt = os.path.splitext(fichier)[0] + ".txt"
            with open(txt, "w", encoding="utf-8") as f:
                f.write((legende or "(légende non trouvée)") + "\n")
            n += 1
            vu = legende[:90] + ("…" if len(legende) > 90 else "") if legende else "(légende non trouvée)"
            print(f"{os.path.basename(fichier):35s} {len(part.blob)/1024:8.0f} Ko | {vu}")
    print(f"\n{n} image(s) extraite(s) dans {sortie}, chacune avec sa légende complète dans un .txt du même nom")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx", help="manuscrit .docx (lu, jamais modifié)")
    ap.add_argument("sortie", help="dossier où écrire les images")
    ap.add_argument("--fenetre", type=int, default=6, help="nombre de paragraphes après l'image où chercher la légende")
    a = ap.parse_args()
    extraire(a.docx, a.sortie, a.fenetre)
