import unittest
from text_analysis_toolkit.frequency import FrequencyAnalyzer


class TestFrequencyAnalyzer(unittest.TestCase):
    def test_empty_tokens(self):
        fa = FrequencyAnalyzer([])
        self.assertEqual(fa.total_words, 0)
        self.assertEqual(fa.unique_words, 0)
        self.assertEqual(fa.word_counts(), {})
        self.assertEqual(fa.top_words(), [])

    def test_basic_counts(self):
        tokens = ["a", "b", "a", "c", "a", "b"]
        fa = FrequencyAnalyzer(tokens)
        self.assertEqual(fa.total_words, 6)
        self.assertEqual(fa.unique_words, 3)
        self.assertDictEqual(fa.word_counts(), {"a": 3, "b": 2, "c": 1})

    def test_top_words(self):
        tokens = ["a", "b", "b", "c", "c", "c"]
        fa = FrequencyAnalyzer(tokens)
        self.assertEqual(fa.top_words(2), [("c", 3), ("b", 2)])

    def test_term_frequency(self):
        tokens = ["a", "a", "b"]
        fa = FrequencyAnalyzer(tokens)
        self.assertEqual(fa.term_frequency("a"), 2 / 3)
        self.assertEqual(fa.term_frequency("c"), 0.0)

    def test_relative_frequencies(self):
        tokens = ["x", "x", "y"]
        fa = FrequencyAnalyzer(tokens)
        rf = fa.relative_frequencies()
        self.assertAlmostEqual(rf["x"], 2 / 3)
        self.assertAlmostEqual(rf["y"], 1 / 3)

    def test_words_above_threshold(self):
        tokens = ["a", "a", "b", "c", "c", "c"]
        fa = FrequencyAnalyzer(tokens)
        above = fa.words_above_threshold(1)
        self.assertIn(("a", 2), above)
        self.assertIn(("c", 3), above)
        self.assertNotIn(("b", 1), above)

    def test_len(self):
        fa = FrequencyAnalyzer(["a", "b", "c"])
        self.assertEqual(len(fa), 3)

    def test_repr(self):
        fa = FrequencyAnalyzer(["a", "b", "c"])
        self.assertIn("3 tokens", repr(fa))

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            FrequencyAnalyzer("not a list")

    def test_tokens_property_immutable(self):
        original = ["a", "b"]
        fa = FrequencyAnalyzer(original)
        tokens_copy = fa.tokens
        tokens_copy.append("c")
        self.assertEqual(len(fa), 2)


if __name__ == "__main__":
    unittest.main()
