import os
import re
import csv
import math
from bert_score import score
from datetime import date

if len(sys.argv) < 3:
	print("Usage : python tfidf_bm25_bert.py [texts_directory] [regex_liste.txt]")
	exit(1)
else:
	# Define the path to the folder of UTF-8 text files and the path to the regex file:
	text_folder_path = sys.argv[1]
	regex_file_path = sys.argv[2]

# Define a dictionary to hold the regex frequencies, tf-idf, bm25 and bert values:
regex_frequencies = {}
regex_tf = {}
regex_idf = {}
regex_tfidf = {}
regex_bm25 = {}
regex_bert = {}

# Read in the regex file and compile each regex pattern:
with open(regex_file_path, "r", encoding="utf-8") as regex_file:
    regex_patterns = [re.compile(pattern.strip()) for pattern in regex_file]
    print(f"Read {len(regex_patterns)} regex patterns from {regex_file_path}")

# Loop through each file in the text folder and count the frequency of each regex pattern
num_files = 0
for filename in os.listdir(text_folder_path):
    num_files += 1
    file_path = os.path.join(text_folder_path, filename)
    print(f"Processing file {file_path}")
    with open(file_path, "r", encoding="utf-8") as text_file:
        text = text_file.read()
        for pattern in regex_patterns:
            regex_count = len(re.findall(pattern, text))
            regex_name = pattern.pattern
            regex_frequencies[regex_name] = regex_frequencies.get(regex_name, 0) + regex_count
            if regex_count > 0:
                regex_tf[regex_name] = regex_tf.get(regex_name, []) + [regex_count]

# Calculate the IDF values for each regex pattern:
for regex_name, tf_list in regex_tf.items():
    idf = math.log(num_files / len(tf_list))
    regex_idf[regex_name] = idf

# Calculate the TF-IDF and BM25 weights for each regex pattern:
k1 = 1.2
b = 0.75
avg_doc_len = sum(len(tf_list) for tf_list in regex_tf.values()) / len(regex_tf)
for regex_name, tf_list in regex_tf.items():
    idf = regex_idf[regex_name]
    doc_len = len(tf_list)
    avg_len = avg_doc_len
    tf = sum(tf_list)
    tf_idf_weight = tf * idf
    bm25_weight = idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_len))))
    regex_tfidf[regex_name] = tf_idf_weight
    regex_bm25[regex_name] = bm25_weight

# Calculate the BERT score for each regex pattern:
for regex_name in regex_frequencies.keys():
    regex_bert[regex_name] = 0
for filename in os.listdir(text_folder_path):
    file_path = os.path.join(text_folder_path, filename)
    print(f"Processing file {file_path}")
    with open(file_path, "r", encoding="utf-8") as text_file:
        text = text_file.read()
        for regex_name in regex_frequencies.keys():
            if re.search(regex_name, text):
                #p, r, f1 = score([regex_name], [text])
                p, r, f1 = score([regex_name], [text], lang="fr")
                regex_bert[regex_name] += f1.item()

# Write the regex frequencies, TF, IDF, BM25, and BERT scores to a CSV file:
output_file_path = "output_" + date.today() + ".csv"
with open(output_file_path, "w", encoding="utf-8", newline="") as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(["Regex", "Frequency", "TF-IDF", "BM25", "BERT"])
    for regex_name, frequency in regex_frequencies.items():
        tf_idf = round(regex_tfidf.get(regex_name, 0), 2)
        bm25 = round(regex_bm25.get(regex_name, 0), 2)
        bert_score = round(regex_bert.get(regex_name, 0), 2)
        csv_writer.writerow([regex_name, frequency, tf_idf, bm25, bert_score])
    print(f"Wrote {len(regex_frequencies)} regex frequencies, TF-IDF, BM25, and BERT scores to {output_file_path}")

