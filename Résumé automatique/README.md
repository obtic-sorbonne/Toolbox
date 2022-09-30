# Génération automatique de résumé

Ce script permet de générer une fiche au format HTML résumant le contenu d'un article scientifique en anglais au format XML.

## Format d'entrée du fichier XML

Le format des articles scientifiques en entrée est celui de la revue *[Comunicar](https://www.revistacomunicar.com/)*. Les différentes sections de l'article doivent se trouver dans des balises <sec>, les titres des sections dans <title> et le contenu textuel dans des balises <p>. Les figures doivent être signalées par des balises <fig>.



## Format de sortie

Le fichier de sortie contient les informations suivantes :

- Nombre de mot

- Temps de lecture estimé (nb_de_mots / 200 * 60 + 10 * nb_figures)

- Résumé de l'abstract

- Résumé de l'introduction

- Titre de chaque section, avec les mots-clés associés à celle-ci

- Résumé de la conclusion

Les résumés automatique et la détection des mots-clés sont basés sur des modèles BERT.


## Exécution du script

`python extract_from_xml.py fichier.xml`
