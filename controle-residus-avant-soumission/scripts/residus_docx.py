#!/usr/bin/env python3
"""
residus_docx.py : contrôle technique d'un manuscrit .docx avant soumission (LECTURE SEULE).

Recherche :
  * modifications suivies (ins, del, déplacements, changements de mise en forme) et commentaires ;
  * texte masqué, surlignage, trame de fond ;
  * balises de travail : [ZOTERO: …], TODO, FIXME, XX, ???, « à vérifier », « Author: » ;
  * champs incomplets (begin/separate/end), « Error! », signets ;
  * typographie : doubles espaces, espace avant ponctuation fermante, ponctuation doublée,
    parenthèses et crochets non appariés ;
  * police effective différente de --police (corps et bibliographie) ;
  * langues de vérification présentes (w:lang) ;
  * ordre de première citation des Figures, Tables et éléments supplémentaires
    (les légendes « Figure N. … » sont exclues ; les plages « S1–S6 » sont traitées comme des plages).

Usage :
  python residus_docx.py manuscrit.docx
  python residus_docx.py manuscrit.docx --lignes lignes.txt --police "Times New Roman"

Prérequis : pip install python-docx
"""
import argparse
import collections
import re
import zipfile
import docx
from docx.oxml.ns import qn

W = lambda t: qn("w:" + t)


def lignes(chemin):
    L = {}
    if chemin:
        for l in open(chemin, encoding="utf-8"):
            m = re.match(r"\s*(\d+) \| (.*)", l)
            if m:
                L[int(m.group(1))] = m.group(2).replace("_", "")
    return L


def ligne_de(L, extrait):
    for n in (25, 14):
        s = extrait.strip()[:n]
        for k in sorted(L):
            if s and s in L[k]:
                return k
    return "?"


def police_effective(p, r):
    if r.font.name:
        return r.font.name
    st = p.style
    while st is not None:
        if st.font.name:
            return st.font.name
        st = st.base_style
    return "(défaut/thème)"


