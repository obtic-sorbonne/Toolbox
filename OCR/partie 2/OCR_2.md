---
marp: true
theme: default
markdown.marp.enableHtml: true
paginate: true
---

<style>

section {
  background-color: white;
  color: black;
}


h1 {
  color: DarkBlue;
}

h2 {
  color: DarkBlue;
}

h3 {
  color: DarkBlue;
}

h4 {
  color: DarkBlue;
}

h5 {
  color: DarkBlue;
}

h6 {
  color: DarkBlue;
  font-size: 30px;
  font-weight:normal;
}


img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
blockquote {
  background: #ffedcc;
  border-left: 10px solid #d1bf9d;
  margin: 1.5em 10px;
  padding: 0.5em 10px;
}
blockquote:before{
  content: unset;
}


blockquote:after{
  content: unset;
}
</style>


<!-- _class: lead -->



![width:200](img/su.png) &nbsp;&nbsp;&nbsp; $\qquad$ $\qquad$ ![width:350](img/obtic.png) $\qquad$ $\qquad$ ![width:200](img/scai.png)
<br> 

## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Transkribus, Kraken, eScriptorium, Tesseract

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Johanna Cordova, Ljudmila Petkovic**<br><br>

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Paris, le 18 novembre 2021




---

## Corpus

_Registre du Comité d'administration du Théâtre français de S. M. l'Empereur et Roi._

* Rédigé par Nicolas Bernard, commissaire du théâtre
* Paris, le 16 janvier 1813
* Texte manuscrit

