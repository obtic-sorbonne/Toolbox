# Reconnaissance des entités nommées

Dans ce dossier se trouvent différents script et tutoriels dans le but
d'effectuer de la reconnaissance des entités nommées.

# Annoter un fichier XML TEI

Le script `tei_ner.py` permet d'annoter un fichier XML TEI en entités nommées.

Utilisation :

```
python ./tei_ner.py source.xml.tei destination.xml.tei
```

Où `source.xml.tei` est le fichier d'entrée et `destination.xml.tei` le fichier
de sortie. Le fichier de sortie ne peut pas être le fichier d'entrée. Un fichier
existant sera réécrit sans confirmation.

Par défault, le moteur utilisé est SpaCy et le modèle utilisé est
`fr_core_news_md`. Il est possible de changer les moteur et modèles avec les
options `-a` et `-m` respectivement. Par exemple, pour annoter avec SpaCy et le
modèle `fr_core_news_lg`:

```
python ./tei_ner.py entree.xml.tei sortie.xml.tei -a spacy -m fr_core_news_lg
```

Le script parcourra par défaut les balises `<p>` (à l'intérieur de la première
balise `<text>` trouvée). Si on souhaite par exemple parcourir les balises `<s>`
à la place :

```
python ./tei_ner.py entree.xml.tei sortie.xml.tei -b s
```

# Entraîner un modèle SpaCy

Voir le dossier [train_spacy](train_spacy) pour avoir la procédure détaillée.

# Configurer un recommandeur sur le service web Inception

Voir le dossier [inception-recommandeur](inception-recommandeur).
