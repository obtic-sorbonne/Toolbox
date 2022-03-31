# Tesseract

## Installation
Pour installer Tesseract, suivre les [instructions](https://tesseract-ocr.github.io/tessdoc/Compiling.html) du Github de l'outil.

Téléchargez [le(s) modèle(s)](https://github.com/tesseract-ocr/tessdata_fast) que vous souhaitez utiliser et placez-les dans le répertoire où Tesseract s'est installé (sur Linux : `/usr/share/tesseract-ocr/4.00/tessdata `)


## Utilisation
Les fichiers à numériser doivent être en format .png ou .jpg (une résolution autour de 180 donne généralement de bons résultats). Il est possible de convertir facilement un fichier pdf en plusieurs fichiers png avec la commande suivante :

`pdftoppm -r 180 fichier.pdf fichier -png`


Commande Tesseract pour lancer l'OCR sur une seule image (génère un fichier .txt) : 
`tesseract -l [nom_du_modele] nom_fichier.png nom_fichier_sortie`

Lancer Tesseract sur un ensemble de fichiers contenus dans un dossier :
`for f in nom_dossier/*.png ; do tesseract -l [model_name] "$f" "$f" ; done`
