# Numérisation de documents (OCR)

Ce répertoire rassemble les ressources liées à la transcription manuelle et automatique (OCR) de documents. Tous ces outils ont été testés en interne et utilisés sur des projets de l'équipe.

Le répertoire **AtelierOCR** contient la restitution des ateliers ObTIC autour de l'OCR. Les diapositives contiennent des informations détaillées et illustrées sur le principe de la numérisation et sur les outils d'OCR (Kraken, eScriptorium, Transkribus, Tesseract). Les fichiers ayant servi aux démonstrations sont également fournis.



## Transcription de document

Outils de transcription manuelle et d'annotation de documents scannés :

- [From the page](https://fromthepage.com/) (en ligne, collaboratif)

- [Scribe](http://scribeproject.github.io/) (à télécharger, version beta)
  
  

## Numérisation de manuscrits (HTR)

La numérisation de manuscrits requiert très souvent l'entraînement d'un modèle adapté à l'écriture qu'on cherche à transcrire. Les outils suivants permettent de détecter les zones de textes, transcrire des échantillons, entraîner un modèle et numériser automatiquement des manuscrits.

### Transkribus

Transkribus est la plateforme de référence pour la numérisation de documents manuscrits. Elle permet d'effectuer facilement tous les traitements liés à la numérisation, et propose de très nombreux modèles pré-entraînés.

Note : pour utiliser le moteur de reconnaissance de caractère HTR+ (le plus performant), il est nécessaire d'obtenir des crédits payants.

### eScriptorium

Cette plateforme, basée sur le moteur d'OCR Kraken, est contrairement à Transkribus libre et open source. Les modèles entraînés sur celle-ci sont donc distribuables librement. Il est possible d'importer des données de Transkribus sur eScriptorium.

## Numérisation d'imprimés

### Tesseract

Cet OCR possède des modèles pré-entraînés sur un très grand nombre de langues, sans précisions sur les polices utilisées (à l'exception du modèle **Fraktur**). Il est performant sur des documents relativement modernes.
