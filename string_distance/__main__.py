import sys 
import os 
from string_distance import * 
from document_index import simple_tokenizer
import pandas as pd 
from itertools import combinations

collection = []
for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        path = os.path.join(root, file)
        with open(path) as f:
            collection = collection + simple_tokenizer(f.read())




data = [] 
for x,y in combinations(set(collection), 2):
    data.append({
        "pair": "%s %s" % (x,y),
        "edit_distance": edit_distance(x,y),
        "set_distance": char_set_distance(x,y),
        "tf-idf_distance": vector_distance(x,y,collection)
    })

print(pd.DataFrame(data).corr("kendall").to_markdown())