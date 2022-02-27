'''
Accepter txt / xml
Modification structure XML
Levenstein?
Ajouter une liste de mots à ignorer: nombres etc.
ar/fr


'''


#il faut aller à: https://cgit.freedesktop.org/libreoffice/dictionaries/tree/
#et télécharger les dico de la langue en question: https://cgit.freedesktop.org/libreoffice/dictionaries/tree/fr_FR
#puis télécharger les deux fichiers fr.aff et fr.dic    puis les déposer dans le dossier:
#C:\Program Files\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell


#la libraire utilise je pense un traitement de distance livenstein.
#voir rapport Nicolas https://docs.google.com/document/d/1xqXQyj21B_7Qe4Bb5BtbgCkkjL7TW_u74rH8KcveEPY/edit#heading=h.frb0dnajfgus
#et https://github.com/Hiebel/Stage-OBVIL-2020

import enchant#la toute premiere fois il faut l'importer depuis cmd: pip install pyenchant
import glob
from lxml import etree#la premiere fois depuis cmd: pip install lxml
import os
from enchant.checker import SpellChecker #la premiere fois depuis cmd: pip install SpellChecker
import csv

# Fonction de lecture de fichier au format XML-TEI qui renvoie le contenu textuel de la balise "text"
def lire_TEI_XML(input_file):
	namespace = "{http://www.tei-c.org/ns/1.0}text"
	parser = etree.XMLParser(recover=True)
	root = etree.parse(input_file, parser)
	contenu = ""
	for texte in root.iter(namespace):
		textes = texte.itertext()
		for cpt, el in enumerate(textes):
			if el != "\n":
				contenu += el
				contenu += " "
		contenu = contenu.replace("\n", " ")
	return contenu


# Chemin vers le dossier contenant les fichiers texte ou XML-TEI à corriger
dossier_corpus = "Input/"

# Chemin vers le dossier pour enregister les sorties
dossier_sortie = "Output/"

print(enchant.dict_exists("fr"))#ar

# Création du dossier de sortie s'il n'existe pas
if not os.path.exists(dossier_sortie):
	os.makedirs(dossier_sortie)

# Instance du vérificateur orthographique (la langue est entre parenthèses)
chkr = SpellChecker("fr")#ar

# Chargement de la liste d'erreurs personnalisée: False veut dire qu'elle n'est pas prise en compte! True le contraire.
charger_liste = True

if charger_liste:

        # Chemhin du fichier csv sous la forme erreur,correction (optionnelle)
        chemin_liste = "Liste_correction/liste.csv"

        # Le fichier csv de la liste de correction contient-il des entetes ? La variable est à True si oui, False sinon
        presence_entetes = True

        # Si le fichier contient des entêtes (presence_entetes = True), il faut les définir ici
        # La première valeur de la liste sera le nom de la colonne des formes erronées, et la deuxième celle des formes correctes
		#liste_entetes = ["Erreur observée", "Correction proposée"]
        liste_entetes = ["forme_erronée", "forme_correcte"]
        delimiteur = ","
        #delimiteur = "\t"

        with open(chemin_liste, "r", encoding="utf-8", newline='') as csvfile:
            if presence_entetes == False:
                reader = csv.reader(csvfile, delimiter=delimiteur)
                for row in reader:
                    print(row)
                    chkr.replace_always(row[0], row[1])
            else:
                reader = csv.DictReader(csvfile, delimiter=delimiteur)
                for row in reader:
                    chkr.replace_always(row[liste_entetes[0]], row[liste_entetes[1]])

# Chemin du fichier csv qui contiendra la liste des erreurs détectées par le script avec la correction proposée et le fichier d'origine
fichier_erreurs = "%s/erreurs.csv" % dossier_sortie

with open(fichier_erreurs, "w", encoding="utf-8", newline='') as csvfile:
	fieldnames = ["Erreur_détectée", "Correction_proposée", "Contexte", "Fichier"]
	spamwriter = csv.writer(csvfile, delimiter="\t")
	spamwriter.writerow(fieldnames)
	
	for fichier in glob.glob("%s/*" % dossier_corpus):
		extension = fichier.split(".")[-1]
		if extension == "txt" or extension == "xml":
			print("Traitement du fichier %s" % fichier)
			nom_fichier = fichier.split("/")[1]
			sans_extension = nom_fichier.split(".")[-2]
			if extension == "xml":
				contenu = lire_TEI_XML(fichier)
			else:
				with open(fichier, 'r', encoding = "utf-8") as fin:
					contenu = fin.read()
			chkr.set_text(contenu)
			for err in chkr:
				ligne = []
				ligne.append(err.word)
				if len(chkr.suggest(err.word)) > 0:
					err.replace(chkr.suggest(err.word)[0])
					ligne.append(chkr.suggest(err.word)[0])
				else:
					ligne.append("Pas de correction trouvée")
				contexte = err.leading_context(50) + err.word + err.trailing_context(50)
				contexte = contexte.replace("\n", " ")
				ligne.append(contexte)
				ligne.append(nom_fichier)
				spamwriter.writerow(ligne)
			correction_contenu = chkr.get_text()
			with open("%s/%s_correction.txt" % (dossier_sortie, sans_extension), 'w', encoding="utf-8") as fout:
				fout.write(correction_contenu)
