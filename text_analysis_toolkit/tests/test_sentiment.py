import unittest
from text_analysis_toolkit.sentiment import SentimentAnalyzer


class TestSentimentAnalyzer(unittest.TestCase):
    def setUp(self):
        self.sa = SentimentAnalyzer()

    def test_empty_tokens(self):
        score = self.sa.score([])
        self.assertEqual(score, 0.0)

    def test_positive_score(self):
        tokens = ["good", "great", "excellent", "bad"]
        score = self.sa.score(tokens)
        self.assertGreater(score, 0)

    def test_negative_score(self):
        tokens = ["bad", "terrible", "awful", "good"]
        score = self.sa.score(tokens)
        self.assertLess(score, 0)

    def test_neutral_score(self):
        tokens = ["the", "cat", "sat", "mat"]
        score = self.sa.score(tokens)
        self.assertEqual(score, 0.0)

    def test_detailed_score(self):
        tokens = ["good", "bad", "happy", "sad"]
        d = self.sa.detailed_score(tokens)
        self.assertIn("sentiment_score", d)
        self.assertIn("sentiment_label", d)
        self.assertIn("positive_count", d)
        self.assertIn("negative_count", d)

    def test_positive_matches(self):
        tokens = ["good", "bad", "great", "terrible"]
        matches = self.sa.positive_matches(tokens)
        self.assertIn("good", matches)
        self.assertIn("great", matches)
        self.assertNotIn("bad", matches)

    def test_negative_matches(self):
        tokens = ["good", "bad", "great", "terrible"]
        matches = self.sa.negative_matches(tokens)
        self.assertIn("bad", matches)
        self.assertIn("terrible", matches)
        self.assertNotIn("good", matches)

    def test_label_positive(self):
        self.assertEqual(self.sa._label(0.5), "positive")

    def test_label_negative(self):
        self.assertEqual(self.sa._label(-0.5), "negative")

    def test_label_neutral(self):
        self.assertEqual(self.sa._label(0.0), "neutral")

    def test_label_positive_threshold(self):
        self.assertEqual(self.sa._label(0.3), "neutral")
        self.assertEqual(self.sa._label(0.31), "positive")

    def test_label_negative_threshold(self):
        self.assertEqual(self.sa._label(-0.3), "neutral")
        self.assertEqual(self.sa._label(-0.31), "negative")

    def test_custom_lexicon(self):
        sa = SentimentAnalyzer(
            positive_words={"foo"},
            negative_words={"bar"}
        )
        self.assertEqual(sa.score(["foo"]), 1.0)
        self.assertEqual(sa.score(["bar"]), -1.0)
        self.assertEqual(sa.score(["foo", "bar"]), 0.0)

    def test_properties(self):
        self.assertIsInstance(self.sa.positive_words, frozenset)
        self.assertIsInstance(self.sa.negative_words, frozenset)


if __name__ == "__main__":
    unittest.main()
