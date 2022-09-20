
from operator import index
import unittest
from document_index import * 


class TestDocumentIndex(unittest.TestCase):
    def test_simple_tokenizer(self):
        self.assertEqual({"a", "b", "c"}, simple_tokenizer("  a  b   c"))
        self.assertEqual({"a", "b", "c"}, simple_tokenizer("  a.  b .  c"))
    
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



