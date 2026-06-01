import unittest
from text_analysis_toolkit.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.tk = Tokenizer()

    def test_empty_string(self):
        self.assertEqual(self.tk.tokenize(""), [])

    def test_whitespace_string(self):
        self.assertEqual(self.tk.tokenize("   "), [])

    def test_basic_tokenization(self):
        tokens = self.tk.tokenize("Hello World")
        self.assertEqual(tokens, ["hello", "world"])

    def test_punctuation_removal(self):
        tokens = self.tk.tokenize("Hello, World! How are you?")
        self.assertEqual(tokens, ["hello", "world", "how", "are", "you"])

    def test_lower_false(self):
        tk = Tokenizer(lower=False)
        tokens = tk.tokenize("Hello World")
        self.assertEqual(tokens, ["Hello", "World"])

    def test_remove_punct_false(self):
        tk = Tokenizer(remove_punct=False)
        tokens = tk.tokenize("Hello, World!")
        self.assertEqual(tokens, ["hello,", "world!"])

    def test_stopword_removal(self):
        tk = Tokenizer(remove_stopwords=True)
        tokens = tk.tokenize("the quick brown fox jumps over the lazy dog")
        expected = ["quick", "brown", "fox", "jumps", "lazy", "dog"]
        self.assertEqual(tokens, expected)

    def test_custom_stopwords(self):
        tk = Tokenizer(remove_stopwords=True, stopwords=["hello", "world"])
        tokens = tk.tokenize("Hello World foo bar")
        self.assertEqual(tokens, ["foo", "bar"])

    def test_sentence_split(self):
        sentences = self.tk.sentence_split("Hello world. How are you? I am fine!")
        self.assertEqual(sentences, ["Hello world.", "How are you?", "I am fine!"])

    def test_ngrams(self):
        self.tk.remove_punct = False
        self.tk.lower = False
        tokens = ["the", "quick", "brown", "fox"]
        grams = self.tk.ngrams(tokens, 2)
        self.assertEqual(grams, ["the quick", "quick brown", "brown fox"])

    def test_ngrams_invalid_n(self):
        tokens = ["a", "b"]
        self.assertEqual(self.tk.ngrams(tokens, 3), [])

    def test_stopwords_property(self):
        tk = Tokenizer(stopwords=["a", "b"])
        sw = tk.stopwords
        self.assertIn("a", sw)
        with self.assertRaises(AttributeError):
            sw.add("c")


if __name__ == "__main__":
    unittest.main()
