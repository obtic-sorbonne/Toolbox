##################################################################
#L'idée de ce script est de pouvoir télécharger à partir du site Wikisource des textes ou des extraits de textes 
#pour les annoter dans un deuxième temps dans d'autres applications comme Brat ou Inception.
#Les paramètres doivent être personnalisables dans le script à l'aide de variables: url, longueur souhaitée, etc.
#Proposé par Motasem Alrahabi, créé par James Gawley, maintenance et développement par Johanna Cordova (ObTIC).

"""Ce script téléchargera un texte à partir de wikisource et échantillonnera
le texte pour le tester. Si le texte est divisé en plusieurs chapitres, chaque
chapitre sera échantillonné de manière égale afin que le nombre total de
caractères soit inférieur à la limite spécifiée par char_limit ci-dessous.
Si le texte est constitué d'une seule section ou page Web, trois échantillons sont
prélevés au début, au milieu et à la fin du texte. Tous les échantillons seront tronqués
à la fin de la dernière phrase qui se situe dans la limite spécifiée par char_limit."""

# Ce script nécessite que la package 'bs4' soit installé (essayez "pip install bs4" sur la ligne de commande).

# Version 1.1

##################################################################
# PARAMETRE OBLIGATOIRE
# ----------------------------------------------------------------
# Copiez et collez l'adresse du livre sur wikisource
book_location = ""

# PARAMETRES OPTIONNELS
# ----------------------------------------------------------------
# Spécifiez un nom de fichier pour la sortie
filename = ""

# Activer l'échantillonnage par chapitres ou parties [oui/non]
chapitres = "non"

# Personnalisez la longueur de l'échantillon / en caracteres
char_limit =  60000


##################################################################
"""Fin des paramètres."""
##################################################################

from bs4 import BeautifulSoup
import urllib
from urllib import parse, request
from urllib.parse import urlparse
import io
import re
import sys
import random


def chapters(book_location):
    # find the location of all chapters in a table-of-contents page
    book = book_location.replace("https://fr.wikisource.org/wiki/", "")
    # Escape URL if not already escaped
    if not '%' in book:
        book = urllib.parse.quote(book)
    book_location = "".join(["https://fr.wikisource.org/wiki/", book])
    try:
        index_page = request.urlopen(book_location)
    except urllib.error.HTTPError:
        sys.exit(" ".join(["The page", book_location, "cannot be opened. Is there a problem with accent marks?"]))

    index_soup = BeautifulSoup(index_page, 'html.parser')
    # get the list of all the links listed on the page and get them ready to scrape.
    nodes = index_soup.findAll("ul")
    try:
        for ul in nodes:
            if ul.parent.attrs['class'][0] == 'ws-summary':
                for li in ul.children:
                    for a in li.children:
                        if 'title' in a.attrs and 'href' in a.attrs:
                            sections.append(a.attrs['href'])
    except (KeyError, AttributeError):
        pass
    if len(sections) == 0:
        # grab the div whose class is ws-summary
        sum = index_soup.find("div", {"class": "mw-parser-output"})
        #grab the anchor tags inside it
        for a in sum.findAll("a"):
            try:
                if "Page:" in a.attrs['href']: # don't include general page tags
                    continue
                sections.append(a.attrs['href'])
            except (NameError, KeyError):
                continue
    return sections


random_texts = [
"Nana/Texte_entier",
"Au_bonheur_des_dames/Texte_entier",
"L%E2%80%99Argent_(Zola)/Texte_entier",
"%C3%80_vau-l%E2%80%99eau",
"Marthe,_histoire_d%E2%80%99une_fille/Texte_entier",
"Les_S%C5%93urs_Vatard/Texte_entier",
"En_m%C3%A9nage",
"Les_Diaboliques/La_vengeance_d%E2%80%99une_femme",
"Germinie_Lacerteux/Texte_entier",
"Le_Journal_d%E2%80%99une_femme_de_chambre/Texte_entier",
"Le_Calvaire/Texte_entier",
"Le_Colonel_Chabert",
"La_Cousine_Bette_(ed._Houssiaux)",
"Une_t%C3%A9n%C3%A9breuse_affaire",
"Louis_Lambert",
"Le_Chef-d%E2%80%99%C5%93uvre_inconnu",
"Physiologie_du_Mariage",
"L%E2%80%99%C3%89ducation_sentimentale,_%C3%A9d._Conard,_1910/Texte_entier",
"L%E2%80%99Insurg%C3%A9_(Vall%C3%A8s)/Texte_entier",
"L%E2%80%99Enfant_(Vall%C3%A8s)/Texte_entier",
]


if __name__ == '__main__':
    sections = []

    # Generate sample from random list
    if not book_location:
        text = random.choice(random_texts)
        book_location = "https://fr.wikisource.org/wiki/" + text

    # Auto extraction of filename if not define
    if not filename:
        path_elems = urlparse(book_location).path.split('/')
        if path_elems[-1] != 'Texte_entier':
            filename = urllib.parse.unquote(path_elems[-1])
        else:
            filename = urllib.parse.unquote(path_elems[-2])

    # Opening output file
    outfile = io.open(filename, "w", encoding='utf-8')

    # Scrapping sections
    if chapitres == "oui":
        sections = chapters(book_location)
    else:
        sections.append(book_location.replace("https://fr.wikisource.org", ""))

    #grab all the text
    chapters = []
    for source_page in sections:
        location = "".join(["https://fr.wikisource.org", source_page])
        try:
            page = request.urlopen(location)
        except:
            print("No server is associated with the following page:")
            print(location)
            continue
        soup = BeautifulSoup(page, 'html.parser')
        print(location)
        text = soup.findAll("div", attrs={'class': 'prp-pages-output'})

        if len(text) == 0:
            print("This does not appear to be part of the text (no prp-pages-output tag at this location).")
            continue

        # Remove end of line inside sentence
        clean_text = re.sub("[^\.:!?»[A-Z]]\n", ' ', text[0].text)

        chapters.append(clean_text)

    #if the text has chapters, sample from each one. Otherwise take three samples.
    if chapitres == "oui":
        cutoff = int(char_limit / len(chapters))
        print(cutoff)
        outfile.write(urllib.parse.unquote(location) + '\n\n')
        for chap in chapters:
            sample = chap[0:cutoff]
            sample = re.sub("^.+?([.;!?])", "\\1", sample[::-1], 0, re.DOTALL)
            outfile.write(sample[::-1])
            outfile.write("\n\n\n\n\n\n")
    else:
        cutoff = int(char_limit / 3)
        inception_points = []
        inception_points.append(0)
        inception_points.append(int(len(chapters[0])/3))
        inception_points.append(int(len(chapters[0])/3) * 2)
        print(inception_points)
        samples = []
        for begin in inception_points:
            end = begin + cutoff
            s = chapters[0][begin:end]
            #clean the beginning and end of the sample
            s = re.sub("\\A\n*.+?([.;?!])", "", s)
            s = re.sub("^.+?([.;!?])", "\\1", s[::-1], 0, re.DOTALL)
            samples.append(s[::-1])
        samples[0] = re.sub("\\A.+\\n", "", samples[0])
        outfile.write(urllib.parse.unquote(location) + '\n\n')
        for sample in samples:
            outfile.write(sample)
            outfile.write("\n\n\n\n\n\n")
