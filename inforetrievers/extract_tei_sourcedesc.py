#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""description:
    Extrait des données au sujet de la source d'un TEI, en particulier ses
    titre, auteur(rice), date et référence. Les métadonnées extraites du TEI
    sont ensuite écrites sous la forme d'un TSV.

exemples d'utilisation:
    python extract_tei_sourcedesc.py -h
    python extract_tei_sourcedesc.py corpus/ metadata.tsv
    python extract_tei_sourcedesc.py corpus/ metadata.tsv --bibl-types firstEdition printSource --text-items author date --attribute-items ref@target
"""

from lxml import etree
from pathlib import Path
import csv


def get_bibl_type(filename, sourceDesc, bibltype, xmlns):
    bibl = sourceDesc.find(f"{{{xmlns}}}bibl[@type='{bibltype}']")
    if bibl is None:
        print(f"{filename}: no {bibltype}")
        bibl = etree.Element("bibl")
    return bibl


def extract_tei_sourcedesc(
    input_directory,
    output_file,
    bibl_types=("firstEdition", "printSource", "digitalSource"),
    text_items=("title", "author", "date"),
    attribute_items=("ref@target",)
):
    liste_metadata = []
    fields = list(text_items)
    attributes = [item.split("@", 1) for item in attribute_items]
    xmlns = "http://www.tei-c.org/ns/1.0"
    for xml in Path(input_directory).glob("*.xml"):
        error = False
        metadata = {"file": xml.name}
        tree = etree.parse(str(xml))
        sourceDesc = tree.find(f".//{{{xmlns}}}sourceDesc")
        bibls = [get_bibl_type(xml, sourceDesc, bibltype, xmlns) for bibltype in bibl_types]
        for field in fields:
            for bibl in bibls:
                element = bibl.find(f"{{{xmlns}}}{field}")
                if element is not None:
                    break
            error = element is None
            if error:
                print(f"{xml}: missing metadata: {field}")
            else:
                metadata[field] = element.text

        for tag, attribkey in attributes:
            for bibl in bibls:
                element = bibl.find(f"{{{xmlns}}}{tag}")
                if element is not None:
                    break
            error = error or element is None
            if error:
                print(f"{xml}: missing metadata: {tag}")
            else:
                metadata[tag] = element.attrib[attribkey]
                if tag == "ref":
                    metadata["refsource"] = bibl.attrib["type"]

        liste_metadata.append(metadata)

    fields.insert(0, "file")
    fields.extend(attrib[0] for attrib in attributes)
    if "ref" in fields:
        fields.append("refsource")
    with open(output_file, "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for line in liste_metadata:
            writer.writerow(line)


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_directory", nargs="?", default="./data", help="The input directory")
    parser.add_argument("output_file", nargs="?", default="metadata.tsv", help="The name of the output file.")
    parser.add_argument(
        "--bibl-types",
        nargs="+",
        default=("firstEdition", "printSource", "digitalSource"),
        help="The bibl types to consider (default: %(default)s)."
    )
    parser.add_argument(
        "--text-items",
        nargs="+",
        default=("title", "author", "date"),
        help="The bibl types to consider (default: %(default)s)."
    )
    parser.add_argument(
        "--attribute-items",
        nargs="+",
        default=("ref@target",),
        help="The bibl types to consider (default: %(default)s)."
    )

    args = parser.parse_args()
    extract_tei_sourcedesc(**vars(args))
    # sys.exit(0)
