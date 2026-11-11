#!/usr/bin/env python3
"""
audit_zotero.py : audit des citations Zotero d'un manuscrit Word (style numéroté [1], [2]…).

LECTURE SEULE : le .docx n'est jamais modifié. Fermez-le dans Word avant de lancer le script.

Contrôles :
  1. numéros tapés à la main (hors champs Zotero) ;
  2. texte affiché du champ différent de la valeur enregistrée par Zotero ;
  3. chaque article cité (titre / DOI dans les données du champ) → numéro de la bibliographie ;
     signale les appels qui affichent un AUTRE numéro (citations restées à l'ancien numéro) ;
  4. références orphelines (jamais citées) et manquantes (citées mais absentes) ;
  5. ordre de première citation croissant ;
  6. balises de travail restantes « [ZOTERO: … ] ».

Chaque problème est affiché avec 40 caractères de texte avant et après la citation,
et avec son numéro de ligne du PDF si --lignes est donné (fichier produit par pdf_lignes.py).

Usage :
    python audit_zotero.py manuscrit.docx
    python audit_zotero.py manuscrit.docx --lignes lignes.txt
    python audit_zotero.py manuscrit.docx --style-biblio Bibliography --json rapport.json

Prérequis : pip install python-docx
"""
import argparse
import sys as _sys
try:  # consoles Windows : afficher flèches et accents sans UnicodeEncodeError
    _sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import json
import re
import unicodedata
import docx
from docx.oxml.ns import qn
from docx.text.run import Run

W = lambda t: qn("w:" + t)
CONTEXTE = 40  # caractères affichés avant et après une citation


# ---------- lignes du PDF (mêmes fonctions dans controles_langue.py et residus_docx.py)
def charger_lignes(chemin):
    """Lignes numérotées du PDF (fichier produit par pdf_lignes.py), dans l'ordre : [(numéro, texte)]."""
    L = []
    if chemin:
        for l in open(chemin, encoding="utf-8"):
            m = re.match(r"\s*(\d+) \| (.*)", l)
            if m:
                L.append((int(m.group(1)), m.group(2).replace("_", "")))
    return L


def index_lignes(L):
    """Toutes les lignes mises bout à bout (espaces normalisés), avec le numéro de ligne de chaque caractère.
    Un saut de ligne compte pour un espace, sauf après un trait d'union (mot coupé en fin de ligne)."""
    morceaux, proprio = [], []
    for n, t in L:
        t = re.sub(r"\s+", " ", t).strip()
        if morceaux and not morceaux[-1].endswith("-"):
            morceaux.append(" "); proprio.append(n)
        morceaux.append(t); proprio.extend([n] * len(t))
    return "".join(morceaux), proprio


def tasser(s):
    """Réduit chaque suite d'espaces à un espace ; garde la position d'origine de chaque caractère."""
    out, ou = [], []
    for i, c in enumerate(s):
        if c.isspace():
            if out and out[-1] == " ":
                continue
            c = " "
        out.append(c); ou.append(i)
    return "".join(out), ou


def ligne_de(index, para, pos):
    """Ligne du PDF où tombe le caractère `pos` du texte de paragraphe `para`.
    On cherche le plus long extrait autour de `pos` dans les lignes mises bout à bout ; le résultat porte
    « (approx.) » si seul un extrait court (moins de 25 caractères) correspond, ou si l'extrait est trouvé plusieurs fois."""
    texte, proprio = index
    if not texte or not para:
        return "?"
    tas, ou = tasser(para)
    k = next((j for j, w in enumerate(ou) if w >= pos), len(tas) - 1)
    for demi in (60, 40, 25, 12):
        a, b = max(0, k - demi), min(len(tas), k + demi)
        morceau = tas[a:b]
        extrait = morceau.strip()
        if len(extrait) < 8:
            continue
        tete = len(morceau) - len(morceau.lstrip())
        trouves = [m.start() for m in re.finditer(re.escape(extrait), texte)]
        if trouves:
            at = min(max(trouves[0] + (k - a - tete), 0), len(proprio) - 1)
            exact = len(trouves) == 1 and len(extrait) >= 25
            return proprio[at] if exact else f"{proprio[at]} (approx.)"
    return "?"


# ---------- Zotero
def normaliser(s):
    """minuscules, sans accents ni ponctuation : pour comparer des titres."""
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def numeros(texte):
    """'[3,5–7]' -> [3, 5, 6, 7]"""
    out = []
    texte = texte.replace("\\uc0\\u8211{}", "–")
    for tok in texte.strip().strip("[]").split(","):
        m = re.fullmatch(r"\s*(\d+)\s*[–-]\s*(\d+)\s*", tok)
        if m:
            out += list(range(int(m.group(1)), int(m.group(2)) + 1))
        elif tok.strip().isdigit():
            out.append(int(tok))
    return out


