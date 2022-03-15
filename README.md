# Toolbox

L'équipe ObTIC met à disposition une suite d'outils, de scripts et de ressources utiles pour la manipulation et le traitement de données textuelles.

## Description des outils

Sauf indication contraire, tous les scripts s'exécutent avec Python 3.7 ou au-dessus.

### Collecte de corpus (Scrapping)
La plateforme [Wikisource](https://fr.wikisource.org/wiki/Wikisource:Accueil) contient de très nombreux textes littéraires libres de droits. Le script `scrape_wikisource.py` permet d'extraire automatiquement un ou plusieurs échantillons d'un texte à partir de son URL Wikisource.

Prérequis : Beautiful Soup 4 doit être installé 
`pip install bs4`


Deux techniques d'extraction sont disponibles :
1. Extraction d'une partie d'un texte intégral
2. Extraction de plusieurs sous-parties piochées à travers les chapitres d'un texte

#### Extraction à partir du texte intégral
Méthode d'extraction par défaut.
En général, les textes complets figurent sur Wikisource sous une URL terminant par /Texte_entier.

#### Extraction de sous-parties à partir d'un sommaire
Pour activer cette option, il est nécessaire de fixer dans le script la variable `chapitres` à la valeur 'oui'.
L'URL à fournir est celle de la page Wikisource listant les chapitres de l'œuvre.
