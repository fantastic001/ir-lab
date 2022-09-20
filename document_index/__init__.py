from typing import List
import string

class Document:
    def __init__(self, id, terms):
        self.id = id 
        self.terms = terms
    

def remove_non_alphanumeric(s: str) -> str:
    return "".join(c for c in s if c.isalnum())

def simple_tokenizer(content: str) -> List[str]:
    return set([remove_non_alphanumeric(s) for s in content.split(" ") if remove_non_alphanumeric(s) != ""])


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
    def __init__(self) -> None:
        self.children = [] 

class BIndex:
    pass 