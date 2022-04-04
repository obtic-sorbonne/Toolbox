# utiliser un recommandeur NER

En supposant qu'on travaille sur un projet appelé MonProjet.

- aller dans `MonProjet`.
- aller dans `settings`
- onglet `Recommanders`

Pour configurer un recommandeur :

- bouton `create`
- Layer `Named entity`
- Feature `value`
- Tool `Remote classifier`
- Remote URL :
    - `http://<adresse-ip>:<port>/` + nom du recommandeur
    - demander les `<adresse-ip>` et `<port>` auprès d'un membre d'ObTIC

# Les recommandeurs installés

- spacy_ner_fr
    - recommandeur spacy de base `fr_core_news_sm`
- spacy_ner_fr_mapper
    - recommandeur spacy de base `fr_core_news_sm`
    - ne conserve que les lieux
    - donne une sous-catégorie aux lieux selon des lexiques
- spacy_coarse
    - recommandeur spacy appris sur tout le corpus gold : https://github.com/OBVIL/Entites-nommees
    - donne toutes les catégories (pour le moment)
    - donne uniquement les catégories "gros grain" (PER, LOC, MISC)
- spacy_fine
    - recommandeur spacy appris sur LVP + Nana : https://github.com/OBVIL/Entites-nommees
    - donne toutes les catégories (pour le moment)
    - donne les catégories "grain fin" (PER, LOC.ConstructionHumaine, LOC.Admin, MISC, etc...) mais pas l'attribut "évoqué"
- spacy_fine_noevoq
    - recommandeur spacy appris sur LVP + Nana : https://github.com/OBVIL/Entites-nommees
    - donne toutes les catégories (pour le moment)
    - donne les catégories "grain fin" (PER, LOC.ConstructionHumaine, LOC.Admin, MISC, etc...) + l'attribut "évoqué" (on peut avoir LOC.Admin.Évoqué)
