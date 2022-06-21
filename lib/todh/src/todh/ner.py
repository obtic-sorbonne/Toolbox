"""Description:
    Le module pour gérer le chargement des modèles de NER ainsi que l'itération
    sur la sortie du modèle.

Exemples d'utilisation:
    SpaCy:
    >>> pipeline, label_function, iterator = load("spacy", "fr_core_news_md")
    >>> for entity in iterator(label_function("Jean Dupont vit à Paris.")):
    ...     print(entity)
    ('PER', 0, 11)
    ('LOC', 18, 23)

    flair:
    >>> pipeline, label_function, iterator = load("flair", "flair/ner-french")
    >>> for entity in iterator(label_function("Jean Dupont vit à Paris.")):
    ...     print(entity)
    ('PER', 0, 11)
    ('LOC', 18, 23)
"""

import functools

import spacy

from flair.data import Sentence as FlairSentence
from flair.models import SequenceTagger


def load(engine, model_name):
    loader = loaders.get(engine)
    iterator = entity_iterators.get(engine)

    if loader is None:
        raise ValueError(f"Pas de chargeur de modèle pour {engine}")

    if iterator is None:
        raise ValueError(f"Pas d'itérateur d'entités pour {engine}")

    pipeline = loader(model_name)
    label_function = get_label_function(engine, pipeline)

    return pipeline, label_function, iterator


def flair_annotate(sentence, modele):
    s = FlairSentence(sentence)
    modele.predict(s)
    return s


def get_label_function(annotateur_name, annotateur):
    if annotateur_name == "flair":
        return functools.partial(flair_annotate, modele=annotateur)

    if annotateur_name == "spacy":
        return annotateur.__call__

    raise KeyError(f"{annotateur_name} n'a pas de fonction d'annotation connue")


def spacy_iterate(doc):
    for entity in doc.ents:
        yield (entity.label_, entity.start_char, entity.end_char)


def flair_iterate(doc):
    for entity in doc.get_spans('ner'):
        yield (entity.tag, entity.start_pos, entity.end_pos)


loaders = {
    "spacy": spacy.load,
    "flair": SequenceTagger.load,
}

entity_iterators = {
    "spacy": spacy_iterate,
    "flair": flair_iterate,
}