def parcourir(d):
    """Lit chaque paragraphe une fois.
    Renvoie les champs complexes (indice du paragraphe, instruction, texte affiché, début, fin, texte du paragraphe)
    et, pour chaque paragraphe, son texte et le texte situé hors des champs (avec les positions d'origine)."""
    champs, paras = [], []
    for i, p in enumerate(d.paragraphs):
        complet, dehors, ou = "", "", []
        prof, etat, instr, debut = 0, None, [], 0
        for r in p._p.iter(W("r")):
            fc = r.find(W("fldChar"))
            if fc is not None:
                t = fc.get(W("fldCharType"))
                if t == "begin":
                    prof += 1
                    if prof == 1:
                        etat, instr = "instr", []
                elif t == "separate":
                    if prof == 1:
                        etat, debut = "resultat", len(complet)
                elif t == "end":
                    if prof == 1 and instr:
                        champs.append([i, "".join(instr), complet[debut:], debut, len(complet)])
                    prof = max(0, prof - 1)
                    if prof == 0:
                        etat = None
                continue
            if etat == "instr":
                it = r.find(W("instrText"))
                if it is not None:
                    instr.append(it.text or "")
                continue
            txt = Run(r, p).text
            if prof == 0:
                dehors += txt
                ou += range(len(complet), len(complet) + len(txt))
            complet += txt
        paras.append((complet, dehors, ou))
    for c in champs:
        c.append(paras[c[0]][0])
    return champs, paras


def autour(texte, debut, fin):
    return "…" + texte[max(0, debut - CONTEXTE):fin + CONTEXTE] + "…"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("--lignes", help="fichier de lignes du PDF (pdf_lignes.py), pour donner la ligne de chaque problème")
    ap.add_argument("--style-biblio", default="Bibliography", help="nom du style Word des entrées de bibliographie")
    ap.add_argument("--json", help="écrire le rapport dans ce fichier JSON")
    a = ap.parse_args()

    d = docx.Document(a.docx)
    index = index_lignes(charger_lignes(a.lignes))
    ou_est = (lambda texte, pos: ligne_de(index, texte, pos)) if a.lignes else None
    tous, paras = parcourir(d)
    cits = [c for c in tous if "ZOTERO_ITEM" in c[1]]
    biblio = {int(m.group(1)): p.text for p in d.paragraphs if p.style.name == a.style_biblio
              for m in [re.match(r"\s*\[?(\d+)[\].]\s", p.text)] if m}
    problemes, vus, ordre = [], set(), []

    def lieu(i, texte, debut):
        info = {"paragraphe": i}
        if ou_est:
            info["ligne"] = ou_est(texte, debut)
        return info

    for i, instr, vu, debut, fin, texte in cits:
        js = json.loads(instr[instr.index("{"): instr.rindex("}") + 1])
        enregistre = js.get("properties", {}).get("plainCitation", "")
        if vu.strip() != enregistre.strip():
            problemes.append({"type": "affiché ≠ enregistré", **lieu(i, texte, debut), "affiché": vu, "enregistré": enregistre,
                              "contexte": autour(texte, debut, fin)})
        ns = numeros(enregistre)
        for item in js.get("citationItems", []):
            data = item.get("itemData", {})
            titre, doi = normaliser(data.get("title", ""))[:40], (data.get("DOI") or "").lower()
            cand = [k for k, v in biblio.items() if (doi and doi in v.lower()) or (titre and titre in normaliser(v))]
            if not cand:
                problemes.append({"type": "article absent de la bibliographie", **lieu(i, texte, debut),
                                  "titre": data.get("title", "")[:60], "contexte": autour(texte, debut, fin)})
            elif not set(cand) & set(ns):
                problemes.append({"type": "appel → autre numéro (ancien numéro ?)", **lieu(i, texte, debut),
                                  "affiché": enregistre, "entrée attendue": cand, "titre": data.get("title", "")[:60],
                                  "contexte": autour(texte, debut, fin)})
        for x in ns:
            if x not in vus:
                vus.add(x); ordre.append(x)

    tapes = []
    for i, p in enumerate(d.paragraphs):
        if p.style.name == a.style_biblio:
            continue
        complet, dehors, ou = paras[i]
        for m in re.finditer(r"\[\d[\d,–\- ]*\]", dehors):
            s, e = ou[m.start()], ou[m.end() - 1] + 1
            tapes.append({**lieu(i, complet, s), "numéro": m.group(0), "contexte": autour(complet, s, e)})
    balises = sum(p.text.count("[ZOTERO:") for p in d.paragraphs)
    orphelines = sorted(set(biblio) - vus)
    manquantes = sorted(vus - set(biblio))
    continue_ = sorted(biblio) == list(range(1, len(biblio) + 1))

    print(f"Champs de citation Zotero : {len(cits)} | bibliographie : {len(biblio)} entrées (numérotation continue : {continue_})")
    print(f"Numéros distincts cités : {len(vus)} | orphelines : {orphelines} | manquantes : {manquantes}")
    print(f"Ordre de première citation croissant : {ordre == sorted(ordre)}")
    print(f"Numéros tapés à la main : {len(tapes)} | balises [ZOTERO: …] restantes : {balises}")
    for t in tapes:
        print("  tapé à la main | " + " | ".join(f"{k}: {v}" for k, v in t.items()))
    print(f"Problèmes : {len(problemes)}")
    for pb in problemes:
        print("  " + " | ".join(f"{k}: {v}" for k, v in pb.items()))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"champs": len(cits), "biblio": len(biblio), "orphelines": orphelines, "manquantes": manquantes,
                       "ordre_croissant": ordre == sorted(ordre), "tapes_main": tapes, "balises": balises,
                       "problemes": problemes}, f, ensure_ascii=False, indent=2)
        print(f"Rapport JSON : {a.json}")
