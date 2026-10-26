#!/usr/bin/env python3
"""
metadonnees.py : affiche les métadonnées de fichiers .docx et .pdf et repère ce qui pourrait
révéler des informations non souhaitées (LECTURE SEULE).

Pour un .docx :
  auteur, dernier modificateur, titre, sujet, mots-clés, description, dates,
  société, modèle Word, auteurs des révisions,
  et recherche de chemins locaux (C:\\Users, /home/, file:///…) dans toutes les parties XML.
Pour un .pdf :
  auteur, titre, sujet, mots-clés, logiciel créateur, dates.

Option --chercher : mots supplémentaires à rechercher (nom du laboratoire, nom de compte…).

Usage :
  python metadonnees.py manuscrit.docx lettre.docx manuscrit.pdf
  python metadonnees.py *.docx --chercher "PC-LABO" "MonNom"

Prérequis : pip install pymupdf (pour les PDF)
"""
import argparse
import re
import zipfile

MOTIFS_CHEMIN = [r"[A-Za-z]:\\Users\\", r"[A-Za-z]:/Users/", r"/home/[^/\s\"<]+", r"/Users/[^/\s\"<]+", r"file:///", r"\\Downloads\\", r"\\Desktop\\"]


def docx_meta(chemin, chercher):
    z = zipfile.ZipFile(chemin)
    core = z.read("docProps/core.xml").decode("utf-8") if "docProps/core.xml" in z.namelist() else ""
    app = z.read("docProps/app.xml").decode("utf-8") if "docProps/app.xml" in z.namelist() else ""
    g = lambda tag, s: (re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", s, re.S) or [None, ""])[1]
    print(f"\n=== {chemin}")
    for etiquette, tag, src in (("auteur", "dc:creator", core), ("dernier modificateur", "cp:lastModifiedBy", core),
                                ("titre", "dc:title", core), ("sujet", "dc:subject", core), ("mots-clés", "cp:keywords", core),
                                ("description", "dc:description", core), ("créé", "dcterms:created", core),
                                ("modifié", "dcterms:modified", core), ("société", "Company", app), ("modèle", "Template", app),
                                ("responsable", "Manager", app)):
        v = g(tag, src)
        if v:
            print(f"  {etiquette:22s}: {v}")
    doc = z.read("word/document.xml").decode("utf-8", "ignore")
    auteurs = sorted(set(re.findall(r'w:author="([^"]*)"', doc)))
    if auteurs:
        print(f"  auteurs des révisions : {auteurs}")
    trouves = []
    for n in z.namelist():
        if not n.endswith((".xml", ".rels")):
            continue
        s = z.read(n).decode("utf-8", "ignore")
        for motif in MOTIFS_CHEMIN + [re.escape(c) for c in chercher]:
            for m in re.finditer(motif, s):
                trouves.append((n, s[max(0, m.start() - 20):m.end() + 40].replace("\n", " ")))
    print(f"  chemins locaux / mots recherchés : {len(trouves)}")
    for n, ctx in trouves[:15]:
        print(f"    {n} : …{ctx}…")


def pdf_meta(chemin, chercher):
    import fitz
    d = fitz.open(chemin)
    print(f"\n=== {chemin} ({len(d)} pages)")
    for k, v in d.metadata.items():
        if v:
            print(f"  {k:22s}: {v}")
    texte_meta = " ".join(str(v) for v in d.metadata.values() if v)
    for c in chercher:
        if c.lower() in texte_meta.lower():
            print(f"  !!! « {c} » présent dans les métadonnées")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichiers", nargs="+")
    ap.add_argument("--chercher", nargs="*", default=[], help="mots à rechercher en plus (nom de compte, laboratoire…)")
    a = ap.parse_args()
    for f in a.fichiers:
        if f.lower().endswith(".docx"):
            docx_meta(f, a.chercher)
        elif f.lower().endswith(".pdf"):
            pdf_meta(f, a.chercher)
        else:
            print(f"\n=== {f} : format non pris en charge")
    print("\nÀ nettoyer dans Word : Fichier → Informations → Inspecter le document → "
          "Propriétés du document et informations personnelles → Supprimer.")
