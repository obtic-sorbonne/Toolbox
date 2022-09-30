import sys
import os
from bs4 import BeautifulSoup
from keybert import KeyBERT
import torch
from transformers import BertTokenizerFast, EncoderDecoderModel
from summarizer import Summarizer,TransformerSummarizer


# Initialisation BERT
bert_model = Summarizer()

# Initialisation GPT2
GPT2_model = TransformerSummarizer(transformer_type="GPT2",transformer_model_key="gpt2-medium")

# Initialisation Bert pour l'espagnol
"""device = 'cuda' if torch.cuda.is_available() else 'cpu'
ckpt = 'mrm8488/bert2bert_shared-spanish-finetuned-summarization'
tokenizer = BertTokenizerFast.from_pretrained(ckpt)
model = EncoderDecoderModel.from_pretrained(ckpt).to(device)"""


def tokenise(text):
	PUNCT = [',', '.', '?', '!', "'", '"', '“', '”', ':','‘','’', ';', '—', '‘', '’']
	return "".join(c for c in text if c not in PUNCT)

# Compte le nombre de mots
def count_words(soup):
	nb_words = 0
	p_content = soup.find_all('p')
	for p in p_content:
		tokens = tokenise(p.text)
		words = tokens.split(' ')
		nb_words += len(words)

	titles = soup.find_all('title')
	for t in titles:
		tokens = tokenise(t.text)
		words = tokens.split(' ')
		nb_words += len(words)

	return nb_words


# Génère un résumé avec le modèle Bert
def generate_summary(text):
   inputs = tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
   input_ids = inputs.input_ids.to(device)
   attention_mask = inputs.attention_mask.to(device)
   output = model.generate(input_ids, attention_mask=attention_mask)
   return tokenizer.decode(output[0], skip_special_tokens=True)

# Writing output
def writeHTML(filepath, title, nb_words, m, abstract_summary, overview, intro_summary, conclusion_summary):
	filename = os.path.basename(filepath)
	outputname = "cubierta_" + os.path.splitext(filename)[0] + '.html'
	new_soup = BeautifulSoup('<!doctype html>\
	<html><body>\
	<h1></h1>\
	<div id="info"><p id="nb_words"></p><p id="reading_time"></p></div>\
	<div><p id="en_abstract"></p></div>\
	<h2>Overview</h2>\
	<div id="overview"><ul></ul></div>\
	<div><h2>Introduction Summary</h2>\
	<p id="intro_summary"></p>\
	<h2>Conclusion Summary</h2>\
	<p id="conclusion_summary"></p>\
	</body></html>', 'html.parser')

	# Write title
	new_soup.h1.string = title

	# Write number of words
	p = new_soup.find(id="nb_words")
	p.insert(1, "Number of words: " + str(nb_words))

	# Write reading time
	p = new_soup.find(id="reading_time")
	p.insert(1, "Reading time: " + str(int(m)) + " minutes")

	# Write abstract
	p = new_soup.find(id="en_abstract")
	p.insert(1, abstract_summary)

	# Write overview
	for sec_title, keywords in overview.items():
		h3 = new_soup.new_tag('li')
		h3.string = sec_title
		div = new_soup.find(id="overview")
		div.append(h3)

		keywords_list = [x[0] for x in keywords if x[1] > 0.46]
		p = new_soup.new_tag('span')
		p.string = ", ".join(keywords_list)
		h3.append(p)

	# Write introduction summary
	p = new_soup.find(id="intro_summary")
	p.insert(1, intro_summary)

	p = new_soup.find(id="conclusion_summary")
	p.insert(1, conclusion_summary)

	with open(outputname, 'w') as output:
		output.write(str(new_soup.prettify()))


# Lecture paramètres
if len(sys.argv) < 2:
	print("File name missing.\n")
	sys.exit(1)
else:
	filepath = sys.argv[1]


# Lecture du fichier d'entrée
with open(filepath, 'r') as f:
	content = f.read()

soup = BeautifulSoup(content, 'xml')

# Titre de l'article
title = soup.find('article-title').text
print("Title: {}".format(title))

# Nombre de mots
nb_words = count_words(soup)
print("Number of words : {}".format(nb_words))

# Temps de lecture
# Reading time : seconds = num_words / 265 * 60 + img_weight * num_images
nb_fig = len(soup.find_all('fig'))
seconds = nb_words / 200 * 60 + 10 * nb_fig
m, s = divmod(seconds, 60)
print("Reading time: {}".format(int(m)))

# Parsing des abstracts
abstracts = soup.find_all('abstract')
bert_summary = ""
bert_resumen = ""

for abstract in abstracts:
	if abstract.title.text.lower() == 'abstract':
		en_abstract = abstract.p.text
		abstract_summary = ''.join(bert_model(en_abstract, min_length=50))
		print("Abstract BERT: {}".format(abstract_summary))

		abstract_summary_gpt2 = ''.join(GPT2_model(en_abstract, min_length=50))
		print("Abstract GPT2: {}".format(abstract_summary_gpt2))

	#elif abstract.title.text.lower() == 'resumen':
		#esp_abstract = abstract.p.text
		#bert_resumen = generate_summary(esp_abstract)
		#print("Resumen : {}".format(bert_resumen))


# Mots-clés par section
intro_summary = ""
conclusion_summary = ""

kw_model = KeyBERT()
sections = soup.find_all('sec')
overview = {}
for sec in sections:
	current_sec_title = sec.title.text
	print("Section title : {}".format(current_sec_title))
	current_text = sec.p.text


	# Résumé introduction
	if current_sec_title.lower() == 'introduction':
		intro_summary = ''.join(bert_model(current_text, min_length=50))
		print("Introduction summary (BERT): {}\n".format(intro_summary))

		"""# Summarisation with GPT2
		intro_summary_gpt2 = ''.join(GPT2_model(current_text, min_length=50))
		print("Introduction summary (GPT2): {}\n".format(intro_summary_gpt2))"""

	# Résumé conclusion
	elif 'conclusion' in current_sec_title.lower():
		conclusion_summary = ''.join(bert_model(current_text, min_length=50))
		print("Conclusion summary (BERT): {}\n".format(conclusion_summary))

		"""conclusion_summary_gpt2 = ''.join(GPT2_model(current_text, min_length=50))
		print("Conclusion summary (GPT2): {}\n".format(conclusion_summary_gpt2))"""


	"""keywords_MMR = kw_model.extract_keywords(current_text, keyphrase_ngram_range=(1, 2), stop_words='english',
							  use_mmr=True, diversity=0.6)
	print("Keywords with MMR: {}\n".format(keywords_MMR))"""

	keywords_MSD = kw_model.extract_keywords(current_text, keyphrase_ngram_range=(1, 3), stop_words='english',
							  use_maxsum=True, nr_candidates=30, top_n=5)
	print("Keywords with MSD: {}\n".format(keywords_MSD))

	overview[current_sec_title] = keywords_MSD


writeHTML(filepath, title, nb_words, m, abstract_summary, overview, intro_summary, conclusion_summary)
