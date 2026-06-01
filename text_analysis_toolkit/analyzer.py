from typing import Dict, List, Optional, Tuple
from text_analysis_toolkit.tokenizer import Tokenizer
from text_analysis_toolkit.frequency import FrequencyAnalyzer
from text_analysis_toolkit.sentiment import SentimentAnalyzer
from text_analysis_toolkit.reporter import ReportGenerator
from pathlib import Path


class TextAnalyzer:
    def __init__(self, remove_stopwords: bool = False,
                 custom_stopwords: Optional[List[str]] = None,
                 ngram_range: Tuple[int, int] = (2, 3),
                 report_title: str = "Text Analysis Report"):
        self.tokenizer = Tokenizer(
            lower=True, remove_punct=True,
            remove_stopwords=remove_stopwords,
            stopwords=custom_stopwords
        )
        self.sentiment = SentimentAnalyzer()
        self.reporter = ReportGenerator(title=report_title)
        self.ngram_range = ngram_range

    def analyze(self, text: str) -> Dict:
        tokens = self.tokenizer.tokenize(text)
        sentences = self.tokenizer.sentence_split(text)
        fa = FrequencyAnalyzer(tokens)

        avg_word_length = sum(len(w) for w in tokens) / len(tokens) if tokens else 0.0

        stats = {
            "total_words": fa.total_words,
            "unique_words": fa.unique_words,
            "sentences": len(sentences),
            "avg_word_length": round(avg_word_length, 2),
        }

        freq_result = {
            "top_words": fa.top_words(20),
            "unique_words": fa.unique_words,
            "relative": fa.relative_frequencies(),
        }

        sentiment_result = self.sentiment.detailed_score(tokens)

        ngrams = {}
        for n in range(self.ngram_range[0], self.ngram_range[1] + 1):
            ng_list = self.tokenizer.ngrams(tokens, n)
            if ng_list:
                from collections import Counter
                ngram_counts = Counter(ng_list).most_common(20)
                ngrams[f"{n}"] = [(g, c) for g, c in ngram_counts]

        result = {
            "statistics": stats,
            "frequencies": freq_result,
            "sentiment": sentiment_result,
            "ngrams": ngrams,
            "tokens": tokens,
        }
        return result

    def analyze_file(self, filepath: str, encoding: str = "utf-8") -> Dict:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        text = path.read_text(encoding=encoding)
        return self.analyze(text)

    def report_text(self, result: Dict) -> str:
        return self.reporter.generate_text(
            stats=result["statistics"],
            frequencies=result["frequencies"],
            sentiment=result["sentiment"],
            ngrams=result["ngrams"],
        )

    def report_json(self, result: Dict) -> str:
        return self.reporter.generate_json(
            stats=result["statistics"],
            frequencies=result["frequencies"],
            sentiment=result["sentiment"],
            ngrams=result["ngrams"],
        )
