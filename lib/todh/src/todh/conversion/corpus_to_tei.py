"""description:
    Transforme un ensemble de fichiers textes en TEI en cherchant les métadonnées
    dans un fichier ods.

exemples d'utilisation (code):
>>> import todh.conversion.corpus_to_tei as corpus_to_tei
>>> corpus_to_tei("path/to/corpusfolder/", "path/to/odsfile", output_dir="./out/")

exemples d'utilisation (terminal):
    python corpus_to_tei.py -h
    python corpus_to_tei.py donnees-corrigees metadata.ods
"""

__author__ = "Arthur Provenier, Yoann Dupont"
__licence__ = "MIT"


import uuid
import pathlib
from datetime import date
import csv

from lxml import etree
from lxml.builder import ElementMaker

from pyexcel_ods import get_data

from todh.conversion.utils import cc_licence_link
from todh.conversion.tei import text_to_tei


def run(
    corpus_dir,
    metadata_file,
    ext=".txt",
    output_dir="./output/",
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
    corpus_dir : str
        le chemin vers le dossier contenant les fichiers à convertir
    metadata_file : str
        le chemin vers le fichier de métadonnées (.ods / .tsv)
    ext : str, default=".txt"
        l'extension des fichiers à convertir. Par défaut: ".txt"
    output_dir : str
        le dossier de sortie, doit exister au préalable
    responsibility : str
        la personne responsable. Par defaut: None
    editor
        l'éditeur. Par defaut: None
    edition
        l'édition. Par defaut: None
    licence
        la licence à attribuer aux fichiers construits. Par defaut: "by-nc-sa"
    """

    corpus_path = pathlib.Path(corpus_dir)
    E = ElementMaker(
        namespace="http://www.tei-c.org/ns/1.0", nsmap={None: "http://www.tei-c.org/ns/1.0"}
    )

    missingcorpusfiles = set(path.name for path in corpus_path.glob(f"*{ext}"))
    missingmetadatafiles = set()

    folder = pathlib.Path(output_dir)
    if not folder.exists():
        raise FileNotFoundError(
            f"Le dossier '{folder.absolute()}' n'existe pas: vous devez le créer."
        )

    if metadata_file.endswith('.ods'):
        data = get_data(metadata_file)
        data = data["Sheet1"]
    else:
        data = []
        with open(metadata_file) as input_stream:
            reader = csv.reader(input_stream, delimiter='\t', quotechar='"')
            for row in reader:
                data.append(row)

    for i, row in enumerate(data):
        if i == 0:
            continue

        try:
            filename, author, toptitle, title, rate, project, cat, publisher, pub_date, lang = row
            filename = filename.replace("'", "")
            file_ = f"{filename.strip()}{ext}"
        except ValueError as ve:
            print(f"Erreur à la ligne {i+1}: '{ve}'")
            continue

        if lang == "français":
            lang = "fre"  # WARNING: why "fre" and not "fr"?

        try:
            with open(corpus_path / file_, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            missingmetadatafiles.add(file_)
            continue

        missingcorpusfiles.remove(file_)

        teifile = text_to_tei(
            text,
            author,
            publisher,
            toptitle,
            title,
            project,
            responsibility,
            editor,
            edition,
            pub_date,
            lang,
            licence
        )

        f = f'{folder}/{filename}.xml'
        with open(f, 'wb') as fout:
            fout.write(
                etree.tostring(teifile, xml_declaration=True, pretty_print=True, encoding='UTF-8')
            )

    print()
    print(
        f"Les fichiers suivants du corpus '{corpus_path}' n'ont pas de métadonnées '{metadata_file}':"
    )
    for item in sorted(missingcorpusfiles):
        print(f'\t{item}')
    print()
    print(
        f"Les fichiers suivants des métadonnées '{metadata_file}' sont absents du corpus '{corpus_path}':"
    )
    for item in sorted(missingmetadatafiles):
        print(f'\t{item}')


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('corpus_dir', help='donnees-corrigees')
    parser.add_argument('metadata_file', help='The metadata file (.ods / .tsv)')
    parser.add_argument(
        '-e', '--ext', default='.txt', help='Extension des fichiers à chercher (default: ".txt")'
    )
    parser.add_argument(
        '-o', '--output-dir', default='output', help='Le dossier de sortie où écrire les XML.'
    )
    parser.add_argument('-r', '--responsibility', help='Qui est responsable?')
    parser.add_argument('--editor', help='Qui est éditeur?')
    parser.add_argument('--edition', help="Quelle est l'édition?")
    parser.add_argument(
        '--licence', default='by-nc-sa', help='Quelle est la licence? (default: by-nc-sa)'
    )

    args = parser.parse_args()

    run(**vars(args))
