# Word Embeddings
Les modèles 'embeddings' de mots transforment les tokens d'un texte en vecteurs, dont les valeurs sont déterminées par le contexte dans lequel chaque token se trouve. Les vectorisations nous renseignent donc sur la manière dont les mots sont utilisés dans le corpus sur lequel le modèle est entraîné. Dans ce cas, le fichier french-18C a été entraîné sur une combinaison du corpus complet 'frantext' et de l'Encyclopédie (Environ 57 millions de tokens).

📌  **Utilisation rapide** : `python3 obtenir_synonymes.py frantext syns_50_wordcount.txt word2vec`
<br/>Entraîner un modèle (soit fasttext, soit word2vec) sur un dossier donné de documents. Les options sont décrites dans le script. Nécessite un grand nombre de textes pour entraîner le modèle (voir ci-dessus).