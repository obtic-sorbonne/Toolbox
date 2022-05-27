# Correction des sorties OCR
## [`jamspell`](https://github.com/bakwc/JamSpell/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obtic-scai/Toolbox/blob/dev/Correction/jamspell/jamspell_xml_txt.ipynb)

https://github.com/obtic-scai/Toolbox/blob/dev/Correction/jamspell/jamspell_xml_txt.ipynb

<!-- Le texte brut issu de l'océrisation peut être corrigé avec la librairie de correction contextuelle libre et *open source* ([`jamspell`](https://github.com/bakwc/JamSpell/)). -->

Librairie initialement écrite en **C++**, mais fonctionnelle également en **Python**.

<ins>Prérequis</ins> : installer les *bindings* `swig`
* compilateur d'interface qui connecte des programmes écrits en C++ avec d'autres langages (en l'occurrence, avec Python).

Instructions d'installation en local -> [GitHub](https://github.com/bakwc/JamSpell/#usage).
* Pour contourner les problèmes d'installation potentiels du `swig` et, par conséquent, de `jamspell`, envisagez à utiliser [Google Colab](https://colab.research.google.com/github/obtic-scai/Toolbox/blob/dev/Correction/jamspell/jamspell.ipynb#scrollTo=Hoqpo17hlWIk).

La correction des textes en français s'effectue grâce au modèle de langage correspondant, parmi les autres modèles téléchargeables [ici](https://github.com/bakwc/JamSpell/#download-models).

Pour entraîner votre propre modèle -> [instructions d'utilisation](https://github.com/bakwc/JamSpell/#train).
