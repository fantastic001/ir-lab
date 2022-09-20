
import sys
from document_index import * 
import os 

index = Index()

for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        index.add(Document.from_file(os.path.join(root, file), simple_tokenizer))

is_finished = lambda q: q in ["exit", "quit"]

while True:
    query = input(">>> ")
    if is_finished(query):
        break
    for path in index.query_all(set(simple_tokenizer(query))):
        print(path)