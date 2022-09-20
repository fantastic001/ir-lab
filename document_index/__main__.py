
from document_index.stemming import StandardStemmer, english_rules, stemmed_tokenizer
import sys
from document_index import * 
import os 

index = Index()


dictionary = ""
for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        dictionary = dictionary + open(os.path.join(root, file)).read()
english_stemmer = StandardStemmer.from_string(
                dictionary, 
                english_rules()
)
for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        index.add(Document.from_file(os.path.join(root, file), stemmed_tokenizer(
            standard_tokenizer, 
            english_stemmer
        )))

is_finished = lambda q: q in ["exit", "quit"]

tokenizer = stemmed_tokenizer(standard_tokenizer, english_stemmer)

while True:
    query = input(">>> ")
    if is_finished(query):
        break
    for path in index.query_all(set((tokenizer(query)))):
        print(path)