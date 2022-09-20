

from document_index import simple_tokenizer


def replace_ending(x, y):
    return lambda s: s[:-len(x)] + y if s.endswith(x) else s 


def remove_ending(x):
    return replace_ending(x, "")

class StandardStemmer:
    def __init__(self, rules, dataset) -> None:
        self.rules = rules 
        self.dataset = dataset
    
    @staticmethod
    def from_file(path, rules):
        return StandardStemmer.from_string(open(path).read(), rules)
    
    @staticmethod
    def from_string(s, rules):
        return StandardStemmer(rules, simple_tokenizer(s))
    
    
    def __call__(self, word: str) -> str:
        word = word.lower()
        for rule in self.rules:
            if rule(word) in self.dataset:
                word = rule(word)
        return word


def english_rules():
    return [
        replace_ending("ies", "y"),
        replace_ending("ied", "y"),
        remove_ending("ed"),
        remove_ending("s"),
    ]


def stemmed_tokenizer(tokenizer, stemmer):
    return lambda x: [stemmer(token) for token in tokenizer(x)]