def deplier(seq):
    """'S1–S6' -> ['S1',…,'S6'] ; '2 and 3' -> ['2','3']"""
    out = []
    for m in re.finditer(r"(S?)(\d+)(?:\s*[–-]\s*S?(\d+))?", seq):
        pre, a, b = m.group(1), int(m.group(2)), m.group(3)
        out += [f"{pre}{x}" for x in range(a, int(b) + 1)] if b else [f"{pre}{a}"]
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("--lignes", help="fichier de lignes (pdf_lignes.py)")
    ap.add_argument("--police", default="Times New Roman", help="police attendue")
    ap.add_argument("--style-biblio", default="Bibliography")
    a = ap.parse_args()

    L = lignes(a.lignes)
    z = zipfile.ZipFile(a.docx)
    xml = z.read("word/document.xml").decode("utf-8")
    d = docx.Document(a.docx)
    paras = d.paragraphs
    corps = [p for p in paras if p.style.name != a.style_biblio]
    alertes = []

    def dire(cat, quoi, ligne="-"):
        alertes.append((cat, ligne, quoi))

    # 1. suivi, commentaires, masqué
    for balise, nom in (("<w:ins ", "insertion suivie"), ("<w:del ", "suppression suivie"), ("<w:moveFrom ", "déplacement suivi"),
                        ("<w:rPrChange", "mise en forme suivie"), ("<w:pPrChange", "paragraphe suivi"),
                        ("<w:commentRangeStart", "commentaire"), ("<w:vanish/>", "texte masqué")):
        n = xml.count(balise)
        if n:
            dire("technique", f"{n} × {nom}")
    if [n for n in z.namelist() if "comments" in n]:
        dire("technique", "partie 'commentaires' présente dans le fichier")
    for p in corps:
        for r in p.runs:
            rpr = r._r.find(W("rPr"))
            if rpr is None or not r.text.strip():
                continue
            if rpr.find(W("highlight")) is not None:
                dire("technique", f"surlignage : {r.text[:40]!r}", ligne_de(L, p.text[:40]))
            shd = rpr.find(W("shd"))
            if shd is not None and (shd.get(W("fill")) or "auto").lower() not in ("auto", "ffffff"):
                dire("technique", f"trame de fond : {r.text[:40]!r}", ligne_de(L, p.text[:40]))

    # 2. balises de travail
    for p in corps:
        for m in re.finditer(r"\[ZOTERO:[^\]]*\]|\bTODO\b|\bFIXME\b|\bXXX?\b|\?\?\?|à vérifier|à corriger|\bAuthor:", p.text):
            dire("balise", f"{m.group(0)!r} dans « {p.text[max(0, m.start()-30):m.end()+20]} »", ligne_de(L, p.text[max(0, m.start()-20):m.start()+5]))

    # 3. champs et signets
    fc = collections.Counter(e.get(W("fldCharType")) for e in d.element.body.iter(W("fldChar")))
    if not (fc["begin"] == fc["separate"] == fc["end"]):
        dire("technique", f"champs incomplets : begin/separate/end = {fc['begin']}/{fc['separate']}/{fc['end']}")
    if any("Error!" in p.text for p in paras):
        dire("technique", "texte « Error! » (champ cassé)")
    sig = [e.get(W("name")) for e in d.element.body.iter(W("bookmarkStart"))]
    fins = len(list(d.element.body.iter(W("bookmarkEnd"))))
    if len(sig) != fins:
        dire("technique", f"signets non appariés : {len(sig)} débuts / {fins} fins")

    # 4. typographie
    regles = {"double espace": r"(?<=\S)  +(?=\S)", "espace avant ponctuation": r"\s+[\)\],;:](?!\d)|\s+\.(?!\d)",
              "ponctuation doublée": r"(?<!\.)\.\.(?!\.)|,,|;;|[a-z]\.\s\((?![a-z]\))"}
    for p in corps:
        t = p.text
        for nom, motif in regles.items():
            for m in re.finditer(motif, t):
                ctx = t[max(0, m.start() - 30):m.end() + 20]
                if re.search(r"\b(e\.g|i\.e|et al)\.", ctx):
                    continue
                dire("typographie", f"{nom} : …{ctx}…", ligne_de(L, t[max(0, m.start()-20):m.start()+5]))
        for o, f in (("(", ")"), ("[", "]")):
            if t.count(o) != t.count(f):
                dire("typographie", f"{o}{f} non appariés ({t.count(o)} / {t.count(f)}) : {t[:70]!r}", ligne_de(L, t[:40]))

    # 5. polices et langues
    polices = collections.Counter()
    for p in paras:
        for r in p.runs:
            if r.text.strip():
                polices[(p.style.name == a.style_biblio, police_effective(p, r))] += len(r.text)
    autres = {k: v for k, v in polices.items() if k[1] != a.police}
    if autres:
        dire("police", f"caractères hors {a.police} (biblio?, police) : {autres}")
    langues = collections.Counter(e.get(W("val")) for e in d.element.body.iter(W("lang")) if e.get(W("val")))
    if langues:
        dire("langue", f"langues de vérification : {dict(langues)} (invisible dans le PDF, visible dans un document suivi)")

    # 6. ordre des renvois
    debut = next((i for i, p in enumerate(corps) if re.match(r"\s*1\.?\s+Introduction", p.text)), 0)
    premiers = collections.defaultdict(list)
    for p in corps[debut:]:
        if re.match(r"(Figure|Table|Fig\.) S?\d+\.", p.text):
            continue  # légende
        # un élément de liste n'est retenu que s'il est suivi d'une ponctuation ou de « and »
        # (évite de lire « Table S3, 13 MAGs » comme « Tables S3 et 13 »)
        for m in re.finditer(r"(Supplementary\s+)?(Figures?|Tables?|Data)\s+((?:S?\d+)(?:\s*(?:,|and|–|-)\s*S?\d+(?=\s*(?:,|and\b|–|-|\)|;|\.|$)))*)", p.text):
            genre = "Table" if "Table" in m.group(2) else ("Data" if m.group(2) == "Data" else "Figure")
            for x in deplier(m.group(3)):
                cle = (genre, x.startswith("S"))
                if x not in premiers[cle]:
                    premiers[cle].append(x)
    for (genre, supp), seq in sorted(premiers.items()):
        nums = [int(x.lstrip("S")) for x in seq]
        etat = "OK" if nums == sorted(nums) else "ORDRE NON CROISSANT"
        dire("ordre", f"{genre}{' S' if supp else ''} : {seq} → {etat}")

    for cat in ("technique", "balise", "typographie", "police", "langue", "ordre"):
        items = [x for x in alertes if x[0] == cat]
        print(f"\n===== {cat} ({len(items)})")
        for _, ligne, quoi in items:
            print(f"  L{ligne!s:>5} | {quoi}")
    print("\nRien dans une catégorie = rien trouvé. Vérifiez chaque point avant de corriger (certains sont légitimes).")
