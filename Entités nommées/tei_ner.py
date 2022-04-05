#!/usr/bin/env python3
"""description:
    Annote un fichier TEI avec un moteur de reconnaissance d'entités nommées.
    Ce script utilise la structure du XML pour trouver le contenu textuelle du
    fichier. De base, ce script itère sur les balises <p> à l'intérieur de la
    balise <text>. Le script récupère le contenu textuel de chaque balise et
    annote avec un outil au choix pour ensuite ajouter des balise <Entity> sur
    les mentions trouvées dans le texte.

    L'utilisation de cette balise <Entity> rend utilisable la sortie de ce
    script dans la plateforme Ariane.

    ATTENTION : ce script détuit potentiellement une partie du formattage XML du
    fichier. En effet, lorsque le contenu textuel est récupéré, tout formattage
    potentiellement présent dans le texte sera perdu.

exemples d'utilisation:
    python ./tei_ner.py -h
    python ./tei_ner.py entree.xml.tei sortie.xml.tei
    python ./tei_ner.py entree.xml.tei sortie.xml.tei -a spacy -m fr_core_news_lg -b s
"""

import pathlib
import spacy
from lxml import etree


def spacy_iterate(doc):
    for entity in doc.ents:
        yield (entity.label_, entity.start_char, entity.end_char)


loaders = {
    "spacy": spacy.load,
}

entity_iterators = {
    "spacy": spacy_iterate,
}


def tei_ner(fichier, balise, annotateur, iterateur):
    """Annote un fichier TEI avec un moteur de reconnaissance d'entités nommées.
    Renvoie un objet XML (lxml.etree.ElementTree). Tout formattage du texte
    (ex: italique, gras, etc.) sera perdu au cours du processus.

    Parameters
    ----------
    fichier : str or pathlike
        Le fichier d'entrée
    annotateur : str, default="spacy"
        Le moteur d'annotation à utiliser
    modele : str, default="fr_core_news_md"
        Le modèle que le moteur doit utiliser
    balise : str, default="p"
        La type de balise contenant le texte

    Returns
    -------
    xml : lxml.etree.ElementTree
        L'arbre XML enrichi des annotations en entités nommées fournies par le
        moteur.
    """

    xmlns = "http://www.tei-c.org/ns/1.0"
    tree = etree.parse(fichier)

    textnode = next(tree.iterfind(f".//{{{xmlns}}}text"))
    for node in textnode.iterfind(f".//{{{xmlns}}}{balise}"):
        # get all the text content of node. This will remove any existing XML
        # formatting as we will provide annotations for the text and replace the
        # content of the XML, so beware.
        text = etree.tostring(node, method="text", encoding="utf-8").decode("utf-8").strip()
=
        node.clear()

        prev = 0
        previous_node = None
        for label, start, end in iterateur(annotateur(text)):
            if prev == 0:
                node.text = text[prev: start]
            else:
                previous_node.tail = text[prev: start]
            node.append(etree.Element("Entity"))
            previous_node = node[-1]
            previous_node.attrib["annotation"] = label
            previous_node.text = text[start : end]
            prev = end

        # the only way previous_node is None is when no entities are found
        if previous_node is not None:
            previous_node.tail = text[end:]
        else:
            node.text = text

    return tree


def main(fichier, sortie, balise="p", annotateur="spacy", modele="fr_core_news_md"):
    if pathlib.Path(fichier).samefile(sortie):
        raise ValueError("Les fichiers d'entrée et de sortie sont identiques")

    loader = loaders.get(annotateur)
    iterator = entity_iterators.get(annotateur)

    if loader is None:
        raise ValueError(f"Pas de chargeur de modèle pour {annotateur}")

    if iterator is None:
        raise ValueError(f"Pas d'itérateur d'entités pour {annotateur}")

    tree = tei_ner(fichier, balise, loader(modele), iterator)

    with open(sortie, "w", encoding="utf-8") as output_stream:
        output_stream.write(
            etree.tostring(tree, pretty_print=True, encoding="utf-8").decode("utf-8")
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("fichier", help="Le fichier TEI à annoter")
    parser.add_argument("sortie", help="Le fichier TEI à écrire")
    parser.add_argument(
        "-b",
        "--balise",
        default="p",
        help="Le type de balise à utiliser pour extraire le texte (par défaut: p)"
    )
    parser.add_argument(
        "-a",
        "--annotateur",
        choices=("spacy",),
        default="spacy",
        help="L'anntateur (moteur d'annotation) à utiliser (défaut: spacy)"
    )
    parser.add_argument(
        "-m",
        "--modele",
        default="fr_core_news_md",
        help="Le modèle à utiliser par l'annotateur (défaut : fr_core_news_md)"
    )

    args = parser.parse_args()

    main(**vars(args))
