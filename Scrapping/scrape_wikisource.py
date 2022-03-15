##################################################################
#L'idée de ce script, selon Motasem, est de générer 10% du roman entier,
#à condition que le résultat ne dépasse pas 10000 mots (sinon réduire le pourcentage).
# créé par James Gawley

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

#Copiez et collez l'adresse du livre sur wikisource :
book_location = "https://fr.wikisource.org/wiki/Germinie_Lacerteux/Texte_entier"

# Lisez s'il-vous plait:
"""Attention : s'il y a des accents ou des ponctuations dans le titre, il faut les retaper
soigneusement dans le fichier script. Par exemple, si vous copiez
"https://fr.wikisource.org/wiki/L'Éducation_sentimentale,_éd._Conard,_1910"
et le coller dans ce script, il peut être changé en
"https://fr.wikisource.org/wiki/L%E2%80%99%C3%89ducation_sentimentale,_%C3%A9d._Conard,_1910".
Le script ne s'exécutera pas et vous recevrez un message d'erreur."""

#Indiquez si le texte est divisé en chapitres : oui / non
chapitres = "non"

# Spécifiez un nom de fichier unique pour la sortie.
filename = "Goncourt-Lacerteux.txt"

# Personnalisez la longueur de l'échantillon / en caracteres
char_limit =  60000


##################################################################
"""Fin des options."""
##################################################################

from bs4 import BeautifulSoup
import urllib
from urllib import parse, request
import codecs
import re
import sys


outfile = codecs.open(filename, "w", encoding='utf-8')

sections = []
def chapters(book_location):
    # find the location of all chapters in a table-of-contents page
    book = book_location.replace("https://fr.wikisource.org/wiki/", "")
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

if chapitres == "oui":
    sections = chapters(book_location)
elif chapitres != "oui":
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
    clean_text = re.sub("[^\.:!?»]\n", ' ', text[0].text)

    chapters.append(clean_text)

#if the text has chapters, sample from each one. Otherwise take three samples.
if chapitres == "oui":
    cutoff = int(char_limit / len(chapters))
    print(cutoff)
    outfile.write(location)
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
    outfile.write(location)
    for sample in samples:
        outfile.write(sample)
        outfile.write("\n\n\n\n\n\n")
