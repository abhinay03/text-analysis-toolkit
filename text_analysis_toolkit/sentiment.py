from typing import Dict, List, Optional, Set, Tuple
from pathlib import Path


class SentimentAnalyzer:
    def __init__(self, positive_words: Optional[Set[str]] = None,
                 negative_words: Optional[Set[str]] = None):
        self._positive = set(positive_words) if positive_words else self._default_positive()
        self._negative = set(negative_words) if negative_words else self._default_negative()

    @staticmethod
    def _default_positive() -> Set[str]:
        return {
            "good", "great", "excellent", "amazing", "wonderful", "fantastic",
            "beautiful", "love", "happy", "joy", "delight", "perfect",
            "brilliant", "awesome", "superb", "outstanding", "positive",
            "best", "favourite", "fun", "enjoy", "pleasure", "glad",
            "grateful", "thankful", "marvelous", "splendid", "magnificent",
            "tremendous", "remarkable", "pleasant", "cheerful", "optimistic",
            "hopeful", "success", "triumph", "victory", "benefit", "better",
            "nice", "kind", "generous", "caring", "helpful", "lovely",
            "wonderful", "impressive", "incredible", "fabulous", "terrific"
        }

    @staticmethod
    def _default_negative() -> Set[str]:
        return {
            "bad", "terrible", "awful", "horrible", "poor", "hate", "ugly",
            "sad", "angry", "furious", "disgusting", "dreadful", "worst",
            "mediocre", "boring", "annoying", "frustrating", "disappointing",
            "pathetic", "inferior", "negative", "failure", "useless",
            "horrendous", "atrocious", "abysmal", "gross", "nasty", "cruel",
            "evil", "wicked", "painful", "suffering", "tragic", "gloomy",
            "depressing", "hopeless", "dismal", "disaster", "catastrophe",
            "damage", "harmful", "toxic", "vile", "hideous", "lousy",
            "rotten", "shameful", "unpleasant", "miserable", "unhappy"
        }

    @property
    def positive_words(self) -> frozenset:
        return frozenset(self._positive)

    @property
    def negative_words(self) -> frozenset:
        return frozenset(self._negative)

    def score(self, tokens: List[str]) -> float:
        if not tokens:
            return 0.0
        pos_count = sum(1 for t in tokens if t in self._positive)
        neg_count = sum(1 for t in tokens if t in self._negative)
        total = pos_count + neg_count
        if total == 0:
            return 0.0
        return (pos_count - neg_count) / total

    def detailed_score(self, tokens: List[str]) -> Dict[str, float]:
        pos_count = sum(1 for t in tokens if t in self._positive)
        neg_count = sum(1 for t in tokens if t in self._negative)
        total = len(tokens)
        return {
            "positive_count": pos_count,
            "negative_count": neg_count,
            "positive_ratio": pos_count / total if total else 0.0,
            "negative_ratio": neg_count / total if total else 0.0,
            "sentiment_score": self.score(tokens),
            "sentiment_label": self._label(self.score(tokens)),
        }

    def positive_matches(self, tokens: List[str]) -> List[str]:
        return [t for t in tokens if t in self._positive]

    def negative_matches(self, tokens: List[str]) -> List[str]:
        return [t for t in tokens if t in self._negative]

    @staticmethod
    def _label(score: float) -> str:
        if score > 0.3:
            return "positive"
        if score < -0.3:
            return "negative"
        return "neutral"

    def load_custom_lexicon(self, filepath: str, sentiment: str):
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Lexicon file not found: {filepath}")
        words = {line.strip().lower() for line in path.read_text(encoding="utf-8").splitlines()
                 if line.strip() and not line.startswith("#")}
        if sentiment == "positive":
            self._positive.update(words)
        elif sentiment == "negative":
            self._negative.update(words)
        else:
            raise ValueError("sentiment must be 'positive' or 'negative'")
