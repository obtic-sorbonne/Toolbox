#!/usr/bin/env python3
"""description:
  Transforme un ensemble de fichiers textes en TEI en cherchant les métadonnées
  dans un fichier ods.

exemples d'utilisation:
  python ./corpus_to_tei.py -h
  python ./corpus_to_tei.py donnees-corrigees metadata.ods
"""

# authors: Arthur Provenier, Yoann Dupont


import uuid
import pathlib
from datetime import date

from lxml import etree
from lxml.builder import ElementMaker

from pyexcel_ods import get_data


def licence_link(licence):
    l = licence.lower()

    if l.startswith("cc ") or l.startswith("cc-"):
        l = l[3:]

    if l.startswith("by"):
        return f"https://creativecommons.org/licenses/{l}/4.0/"

    return licence  # other licences will keep their name



def corpus_to_tei(
    corpus_path,
    ods_path,
    ext=".txt",
    output_path="output",
    responsibility=None,
    editor=None,
    edition=None,
    licence="by-nc-sa",
):
    """Convertit chaque fichier d'un dossier en TEI. Seuls les fichiers ayant
    la bonne extension seront convertis. Les fichiers TEI générés seront écrits
    dans le même dossier de sortie.

    Parameters
    ----------
    corpus_path : str
        le chemin vers le dossier contenant les fichiers à convertir
    ods_path : str
        le chemin vers le fichier de métadonnées
    ext : str, default=".txt"
        l'extension des fichiers à convertir. Par défaut: ".txt"
    output_path : str
        le dossier de sortie, doit exister au préalable
    """

    corpus_path = pathlib.Path(corpus_path)
    E = ElementMaker(
        namespace="http://www.tei-c.org/ns/1.0", nsmap={None: "http://www.tei-c.org/ns/1.0"}
    )

    missingcorpusfiles = set(path.name for path in corpus_path.glob(f"*{ext}"))
    missingmetadatafiles = set()

    folder = pathlib.Path(output_path)
    if not folder.exists():
        raise FileNotFoundError(
            f"Le dossier '{folder.absolute()}' n'existe pas: vous devez le créer."
        )

    data = get_data(ods_path)
    for i, row in enumerate(data["Sheet1"]):
        if i == 0:
            continue

        try:
            # filename, author, toptitle, title, proj, cat, publisher, pub_date, lang = row
            filename, author, toptitle, title, rate, proj, cat, publisher, pub_date, lang = row
            filename = filename.replace("'", "")
            file_ = f"{filename.strip()}{ext}"
        except ValueError as ve:
            print(f"Erreur à la ligne {i+1}: '{ve}'")
            continue

        if lang == "français":
            lang = "fre"

        try:
            with open(corpus_path / file_, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            # print(f"Fichier {corpus_path}/{file_} non trouvé")
            missingmetadatafiles.add(file_)
            continue

        missingcorpusfiles.remove(file_)

        teifile = E.TEI(
            E.teiHeader(
                E.fileDesc(
                    E.titleStmt(E.title(f"{toptitle}"), E.author(f"{author}")),
                    E.editionStmt(
                        E.edition(edition or "{edition}"),  # formerly: "Thèse de doctorat"
                        E.respStmt(E.resp(), E.name(responsibility or "{responsibility}")),  # formerly: FirstName LastName
                    ),
                    E.publicationStmt(
                        E.publisher(editor or "{editor}"),  # formerly: "OBVIL"
                        E.date(when=str(date.today().year)),
                        E.idno(),
                        E.availability(
                            E.licence(
                                f"Licence {licence}", target=licence_link(licence)
                            ),
                            status="restricted",
                        ),
                    ),
                    E.sourceDesc(E.bibl()),
                ),
                E.profileDesc(
                    E.creation(E.date(when=f"{'-'.join(pub_date.split('/')[::-1])}")),
                    E.langUsage(E.language(ident=f"{lang}")),
                    E.textClass(
                        E.keywords(
                            E.term(f"{toptitle}", type="topTitle"),
                            E.term(f"{proj}", type="project"),
                            E.term(f"{uuid.uuid4().hex}", type="id"),
                            E.term(
                                f"{toptitle}", type="title"
                            ),  # Modifier ici et mettre 'title' à la place de 'toptitle'
                            E.term(editor or "{editor}", type="edition"),  # formerly: "OBVIL"
                            E.term(f"{publisher}", type="publisher"),
                            E.term(f"{author}", type="author"),
                            E.term(type="recipient"),
                            E.term(f"{pub_date}", type="date"),
                            scheme="indexation",
                        )
                    ),
                ),
            ),
            E.text(E.body(E.div(*[E.p(t.strip()) for t in text.split("\n") if t.strip()]))),
        )

        f = f"{folder}/{filename}.xml"
        with open(f, "wb") as fout:
            fout.write(
                etree.tostring(teifile, xml_declaration=True, pretty_print=True, encoding="UTF-8")
            )

    print()
    print(f"Les fichiers suivants du corpus '{corpus_path}' n'ont pas de métadonnées '{ods_path}':")
    for item in sorted(missingcorpusfiles):
        print(f"\t{item}")
    print()
    print(
        f"Les fichiers suivants des métadonnées '{ods_path}' sont absents du corpus '{corpus_path}':"
    )
    for item in sorted(missingmetadatafiles):
        print(f"\t{item}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("corpus_path", help="donnees-corrigees")
    parser.add_argument("ods_path", help="metadata.ods")
    parser.add_argument("-e", "--ext", default=".txt", help="")
    parser.add_argument("-o", "--output-path", default="output", help="")
    parser.add_argument("-r", "--responsibility", help="Who has responsibility?")
    parser.add_argument("--editor", help="Who is the editor?")
    parser.add_argument("--edition", help="What is the edition?")
    parser.add_argument("--licence", default="by-nc-sa", help="What is the licence? (default: by-nc-sa)")

    args = parser.parse_args()

    corpus_to_tei(**vars(args))
