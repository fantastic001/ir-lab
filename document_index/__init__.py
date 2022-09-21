from distutils.command.config import config
from gettext import bindtextdomain
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



class BNode:
    class Config:
        RANK = 5
    def __init__(self, children, data, last, parent, rank=Config.RANK) -> None:
        self.children = children
        self.data = data 
        self.last = last 
        self.parent = parent 
        self.rank = rank 
    
    def add(self, key, data):
        if len(self.children) < 2*self.rank:
            self.data[key] = data
            self.children[key] = None
            return self 
        else:
            self.data[key] = data 
            self.children[key] = None 
            keys = list(self.children.keys())
            mid = keys[len(keys)//2]
            left = [x for x in keys if x < mid] 
            right = [x for x in keys if x > mid]
            right_data = {x: self.data[x] for x in keys if x in right}
            right_children = {x: self.children[x] for x in keys if x in right}
            right_last = self.last 
            self.last = self.children[mid]
            mid_data = self.data[mid]
            self.data = {x: self.data[x] for x in left}
            self.children = {x: self.children[x] for x in left}
            if self.parent is None:
                self.parent = BNode({
                        mid: self
                    }, {
                        mid: mid_data
                    }, 
                    BNode(right_children, right_data, right_last, None, self.rank),
                    None, 
                    self.rank
                )
                self.parent.last.parent = self.parent
                return self.parent
            else:
                node = self.parent.add(mid, mid_data)
                node.children[mid] = self
                mid_right = [x for x in node.children.keys() if  x > mid] 
                if len(mid_right) == 0:
                    node.last = BNode(right_children, right_data, right_last, node, self.rank)
                else:
                    node.children[min(mid_right)] = BNode(right_children, right_data, right_last, node, self.rank)
                return node 

class BTree:
    def __init__(self) -> None:
        self.root = BNode(dict(), dict(), None, None, BNode.Config.RANK)
    def add(self, key, data):
        curr = self.root 
        while curr.last is not None:
            # find minimal key greater than needed 
            right = [x for x in curr.data.keys() if x > key]
            if len(right) == 0:
                curr = curr.last
            else:
                curr = curr.children[min(right)]
        curr.add(key, data)
        while self.root.parent is not None:
            self.root = self.root.parent
    
    def get(self, key, default):
        curr = self.root 
        while key not in curr.data and curr.last is not None:
            # find minimal key greater than needed 
            right = [x for x in curr.data.keys() if x > key]
            if len(right) == 0:
                curr = curr.last
            else:
                curr = curr.children[min(right)]
        if key not in curr.data:
            return default 
        else:
            return curr.data[key]
class Index:
    def __init__(self) -> None:
        self.data = BTree()
    
    def add(self, doc: Document):
        for term in doc.terms:
            plist = self.data.get(term, None)
            if plist is None:
                self.data.add(term, PostingsList.from_list([doc.id]))
            else:
                plist.add(doc.id)
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