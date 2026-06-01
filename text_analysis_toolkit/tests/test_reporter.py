import unittest
import json
import tempfile
import os
from text_analysis_toolkit.reporter import ReportGenerator
from text_analysis_toolkit.frequency import FrequencyAnalyzer
from text_analysis_toolkit.sentiment import SentimentAnalyzer


class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.rg = ReportGenerator("Test Report")
        tokens = ["good", "bad", "good", "great", "terrible", "nice",
                  "good", "happy", "sad", "okay"]
        fa = FrequencyAnalyzer(tokens)
        sa = SentimentAnalyzer()

        self.stats = {
            "total_words": fa.total_words,
            "unique_words": fa.unique_words,
            "sentences": 3,
            "avg_word_length": 4.2,
        }
        self.frequencies = {
            "top_words": fa.top_words(20),
            "unique_words": fa.unique_words,
            "relative": fa.relative_frequencies(),
        }
        self.sentiment = sa.detailed_score(tokens)

    def test_generate_text_contains_sections(self):
        text = self.rg.generate_text(self.stats, self.frequencies, self.sentiment)
        self.assertIn("Test Report", text)
        self.assertIn("Basic Statistics", text)
        self.assertIn("Top 20 Most Frequent Words", text)
        self.assertIn("Sentiment Analysis", text)

    def test_generate_text_stats(self):
        text = self.rg.generate_text(self.stats, self.frequencies, self.sentiment)
        self.assertIn("Total words:", text)
        self.assertIn("Unique words:", text)
        self.assertIn("Sentences:", text)

    def test_generate_json_valid(self):
        output = self.rg.generate_json(self.stats, self.frequencies, self.sentiment)
        parsed = json.loads(output)
        self.assertEqual(parsed["title"], "Test Report")
        self.assertIn("statistics", parsed)
        self.assertIn("frequencies", parsed)
        self.assertIn("sentiment", parsed)

    def test_generate_json_ngrams(self):
        ngrams = {"2": [("good good", 1)]}
        output = self.rg.generate_json(self.stats, self.frequencies, self.sentiment, ngrams)
        parsed = json.loads(output)
        self.assertIn("ngrams", parsed)

    def test_write_report(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            tmp_path = f.name
        try:
            content = "test report content"
            self.rg.write_report(tmp_path, content)
            with open(tmp_path, "r") as f:
                self.assertEqual(f.read(), content)
        finally:
            os.unlink(tmp_path)

    def test_text_with_ngrams(self):
        ngrams = {"2": [("good good", 2), ("bad bad", 1)],
                  "3": [("good good good", 1)]}
        text = self.rg.generate_text(self.stats, self.frequencies, self.sentiment, ngrams)
        self.assertIn("2-grams", text)
        self.assertIn("3-grams", text)


if __name__ == "__main__":
    unittest.main()
