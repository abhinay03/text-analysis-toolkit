import unittest
import tempfile
import os
from text_analysis_toolkit.analyzer import TextAnalyzer


SAMPLE_TEXT = """
The quick brown fox jumps over the lazy dog. This is a simple sentence for testing.
The dog was lazy but the fox was quick. Good things come to those who wait.
This is terrible and bad. I love this amazing world!
"""


class TestTextAnalyzer(unittest.TestCase):
    def setUp(self):
        self.ta = TextAnalyzer()

    def test_analyze_returns_dict(self):
        result = self.ta.analyze(SAMPLE_TEXT)
        self.assertIn("statistics", result)
        self.assertIn("frequencies", result)
        self.assertIn("sentiment", result)
        self.assertIn("ngrams", result)
        self.assertIn("tokens", result)

    def test_analyze_statistics(self):
        result = self.ta.analyze("Hello world. How are you?")
        stats = result["statistics"]
        self.assertEqual(stats["total_words"], 5)
        self.assertEqual(stats["sentences"], 2)

    def test_analyze_sentiment_in_result(self):
        result = self.ta.analyze(SAMPLE_TEXT)
        sentiment = result["sentiment"]
        self.assertIn("sentiment_score", sentiment)
        self.assertIn("sentiment_label", sentiment)

    def test_analyze_ngrams(self):
        result = self.ta.analyze("the quick brown fox")
        self.assertIn("2", result["ngrams"])
        self.assertIn("3", result["ngrams"])

    def test_analyze_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write(SAMPLE_TEXT)
            tmp_path = f.name
        try:
            result = self.ta.analyze_file(tmp_path)
            self.assertIn("statistics", result)
        finally:
            os.unlink(tmp_path)

    def test_analyze_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.ta.analyze_file("nonexistent_file.txt")

    def test_report_text(self):
        result = self.ta.analyze(SAMPLE_TEXT)
        report = self.ta.report_text(result)
        self.assertIn("Text Analysis Report", report)
        self.assertIn("Sentiment", report)

    def test_report_json(self):
        result = self.ta.analyze(SAMPLE_TEXT)
        report = self.ta.report_json(result)
        self.assertIn("statistics", report)
        self.assertIn("frequencies", report)

    def test_custom_stopwords(self):
        ta = TextAnalyzer(remove_stopwords=True)
        result = ta.analyze("the cat sat on the mat")
        stats = result["statistics"]
        self.assertLess(stats["total_words"], 6)


if __name__ == "__main__":
    unittest.main()
