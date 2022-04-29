Ces scripts peuvent être utiles pour convertir entre les différents formats de fichiers produits par les logiciels de reconnaissance d'entités nommées, y compris les plateformes de balisage brat (https://brat.nlplab.org/introduction.html) et Inception (https://inception-project.github.io/example-projects/lener-br/), et les systèmes de génération automatique de balises SpaCy (https://spacy.io/api/entityrecognizer/) et stanza (https://stanfordnlp.github.io/stanza/ner.html).

### 0-transformer-brat-a-bios.pl

Convertit les fichiers au format brat (.ann et .txt) en bios (séparés par des tabulations). Traduit les balises brat en codes standard. Corrèle les débuts et fins de phrases avec les espaces dans un fichier txt de référence de brat. S'assure que les balises couvrant plusieurs tokens sont appliquées à tous les tokens pertinents.

Voir les commentaires du script pour la documentation, ou exécuter "perl <code>0-transformer-brat-a-bios.pl --help".</code>

### 1-convertir-conll2002-a-csv.py

Convertir la sortie de Brat en un csv utilisable par le script
de calcul du score inter-annotateurs.
Sous-entend que les fichiers sont dans un dossier avec pour nom le titre du corpus.
Et à l'intérieur, les dossiers extraits de Connll 2002 au format "nomCorpus-auteur-nomAnnotateur"
Convertir la sortie de Brat en un csv utilisable par le script
de calcul du score inter-annotateurs.
Sous-entend que les fichiers sont dans un dossier avec pour nom le titre du corpus.
À lancer: <code> python brat-to-csv-interAnnotateurs.py <dossier_corpus> <fichier_output></code>
Et à l'intérieur, les dossiers extraits de Brat au format "nomCorpus-auteur-nomAnnotateur"
À lancer:
D'abord, convertir les fichiers dans le dossier de chaque annotateur:
<code> perl 0-transformer-brat-a-bios.pl <dossier_corpus> </code>
Exécutez ensuite le script pour comparer les annotateurs :
<code> python 1-convertir-conll2002-a-csv.py <dossier_input> <dossier_output> </code>

```
lvp
├── lvp-zola-camille
│   ├── chapitre1.bios.tsv
│   ├── chapitre2.bios.tsv
└── lvp-zola-marguerite
    ├── chapitre1.bios.tsv
    ├── chapitre2.bios.tsv
```
Par example:
<code>
perl scripts/0-transformer-brat-a-bios.pl corpus-plusieurs-annotateurs/lvp/lvp-zola-c/* --skip-verification
perl scripts/0-transformer-brat-a-bios.pl corpus-plusieurs-annotateurs/lvp/lvp-zola-m/* --skip-verification
python scripts/1-convertir-conll2002-a-csv.py corpus-plusieurs-annotateurs/lvp corpus-plusieurs-annotateurs/output.csv</code>

