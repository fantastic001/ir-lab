
from operator import index
import unittest
from document_index import * 
from string_distance import * 
from document_index.stemming import * 

class TestDocumentIndex(unittest.TestCase):
    def test_simple_tokenizer(self):
        self.assertEqual(["a", "b", "c"], simple_tokenizer("  a  b   c"))
        self.assertEqual(["a", "b", "c"], simple_tokenizer("  a.  b .  c"))
    
    def test_postings_list(self):
        docs = PostingsList()
        docs.add("a")
        docs.add("b")
        docs.add("d")
        docs.add("c")
        self.assertEqual(len(docs), 4)
        self.assertEqual(docs.first(), "a")
        self.assertEqual(list(docs), ["a", "b", "c", "d"])
        self.assertEqual(list(docs + PostingsList()), ["a", "b", "c", "d"])
        self.assertEqual(list(docs + PostingsList.from_list(["e", "f"])), ["a", "b", "c", "d", "e", "f"])
        self.assertEqual(list(docs ^ PostingsList()), [])
        self.assertEqual(list(docs ^ PostingsList.from_list(["a"])), ["a"])
        self.assertEqual(list(docs ^ PostingsList.from_list(["d"])), ["d"])
        self.assertEqual(list(docs ^ PostingsList.from_list(["b", "c"])), ["b", "c"])
    
    def test_index(self):
        index = Index()
        index.add(Document("1", {"a", "b", "c"}))
        index.add(Document("2", {"b", "c", "d"}))
        self.assertEqual(list(index.query_all({"b", "c"})), ["1", "2"])
        self.assertEqual(list(index.query_all({"a", "b", "c"})), ["1"])
        self.assertEqual(list(index.query_all({"a", "b", "cjlkjkljkl"})), [])
            
    def test_stemming(self):
        dictionary = "play join fly we like to with"
        stemmer = StandardStemmer.from_string(dictionary, english_rules())
        self.assertEqual(stemmed_tokenizer(standard_tokenizer, stemmer)("We like to play with flies"), ["we", "like", "to", "play", "with", "fly"])
        self.assertEqual(stemmed_tokenizer(standard_tokenizer, stemmer)("We like then play"), ["we", "like", "play"])
    
    def test_standard_tokenizer(self):
        self.assertEqual(["a", "b", "c"], standard_tokenizer("  a  b   c"))
        self.assertEqual(["usa", "b", "c"], standard_tokenizer("  U.S.A  b   c"))
        self.assertEqual(["stefans", "b", "c"], standard_tokenizer("  Stefan's  b   c"))

        

class TestStringDistance(unittest.TestCase):

    def test_edit_distance(self):
        self.assertEqual(edit_distance("a", "a"), 0)
        self.assertEqual(edit_distance("", "a"), 1)
        self.assertEqual(edit_distance("a", "b"), 1)
        self.assertEqual(edit_distance("abc", "cba"), 2)
        self.assertEqual(edit_distance("abcd", "cbad"), 2)
        self.assertEqual(edit_distance("abcd", ""), 4)
    
    def test_char_set_distance(self):
        self.assertEqual(char_set_distance("ab", "b"), 1)
        self.assertEqual(char_set_distance("ab", "ba"), 0)
        self.assertEqual(char_set_distance("", "b"), np.inf)

    def test_tf_idf_distance(self):
        pass 
