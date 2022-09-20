import string
from typing import Callable, Set
from typing import List
import numpy as np 
class Document:
    def __init__(self, id, terms):
        self.id = id 
        self.terms = terms
    
    @staticmethod
    def from_file(path: str, tokenizer: Callable[[str], List[str]]) -> "Document":
        result = None
        with open(path) as f:
            result =  Document(path, set(tokenizer(f.read())))
        return result
    

def remove_non_alphanumeric(s: str) -> str:
    return "".join(c for c in s if c.isalnum())

def simple_tokenizer(content: str) -> List[str]:
    return [remove_non_alphanumeric(s) for s in content.split(" ") if remove_non_alphanumeric(s) != ""]


def standard_tokenizer(content: str) -> List[str]:
    result = [] 
    prev = ""
    A = string.ascii_letters + string.digits
    is_alnum = lambda x: x in A 
    current = ""
    for c in content:
        if is_alnum(c):
            current = current + c 
        else:
            if c not in "'." or not is_alnum(prev):
                if current != "":
                    result.append(current.lower())
                    current = ""
        prev = c
    if current != "":
        result.append(current)
    return result 

class PostingsList:

    @staticmethod
    def from_list(l):
        result = PostingsList()
        for x in l:
            result.add(x)
        return result 

    def __init__(self) -> None:
        self.next = None
        self.value = None
        self.size = 0 
    def add(self, doc: Document):
        self.size += 1
        if self.value is None:
            self.value = doc
        else:
            if self.next is None:
                if self.value < doc:
                    self.next = PostingsList()
                    self.next.add(doc)
                else:
                    self.next = PostingsList()
                    self.next.value = self.value
                    self.value = doc
            else:
                if self.value < doc:
                    self.next.add(doc)
                else:
                    value = self.value
                    self.value = doc 
                    self.next.add(value)
                
    def __len__(self):
        return self.size
    
    def first(self):
        return self.value
    
    def __iter__(self):
        if self.value is None:
            return 
        else: 
            yield self.value 
            if self.next is not None:
                for d in self.next:
                    yield d 
    
    def __add__(self, other):
        result = PostingsList()
        x = self 
        y = other
        while x is not None and x.value is not None and y is not None and y.value is not None:
            if x.value == y.value:
                result.add(x.value)
                x = x.next 
                y = y.next
            elif x.value < y.value:
                result.add(x.value)
                x = x.next
            else:
                result.add(y.value)
                y = y.next 
        if x is not None and x.value is not None:
            for d in x:
                result.add(d)
        if y is not None and y.value is not None:
            for d in y:
                result.add(d)
        return result 
    
    def __xor__(self, other):
        result = PostingsList()
        x = self 
        y = other
        while x is not None and x.value is not None and y is not None and y.value is not None:
            if x.value == y.value:
                result.add(x.value)
                x = x.next 
                y = y.next
            elif x.value < y.value:
                x = x.next
            else:
                y = y.next 
        return result 


class Index:
    def __init__(self) -> None:
        self.data = {}
    
    def add(self, doc: Document):
        for term in doc.terms:
            if term not in self.data:
                self.data[term] = PostingsList.from_list([doc.id])
            else:
                self.data[term].add(doc.id)
    def query_all(self, terms: Set[str]):
        plists = sorted([self.data.get(term, PostingsList()) for term in terms], key = lambda x: len(x))
        result = plists[0]
        for p in plists[1:]:
            result = result ^ p
        return result 

def vectorize(doc: str, collection: List[str]):
    A = string.ascii_letters + string.digits
    return np.array([np.log(1 + len([c for c in doc if c == x]) / len(doc)*(
        np.log(len(collection) / len([d for d in collection if x in d])) if any(x in c for c in collection) else 0 
    )) for x in A])