import re
from typing import List, Optional


class Tokenizer:
    DEFAULT_STOPWORDS = frozenset({
        "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "by", "with", "from", "as", "is", "was", "are", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "shall", "can", "need",
        "dare", "ought", "used", "it", "its", "this", "that", "these", "those",
        "i", "you", "he", "she", "we", "they", "me", "him", "her", "us", "them",
        "my", "your", "his", "our", "their", "not", "no", "nor", "so", "if",
        "then", "than", "too", "very", "just", "about", "up", "out", "off",
        "over", "also", "into", "only", "other", "more", "some", "such", "each",
        "every", "own", "same", "both", "here", "there", "when", "where", "why",
        "how", "which", "who", "whom", "what"
    })

    def __init__(self, lower: bool = True, remove_punct: bool = True,
                 remove_stopwords: bool = False, stopwords: Optional[List[str]] = None):
        self.lower = lower
        self.remove_punct = remove_punct
        self.remove_stopwords = remove_stopwords
        self._stopwords = set(stopwords) if stopwords else set(self.DEFAULT_STOPWORDS)

    @property
    def stopwords(self):
        return frozenset(self._stopwords)

    def tokenize(self, text: str) -> List[str]:
        text = text.strip()
        if not text:
            return []

        if self.lower:
            text = text.lower()
        if self.remove_punct:
            text = re.sub(r"[^\w\s]", "", text)

        tokens = text.split()
        tokens = [t for t in tokens if t]

        if self.remove_stopwords:
            tokens = [t for t in tokens if t not in self._stopwords]

        return tokens

    def sentence_split(self, text: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        if n < 1 or len(tokens) < n:
            return []
        return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