* **Document** : collection d'images formant un ensemble
* Échantillon de 10 pages ([dépôt GitHub](https://github.com/ljpetkovic/Registre_R416))

---


## I&nbsp;&nbsp;&nbsp; Transkribus

### 1. Pré-traitement des données 

---

## Pré-traitement des données


* **Sélectionner les pages à pré-traiter** (de bonne qualité)
  * Exclure les pages vides, non pertinentes, le dos de livre etc.

* **Découper les scans PDF**
  * afin de ne transcrire que le véritable contenu textuel d'une page
  * sinon, le moteur d'OCR / HTR va générer des symboles inutiles
  * Impact de la couverture du document, des traces de l'écriture de la page précédante / suivante, des taches etc. sur la qualité de transcription


---

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![width:350](img/découpage.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![width:290](img/découpé.png)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Figure 1a : PDF original.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Figure 1b : PDF découpé.  

---

## Pré-traitement des données

* Charger toutes les pages, pour garder les références (page de titre) 
* Normalisation du contrast **sans** binarisation lors du chargement des images du document ([Michael _et al_, 2018](https://readcoop.eu/wp-content/uploads/2018/12/D7.9_HTR_NN_final.pdf)) 
  * ≠ Kraken — binarisation comme une étape indépendante et facultative

---

## I&nbsp;&nbsp;&nbsp; Transkribus

### 2. Choix du modèle de transcription
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.1 New France 17th-18th Centuries

---


## Choix du modèle de transcription

Plusieurs paramètres :
* Langue : française
* Alphabet : latin
* Type d'écriture : [_coulée_](https://books.google.fr/books?id=lcHRgDFtBSYC&pg=PA110&lpg=PA110&dq=ronde”,+“bâtarde”+and+“coulée&source=bl&ots=HjaRrULe19&sig=ACfU3U1qwQZuF15hXKxv1DXqcAzFIJueMg&hl=en&sa=X&ved=2ahUKEwi4oZmeoIf0AhWqyIUKHYQPA5kQ6AF6BAgCEAM#v=onepage&q=ronde”%2C%20“bâtarde”%20and%20“coulée&f=false) ![width:190](img/coulee.png) [_ronde_](https://books.google.fr/books?id=lcHRgDFtBSYC&pg=PA110&lpg=PA110&dq=ronde”,+“bâtarde”+and+“coulée&source=bl&ots=HjaRrULe19&sig=ACfU3U1qwQZuF15hXKxv1DXqcAzFIJueMg&hl=en&sa=X&ved=2ahUKEwi4oZmeoIf0AhWqyIUKHYQPA5kQ6AF6BAgCEAM#v=onepage&q=%22ronde”&f=false) ![width:180](img/ronde.png) [_bâtarde_](http://classes.bnf.fr/ecritures/grand/e142.htm) ![width:200](img/batarde.png)
* Type de documents : administratif, ~ordonnances, chancellerie
* Époque : début du XIX$^e$ s.
* Moteur de reconnaissance de caractères : HTR ou HTR+ (plus performant, _cf._ [ici](https://readcoop.eu/wp-content/uploads/2018/11/LEIFERT-CITLAB.pdf))
* CER (taux d'erreur de caractère, angl. _character error rate_)

---

## Choix du modèle de transcription

Modèles d'HTR+ accessibles au public (_cf._ le site de Transkribus) : 
* [French — General Model](https://readcoop.eu/model/french-general-model/) (8.5% CER)
* [Charter Scripts (German, Latin, French)](https://readcoop.eu/model/charter-scripts-german-latin-french/) (6.32% CER)
* [French and Latin Chancery documents](https://readcoop.eu/model/french-and-latin-chancery-documents/) (5.33% CER)
* [French Handwriting 19$^{th}$ century](https://readcoop.eu/model/french-handwriting-19th-century/) (7.73% CER) 
* [French Livre Rouge](https://readcoop.eu/model/french-livre-rouge/) (8% CER)
* [New France 17$^{th}$-18$^{th}$ centuries](https://readcoop.eu/model/new-france-17th-18th-centuries/) (4.12% CER) 
* [Ordonnances des Intendants](https://readcoop.eu/model/ordonnances-des-intendants/) (4.18% CER)

---

## New France 17$^{th}$-18$^{th}$ centuries
|         |            | 
|:-------------:|-----| 
| ![width:700](img/new_france.png) Source : [Projet « Nouvelle-France numérique »](http://nouvellefrancenumerique.info)    | • Combinaison d'écritures françaises (_ronde_, _bâtarde_ et _coulée_) <br> • 1 600 pages (296 403 mots) de correspondance et de registres des administrateurs coloniaux de la Nouvelle-France du XVII$^e$/XVIII$^e$  s.<br> • CER de 4.12% (données de validation)<br> • Pas adapté aux écrits des notaires ou des greffiers |

---

## I&nbsp;&nbsp;&nbsp; Transkribus

### 3. Préliminaires 
### 4. Lancement de l'HTR 

---

## Préliminaires

* S'inscrire / se connecter à [Transkribus](https://readcoop.eu/transkribus/) avec votre compte
* Ajouter les propriétaires de la collection `Registre_R416` via email
---

## Lancement de l'HTR
* Sélectionner les pages découpées au préalable pour l'HTR

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![width:300](img/overview.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![width:380](img/overview_modèle.png)

---

## Lancement de l'HTR

![width:750 center](img/modèle.png)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Le modèle « New France » dans Transkribus.

---

## Lancement de l'HTR

* La simplification des polygones réduit la complexité des segments de ligne, en économisant de la bande passante et de l'espace de stockage

![width:350 center](img/polygon_simpli.png)


---


## I&nbsp;&nbsp;&nbsp; Transkribus

### 4. Résultats de l'HTR 

---

## Résultats de l'HTR

* Durée de transcription : environ 3h pour 480 pages

![width:600 center](img/transcription.png)


---


## II&nbsp;&nbsp;&nbsp; Kraken

### 1. Choix du modèle de transcription

---
## Choix du modèle de transcription

* Modèles d'HTR accessibles au public (les [nouveaux](https://gitlab.inria.fr/dh-projects/kraken-models) et les [anciens](https://gitlab.inria.fr/dh-projects/kraken-models/-/tree/master/segmentation%20models/archived), ALMAnaCH Inria)
* Les résultats de transcription ne sont pas tout à fait satisfaisants 
* Modèles entraînés sur quels textes ?
* Les modèles obsolètes manifestent un problème d'initialisation du package `nnpack`

---
## Binarisation
* Conversion d'une image en noir et blanc (image _binaire_)
* Distinguer le texte (ou tout autre élément d'image requis) de l'arrière-plan
* Comment « supprimer » la couleur de l'arrière-plan (sombre) sans perdre également les informations du texte ? (même avec de l'ajustement de la luminosité)
* Impossible de filtrer l'arrière-plan sans effacer ou éclaircir simultanément le texte
* L'arrière-plan introduit un « bruit » qui gêne la reconnaissance 
![width:600 center](img/bin_grey.png)

---
## Binarisation kraken

* Algorithme [`nlbin`](https://python.hotexamples.com/examples/kraken.binarization/-/nlbin/python-nlbin-function-examples.html) (non requis avec le segmenteur de ligne de base `-bl`)
![width:550](img/non_binarisation.jpg)![width:490](img/binarisation.png)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Figure 2a : Image non binarisée&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Figure 2b : Image binarisée

---
## `riant_ftmrs15_12.mlmodel` (avec binarisation)
* Ancien modèle
* Génère meilleurs résultats par rapport aux nouveaux modèles de kraken
```
Régistre du Comité d'Administration
d'ou Tonéatre Français de S. M. Emvereur et Roi
2
Paris ce 16 Jauvier 1d
d'après l'inviration deMr Benard suupténant, les foutetions de Commipsaire
Anpérias M. M. FSeury Tahue Nicnos damors demuer &amp; Lacave de nomciprent
a heures dans laSaile des Séances du Contite d adninntration 
d Bernard notitie du arrete deMr Le surentendans desoictaite
oortans l'arganisation d'un du Comite d'Aduntration à d'autie d
conité de Lechere confomeuient au denret inpérias d 
[...]
Art. 3e         # segmentation correcte
le Commiaire unvérial ent charge del'exécution dupréfenr arrêté
PParis ce 13 Janv° 1813. Sigui le Cle de Reimurat 
Argandatton  de Bremier Chambellau deS. M. l'Erupereur &amp; Roi, sureutendant des
dis Cortute de svectaies, du l'Article 68 du Decret nuvérial du 15, 0bre portant orgouisation
du Theitre François, Arrété dt due Suis.
2rt. de         # bonne segmentation
asous nommés meuibres du Comité de Vecture pourlespières crouvelles, M. M
```



---

## `riant_ftmrs15_12.mlmodel` (sans binarisation)
* le début du texte est déplacé (`[...] Registre du Comite d'Administration [...]`)

```
inpérial, M. M. Feury, Tahuu, Michos dumas, desier &amp;Lacave se recrifent
Le Prerrier Chambellau deS. M. l'Empereur et Roi surinteudant des
d'Adhninistration. portaur orgouisation du Théatre Francais, Arrête cequi suit.
Flesdes Raucourt &amp; Mars sout adjouites au Comité pour laPocuation
dis Coutité de spectartes, du l'Article 68 du Décret inpérial du15, 8bre portant orgouisation
Registre du Comite d'Administration
du Cnéatre français deS. M. l'Empereur et Roi,
Organisation
Paris ce 16 Janvier 1813.~
d'après l'invitation duNr Bernard recptinant lesfouctions de Commisaire
à 2 heures dans laSalle desséances du Conrité 
[...]       
Art. 3.           # segmentation incorrecte
Art. 2°.          # segmentation incorrecte
Art. 1er          ...
Art. 2e
Art. 3e
Art. 1er
Verture.
20
sous nommés meubres duComité deLecture pourlespières nouvelles, M. M
```
---

## III&nbsp;&nbsp;&nbsp; eScriptorium

### 1. Introduction

---

## Introduction

* Infrastructure web gratuite et à code source ouvert 
* Spécialisée pour l'HTR des documents anciens
* Développée par PSL | INRIA
* Basée sur les techniques de l'apprentissage machine ([encog](https://en.wikipedia.org/wiki/Encog))
* Cadre de programmation fourni par l'application eScript
* Connexion au [serveur](https://escriptorium.fr) ou installation en local / Docker
* _Cf._ le [tutoriel](https://lectaurep.hypotheses.org/documentation/prendre-en-main-escriptorium) en français
---



## III&nbsp;&nbsp;&nbsp; eScriptorium

### 2. Préliminaires

---

## Préliminaires

**Connexion au serveur** 

* [Instance eScriptorium](https://escriptorium.fr/login/) en ligne
* Nom d'utilisateur : `guest`
* Mot de passe : `GuestAccount2021!` 
* Tableau de bord pour la gestion des documents créés par et partagés avec un compte


---

## Préliminaires

* Création d'un nouveau document
* Chargement des images
>La binarisation n'est plus une étape obligatoire et pourrait même diminuer la qualité [des images à transcrire]
* Segmentation automatique : `blla.mlmodel` par défaut



---

## Segmentation

* `blla.mlmodel` (par défaut)

![width:700 center](img/seg.png)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Les lignes (violet) et les zones (vert).

---

## Transcription (sans binarisation)

```
Registre du Comite d'Administration
du Tnéatre Français deS. M. l'Empereur et Roi,
Paris ce 16 Janvier 1813.~
d'après l'invitation deNr Bernard recptinant lesfouctions de Commisaire
innpérial, M. M. Fleury, Tahuu, Michot dumas, desprer &amp;Lacaue se recrifsent
à 2heures dans laSalle desséances du Contité d'Administration-
Me Deruardnotifie deux arrétés &amp; r leSurintendant desspectaites
portaut l'organisation, l'un du Comité d'Adiniuntration &amp;l'autre du
Comrité de Lecture, confornsément au décret inpérial du15 8bre 1 812-
Ces arrêtés sour ainsiconcur.
Organisation
Le Preurier Chambellau deS. M. l'Eupereur et Roi Surinteudant des
du Comite
Svertactes, du les articles 30 a 49 du décres iipérial du15 8bre 1812
20
d'Aohinistration. poitaut orgouisation du Théatre Francais, Arrete cequi suit.
Art. 1er
Sous nommés meubres duComité d'Aduinistration M. M. Feury, Talmre
Michot, Damas, Denrer, Lacane.
Art. 2e
```
---

## IV&nbsp;&nbsp;&nbsp; Évaluation
1. Mesures d'évaluation
2. Outil d'évaluation
3. Comparaison des modèles HTR

---
## Mesures

Paramètres de qualité : **reconnaissance des caractères**, reconnaissance de la mise en page

2 mesures principales pour évaluer la reconnaissance de caractères :

- *Character error rate* (CER) : pourcentage de caractères erronés dans le document
- *Word error rate* (WER) : pourcentage de mots qui contiennent des erreurs

Types d'erreurs : substitution, insertion, délétion

---

## Résultats
| Exemple                                                      | Texte du manuscrit                                           | Sortie d'OCR                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![](img/exemple.jpg) | Arrêté de M. le<br />surintendant<br />relatif à Mlles<br />Mars et Leverd,<br />qui fixe leurs<br />droits respectifs. | Arrêté de M. le<br/>surintendant<br/>relatif à M**o** **le**<br/>Mars et Leverd<br/>qui fixe leurs<br/>droits respe**r**tifs. |

------

## Outil d'évaluation

Étapes pour l'évaluation : 

- Corriger manuellement une partie des sorties OCR (*ground truth*)

Outil d'édition de *ground truth* : Aletheia (https://www.primaresearch.org/tools/Aletheia/Editions)

- Comparer les pages corrigées et leur version océrisée

Outil de comparaison : **ocrevalUAtion** (https://github.com/impactcentre/ocrevalUAtion)

------

## Comparaison des modèles (segmentation)

|                 | Transkribus                        | Kraken                           | eScriptorium                     |
| --------------- | ---------------------------------- | -------------------------------- | -------------------------------- |
| Détection marge | ✔ | ✗ | ✗ |

------

## Comparaison des modèles (reconnaissance de caractères)

|                  | Transkribus | Kraken (avec binarisation) | Kraken (sans binarisation) | eScriptorium |
| ---------------- | ----------- | -------------------------- | -------------------------- | ------------ |
| CER              | **10,70**   | 41,67                      | 55,8                       | 36,96        |
| WER              | **35,00**   | 80,23                      | 84,86                      | 72,59        |
| WER (sans ordre) | **30,70**   | 63,20                      | 53,9                       | 54,28        |

---
## Comparaison des modèles (reconnaissance de caractères)

![image-20211117162024725](img/graphique_CER_WER.png)


---
## V. Amélioration du modèle

1. Réentraînement du modèle
2. Évaluation du nouveau modèle
3. Utilisation avancée : les formats hOCR et ALTO

------

##  Réentraînement du modèle

Possible sur **Kraken**.

L'outil Kraken détecte d'abord les segments de texte. Il faut alors établir les vérités-terrain (*ground truth*), puis fournir au système les paires images-texte pour qu'il "apprenne" à reconnaître l'écriture du document. Ces nouvelles connaissances sont ajoutées à celles du modèle qu'on réentraîne.

------

##  Évaluation du nouveau modèle

Entraînement sur 4 fichiers (c'est très peu !)

L'évaluation doit se faire sur un fichier qui n'a pas servi à l'entraînement.

Evaluation sur 1 page :

|                  | Modèle initial | Modèle réentraîné |
| ---------------- | -------------- | ----------------- |
| CER              | 55,9           | 56,4              |
| WER              | 91             | 91,4              |
| WER (sans ordre) | 68             | **57**            |

------

## VI. Pour finir

* dépôt [GitHub](https://github.com/ljpetkovic/Registre_R416)

