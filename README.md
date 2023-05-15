# Toolbox

L'équipe [ObTIC-Sorbonne](https://obtic.sorbonne-universite.fr/) met à disposition une suite d'outils, de scripts et de ressources utiles pour la manipulation et le traitement de données textuelles.

<img src="https://obtic.sorbonne-universite.fr/wp-content/uploads/2022/03/data.png" width="300" height="300">
<<<<<<< HEAD

## Description des outils

Sauf indication contraire, tous les scripts s'exécutent avec Python 3.7 ou au-dessus.

### Collecte de corpus (Scrapping)
La plateforme [Wikisource](https://fr.wikisource.org/wiki/Wikisource:Accueil) contient de très nombreux textes littéraires libres de droits. Le script `scrape_wikisource.py` permet d'extraire automatiquement un ou plusieurs échantillons d'un texte à partir de son URL Wikisource.

Prérequis : Beautiful Soup 4 doit être installé 
`pip install bs4`

📌  **Utilisation rapide** : `python scrape_wikisource.py`
Extrait un échantillon dans un texte sélectionné aléatoirement sur Wikisource.


**Utilisation avancée** : Deux techniques d'extraction sont disponibles : extraction d'une partie d'un texte intégral et extraction de plusieurs sous-parties piochées à travers les chapitres d'un texte.

#### Extraction à partir du texte intégral
Méthode d'extraction par défaut.
Il est nécessaire d'ouvrir le script et de remplir la valeur de la variable `book_location` avec l'URL du texte dont on veut extraire un échantillon.
En général, les textes complets figurent sur Wikisource sous une URL terminant par /Texte_entier.

#### Extraction de sous-parties à partir d'un sommaire
Pour activer cette option, il est nécessaire de fixer dans le script la variable `chapitres` à la valeur 'oui'.
L'URL à fournir est celle de la page Wikisource listant les chapitres de l'œuvre.

### Reconnaissance des entités nommées

#### Entraîner un modèle SpaCy

Voir le dossier `train_spacy` dans le dossier [Entités nommées](https://github.com/obtic-scai/Toolbox/tree/dev/Entit%C3%A9s%20nomm%C3%A9es) pour avoir la procédure détaillée.

#### Configurer un recommandeur sur le service web Inception

Voir le dossier [Entités nommées/inception-recommandeur](https://github.com/obtic-scai/Toolbox/tree/dev/Entit%C3%A9s%20nomm%C3%A9es/inception-recommandeur).
=======
>>>>>>> main
