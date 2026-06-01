import json
from typing import Dict, List, Optional, TextIO


class ReportGenerator:
    def __init__(self, title: str = "Text Analysis Report"):
        self.title = title

    def generate_text(self, stats: Dict, frequencies: Dict,
                      sentiment: Dict, ngrams: Optional[Dict] = None) -> str:
        lines = []
        sep = "=" * 60
        lines.append(sep)
        lines.append(f"  {self.title}")
        lines.append(sep)
        lines.append("")

        lines.append("--- Basic Statistics ---")
        lines.append(f"  Total words:      {stats.get('total_words', 0)}")
        lines.append(f"  Unique words:     {stats.get('unique_words', 0)}")
        lines.append(f"  Sentences:        {stats.get('sentences', 0)}")
        lines.append(f"  Avg word length:  {stats.get('avg_word_length', 0):.2f}")
        lines.append("")

        lines.append("--- Top 20 Most Frequent Words ---")
        lines.append(f"  {'Word':<20} {'Count':<8} {'Frequency':<10}")
        lines.append(f"  {'-'*20} {'-'*8} {'-'*10}")
        for word, count in frequencies.get("top_words", []):
            pct = frequencies.get("relative", {}).get(word, 0) * 100
            lines.append(f"  {word:<20} {count:<8} {pct:>6.2f}%")
        lines.append("")

        if ngrams:
            for n, items in ngrams.items():
                lines.append(f"--- Top 10 {n}-grams ---")
                lines.append(f"  {'Ngram':<30} {'Count':<8}")
                lines.append(f"  {'-'*30} {'-'*8}")
                for ng, c in items[:10]:
                    lines.append(f"  {ng:<30} {c:<8}")
                lines.append("")

        lines.append("--- Sentiment Analysis ---")
        lines.append(f"  Score:           {sentiment.get('sentiment_score', 0):+.3f}")
        lines.append(f"  Label:           {sentiment.get('sentiment_label', 'unknown')}")
        lines.append(f"  Positive words:  {sentiment.get('positive_count', 0)}")
        lines.append(f"  Negative words:  {sentiment.get('negative_count', 0)}")
        lines.append(f"  Positive ratio:  {sentiment.get('positive_ratio', 0):.2%}")
        lines.append(f"  Negative ratio:  {sentiment.get('negative_ratio', 0):.2%}")
        lines.append("")
        lines.append(sep)

        return "\n".join(lines)

    def generate_json(self, stats: Dict, frequencies: Dict,
                      sentiment: Dict, ngrams: Optional[Dict] = None) -> str:
        report = {
            "title": self.title,
            "statistics": stats,
            "frequencies": frequencies,
            "sentiment": sentiment,
        }
        if ngrams:
            report["ngrams"] = ngrams
        return json.dumps(report, indent=2, ensure_ascii=False)

    def write_report(self, output_path: str, content: str):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
