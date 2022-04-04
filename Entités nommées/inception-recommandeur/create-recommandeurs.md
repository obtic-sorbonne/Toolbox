Ce readme vise à décrire comment actualiser les recommandeurs du service
Inception fourni par l'ObTIC sur les serveurs d'HumaNum :
https://obvil.huma-num.fr/inception/

# Recommandeurs Inception: création et mise à jour

## Les recommandeurs SpaCy

Les recommandeurs utilisés sur le site d'inception utilisent comme moteur SpaCy.
Il y a deux possibilités pour ajouter des suggestions via un recommandeur :

1. entraîner un nouveau modèle SpaCy
2. utiliser des patrons de reconnaissance

Ces deux méthodes peuvent être combinées. La priorité sera cependant donnée au
moteur SpaCy par rapport aux patrons de reconnaissance en cas de conflit dans
les sorties.

## Entraîner un modèle SpaCy

Documentation SpaCy : https://spacy.io/usage/training

Vous pouvez trouver un tutoriel sur comment entraîner un modèle SpaCy sur le
dépôt Github suivant : github.com/YoannDupont/train_spacy en suivant les étapes :

1. https://github.com/YoannDupont/train_spacy/tree/main/01-prepare_data
2. https://github.com/YoannDupont/train_spacy/tree/main/02-train_model

### Déploiement

Une fois votre modèle entraîné, zippez le dossier `model-best` et envoyez-le à
une personne pouvant le mettre en ligne sur le serveur. Il faudra préciser :

- le nom à utiliser pour pouvoir y accéder

## utiliser des patrons de reconnaissance SpaCy

Documentation SpaCy : https://spacy.io/api/entityruler

Vous pouvez également donner des patrons de reconnaissance à utiliser dans SpaCy
pour générer des suggestions. Ces patrons nécessitent deux valeurs :

1. le patron de reconnaissance (par exemple: expression régulière)
2. l'étiquette à associer à ce patron de reconnaissance (par exemple: Personne, Lieu, etc.)

Vous pouvez vous référer à la documentation SpaCy pour créer des patrons plus
spécifique. Les fichiers de reconnaissance sont à fournir au format `.json`.

Pour des exemples, vous pouvez aller à la page : https://github.com/YoannDupont/train_spacy/tree/main/03-gazetteer

### Exemples de patrons

L'ensemble de patrons suivant reconnaît `Paris` en tant que lieu :

```
[
    {"pattern": "Paris", "label": "Lieu"}
]
```

L'ensemble de patrons suivant reconnaît `Paris` en tant que lieu et `Pâris`
en tant que personne :

```
[
    {"pattern": "Paris", "label": "Lieu"},
    {"pattern": "P\u00e2ris", "label": "Personne"}
]
```

Vous noterez que le `â` de `Pâris` a été transformé pour éviter les erreurs
d'encodage. Il est recommandé d'utiliser un outil qui génère automatiquement un
fichier `.json` si vous utilisez des caractères accentués ou non-latins.

### Déploiement

Une fois votre fichier `.json` créé, envoyez-le à une personne pouvant le mettre
en ligne sur le serveur. Il faudra préciser :

- le nom à utiliser pour pouvoir y accéder
- s'il faut utiliser uniquement les patrons ou conserver les sorties SpaCy
