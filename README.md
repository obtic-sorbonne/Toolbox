# Toolbox

L'équipe [ObTIC-Sorbonne](https://obtic.sorbonne-universite.fr/) met à disposition une suite d'outils, de scripts et de ressources utiles pour la manipulation et le traitement de données textuelles.

<img src="https://obtic.sorbonne-universite.fr/wp-content/uploads/2022/03/data.png" width="300" height="300">

## Description des outils

Sauf indication contraire, tous les scripts s'exécutent avec Python 3.7 ou au-dessus.

### Collecte de corpus (Scrapping)
La plateforme [Wikisource](https://fr.wikisource.org/wiki/Wikisource:Accueil) contient de très nombreux textes littéraires libres de droits. Le script `scrape_wikisource.py` permet d'extraire automatiquement un ou plusieurs échantillons d'un texte à partir de son URL Wikisource.

Prérequis : Beautiful Soup 4 doit être installé 
`pip install bs4`

📌  **Utilisation rapide** : `python scrape_wikisource.py`
<br/>Extrait un échantillon dans un texte sélectionné aléatoirement sur Wikisource.


**Utilisation avancée** : Plusieurs modes d'extraction sont disponibles.

#### Extraction du texte intégral
Méthode d'extraction par défaut.
Il est nécessaire d'ouvrir le script et de remplir la valeur de la variable `book_location` avec l'URL du texte qu'on veut extraire.
En général, les textes complets figurent sur Wikisource sous une URL terminant par /Texte_entier.

#### Extraction d'un échantillon
1. A partir du texte intégral (par défaut)
Il est nécessaire d'ouvrir le script et de remplir la valeur de la variable `book_location` avec l'URL du texte dont on veut extraire un échantillon. Il faut désactiver l'extraction du texte intégral en fixant la variable `texte_complet` à 'non'.

2. A partir d'un sommaire
Pour activer cette option, il est nécessaire de fixer dans le script la variable `chapitres` à la valeur 'oui'.
L'URL à fournir est celle de la page Wikisource listant les chapitres de l'œuvre.
