# importer les librairies nécessaires
import os, re, glob, csv
from spellchecker import SpellChecker
from lxml import etree
from collections import Counter

    

# ignorer les fichiers cachés dans le directoire avec les docs d'entrée (p. ex. le '._5419000_r.xml')
def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))



# spécifier les docs d'entrée (échantillon) à partir desquels les sorties corrigées seront générées
directory_in = listdir_nohidden("./sample_in/")



# enlever l'extension .xml des fichiers d'entrée
for file_in in directory_in:
    tree = etree.parse(file_in)
    root = tree.getroot()
    file_in = os.path.basename(file_in)
    file_in = os.path.splitext(file_in)[0]
    # print(file_in) # 5419000_r, test
    
 

    # créer les nouveaux fichiers .txt sur lesquels les corrections seront appliquées par la suite
    file_out = '{}'.format(file_in)+'.txt'
    # print(file_out) # 5419000_r.txt, test.txt
    directory_out = os.path.join("./sample_out/", file_out)
  

    
    # créer les nouveaux fichiers .csv où les erreurs avec leurs corrections seront enregistrées
    corr_out = os.path.join('./csv/', file_in+'.csv')
     
    
    # les caractères spéciaux à enlever
    car_spec = ['■', '•', '%', '*', '#', '+', '^', '\\', '$', '>', '<', '£', '{', '}']
    
    # générer un tableur .csv où les erreurs, les corrections et les fréquences d'erreurs seront stockées
    with open(directory_out, 'w') as f, open(corr_out, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(["Erreur"'\t' "Correction"'\t' "Fréquence"'\t'])
        
        # enlever les balises XML afin de transférer le contenu des fichiers .xml dans les fichiers .txt



        for elem in root.iter('*'):
            if elem.text is not None:
                text = elem.text.strip()
                if elem.tail is not None:
                     text = elem.text.strip() + str(elem.tail) # pour récupérer le texte dans la balise imbriquée
                                                               # ex : par le moyen des <hi rend="i">emblèmes</hi>,
                if text:
                    for c in car_spec:
                        text = text.replace(c,'')

                    
                    # pré-traitements
                    text = re.sub('&', 'et', text) # l'esperluette '&' signifie 'et'
                    text = re.sub('« \n', '', text) # pour concaténer les mots séparés par un trait d'union
                                                    # (sous forme d'un guillemet français ouvert)
                    text = re.sub(" +", " ", text)  # réduire les espaces multiples en un seul espace
                    text = text.lower() # conversion en minuscules
                    text = text.replace("\n", " ") # pour que chaque ligne commence depuis le tout début,
                                                   # et non pas après un espace
                    
                    # remplacer le guillemet simple par un guillemet français, pour éviter le problème de parsing
                    text = text.replace("'", "’")
                    
                    # effacer l'espace avant certains caractères spéciaux
                    text = text.replace(' ,', ',')
                    text = text.replace(' .','. ')
                    text = text.replace(' :',':')
                    text = text.replace(' ;',';')
                    text = text.replace(' !','!')
                    text = re.sub('\s\?','?', text)
                    text = text.replace(' "','"')
                    text = text.replace('( ','(')
                    text = text.replace(' )',')')
                    text = text.replace(' –','-')
                    
                    # remplacer les tirets moyens et longs par les tirets courts
                    text = text.replace('–', '-')
                    
                    
                    # enlever les signes de ponctuation se trouvant à la fin d'un token
                    # car le signe de ponctuation empêche le correcteur de corriger la séquence
                    # 'token + signe de ponctuation', même si le token est en effet écrit incorrectement
                    # ex: 'jeuneffe,' (avec virgule) > 'jeuneffe' (incorrect)
                    # au lieu de 'jeuneffe' (sans virgule) > 'jeunesse' (correct)
                    text = re.sub('(?<=\w)[,;:?!.]', '', text)
                    
                            

                    # définir le correcteur d'orthographe français
                    # pyspellchecker
                    spell = SpellChecker(language='fr')

                   
                
                    # tokeniser le texte avec le tokeniseur standard (ex: 'l'empire')
                    # car celui de pyspellchecker tokenise mal (ex: 'l', 'empire')
                    token_list = text.split()


                    for t in token_list:
                    # ne pas corriger les tokens contenant l'apostrophe (ex : l’empire, d’art, s’étend...)
                    # ne pas corriger les tokens en parenthèses non plus (ex : (1716-1790))
                        r1 = re.findall(r"(l’\w+|l’\w+-\w+|d’\w+|d’\w+|qu’\w+|c’\w+|n’\w+|j’\w+|lorfqu’\w+|eft|\w+.*?\)|\(.*?.\)|\(.*$)", t)
                        spell.word_frequency.load_words(r1)
                        a = spell.known(r1)  # les mots {'ex : l’empire, d’art, s’étend'} sont désormais
                                             # dans le dictionnaire des mots corrects
                        
                    
                    
                    # corriger les mots incorrects dans le fichier .txt
                    # extraire les erreurs, leurs fréquences et leurs corrections dans un tableur .csv
                    misspelled = spell.unknown(token_list)
                 
                    
                    
                    for m in misspelled:
                        corrected = spell.correction(m)
                        if m in token_list:
                            m_freq = token_list.count(m)
                            # print(m_freq)
                        # print(m, corrected, str(m_freq))
                        text = text.replace(m, corrected)
                        # f.write(c.replace('clafliques', 'classiques'))

                        fout.write(m+'\t' + corrected+'\t' + str(m_freq)+' \n')
#                     print(text)
                    f.write(text + "\n")
