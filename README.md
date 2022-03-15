# Toolbox

L'équipe ObTIC met à disposition une suite d'outils, de scripts et de ressources utiles pour la manipulation et le traitement de données textuelles.

## Description des outils

Sauf indication contraire, tous les scripts s'exécutent avec Python 3.7 ou au-dessus.

### Collecte de corpus (Scrapping)
La plateforme [Wikisource](https://fr.wikisource.org/wiki/Wikisource:Accueil) contient de très nombreux textes littéraires libres de droits. Le script `scrape_wikisource.py` permet de récupérer automatiquement des échantillons d'un texte à partir de son URL Wikisource.

Prérequis : Beautiful Soup 4 doit être installé 
`pip install bs4`

Usage : Le nom du fichier sortie et la longueur de l'échantillon doivent être modifiés directement dans le script avant son exécution.

