"""
Convertir la sortie de 0-transformer-brat-a-bios.pl en un csv utilisable par le script
de calcul du score inter-annotateurs.
Sous-entend que les fichiers sont dans un dossier avec pour nom le titre du corpus.
Et à l'intérieur, les dossiers extraits de Connll 2002 au format "nomCorpus-auteur-nomAnnotateur"

lvp
├── lvp-zola-camille
│   ├── chapitre1.bios.tsv
│   ├── chapitre2.bios.tsv
└── lvp-zola-marguerite
    ├── chapitre1.bios.tsv
    ├── chapitre2.bios.tsv
"""

import sys
import os, glob
import re
import csv
import argparse

# Initialize the parser
parser = argparse.ArgumentParser(
    description="Convertir la sortie de Brat en un csv utilisable par le script '2-calcul-accord-interannotateur-de-csv.py'"
)

# Add the positional parameters
parser.add_argument('input', help="The input folder")
parser.add_argument('output', help="The output file")
arguments = parser.parse_args()

#corpus = "lvp"
#outfile = os.path.join("output", corpus) + '.csv'
outfile = arguments.output
corpus = arguments.input
map_tag = {
    'PER': 0,
    'LOC': 1,
    'MISC': 2,
    'O': 4
}

annotations = []
csv_header = ['token']
for corpus_annotateur in os.listdir(corpus):

    path_corpus = os.path.join(corpus, corpus_annotateur)

    if not (os.path.isdir(path_corpus)):
        continue

    annotateur = corpus_annotateur.split('-')[-1] 
    csv_header.append(annotateur)

    annotation = []
    for conllfile in glob.iglob(f"{path_corpus}/*.bios.tsv"):

        with open(conllfile, 'r', encoding="utf-8") as fin:
            for line in fin:
                line = line.strip()
                if not line:
                    continue

                annotation.append(line.split('\t'))
    annotations.append(annotation)
  

# On itère sur la première sous-liste pour récupérer l'index d'un token
# ensuite pour chaque annotation (=chaque sous-liste)
# on extrait le token correspondant
output = []
for i in range(0, len(annotations[1])):
    
    line = []
    for y in range(0, len(annotations)):
        if y == 0:
            # on ajoute le token une seule fois
            line.append(annotations[y][i][0])

        # ajout du tag
        tag = re.sub('[BIES]-', '', annotations[y][i][1])
        line.append(map_tag[tag])
    output.append(line)

with open(outfile, 'w', encoding="utf-8") as fout:
     csv_writer = csv.writer(fout, delimiter=';')
     csv_writer.writerow(csv_header)
     csv_writer.writerows(output)
