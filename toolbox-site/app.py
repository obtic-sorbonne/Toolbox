import os
from flask import Flask, flash, request, render_template, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename

from lxml import etree

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)

# App config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'pakisqa'

app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024 # Limit file upload to 3MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)

#-----------------------------------------------------------------
# ROUTES
#-----------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/numeriser')  
def numeriser():
	return render_template('numeriser.html')

@app.route('/creer_corpus')
def creer_corpus():
	return render_template('creer_corpus.html')

@app.route('/conversion_xml')
def conversion_xml():
	return render_template('conversion_xml.html')
	
@app.route('/converter', methods=["GET", "POST"])
def xmlconverter():
	if request.method == 'POST':
		fields = {}

		f = request.files['file']
		fields['title'] = request.form['title'] # required
		fields['author'] = request.form.get('author')
		fields['respStmt_name'] = request.form.get('nameresp')
		fields['respStmt_resp'] = request.form.get('resp')
		fields['pubStmt'] = request.form['pubStmt'] # required
		fields['sourceDesc'] = request.form['sourceDesc'] # required

		filename = secure_filename(f.filename)
		path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		f.save(path_to_file)
		try:
			with open(path_to_file, "r") as f:
				for l in f:
					break;
			outputname = txt_to_xml(path_to_file, fields)
			print(outputname)
		except UnicodeDecodeError:
			return 'format de fichier incorrect'

		return 'upload successful' #redirect(url_for(''))

	return render_template("/conversion_xml")

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


#-----------------------------------------------------------------
# FONCTIONS de traitement
#-----------------------------------------------------------------

# CONVERSION XML-TEI
# Construit un fichier TEI à partir des métadonnées renseignées dans le formulaire.
# Renvoie le chemin du fichier ainsi créé
# Paramètres :
# - filename : emplacement du fichier uploadé par l'utilisateur
# - fields : dictionnaire des champs présents dans le form metadata
def txt_to_xml(filename, fields):
	# Initialise TEI
	root = etree.Element("TEI")

	# TEI header
	teiHeader = etree.Element("teiHeader")
	fileDesc = etree.Element("fileDesc")
	titleStmt = etree.Element("titleStmt")
	editionStmt = etree.Element("editionStmt")
	publicationStmt = etree.Element("publicationStmt")
	sourceDesc = etree.Element("sourceDesc")

	#- TitleStmt
	#-- Title
	title = etree.Element("title")
	title.text = fields['title']
	titleStmt.append(title)

	#-- Author
	if fields['author']:
		author = etree.Element("author")
		author.text = fields['author']
		titleStmt.append(author)

	#- EditionStmt
	#-- respStmt
	if fields['respStmt_name']:
		respStmt = etree.Element("respStmt")
		name = etree.Element("name")
		name.text = fields['respStmt_name']
		respStmt.append(name)

		if fields['resp']:
			resp = etree.Element("resp")
			resp.text = fields['respStmt_resp']
			respStmt.append(resp)

		editionStmt.append(respStmt)

	#- PublicationStmt
	publishers_list = fields['pubStmt'].split('\n') # Get publishers list
	publishers_list = list(map(str.strip, publishers_list)) # remove trailing characters
	publishers_list = [x for x in publishers_list if x] # remove empty strings
	for pub in publishers_list:
		publisher = etree.Element("publisher")
		publisher.text = pub
		publicationStmt.append(publisher)

	#- SourceDesc
	paragraphs = fields['sourceDesc'].split('\n')
	for elem in paragraphs:
		p = etree.Element('p')
		p.text = elem
		sourceDesc.append(p)
		
	# Header
	fileDesc.append(titleStmt)
	fileDesc.append(editionStmt)
	fileDesc.append(publicationStmt)
	fileDesc.append(sourceDesc)
	teiHeader.append(fileDesc)
	root.append(teiHeader)

	# Text
	text = etree.Element("text")
	
	with open(filename, "r") as f:
		for line in f:
			ptext = etree.Element('p')
			ptext.text = line
			text.append(ptext)

	root.append(text)

	output = os.path.splitext(filename)[0] + '.xml'
	etree.ElementTree(root).write(output, pretty_print=True, xml_declaration=True, encoding="utf-8")
	return output
#-----------------------------------------------------------------


if __name__ == '__main__':
   app.debug = True
   app.run()
