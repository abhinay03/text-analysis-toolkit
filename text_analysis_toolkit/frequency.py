from typing import Dict, List, Tuple
from collections import Counter


class FrequencyAnalyzer:
    def __init__(self, tokens: List[str]):
        if not isinstance(tokens, list):
            raise TypeError("tokens must be a list of strings")
        self._tokens = list(tokens)
        self._counter = Counter(self._tokens)

    @property
    def tokens(self) -> List[str]:
        return list(self._tokens)

    @property
    def unique_words(self) -> int:
        return len(self._counter)

    @property
    def total_words(self) -> int:
        return len(self._tokens)

    def word_counts(self) -> Dict[str, int]:
        return dict(self._counter)

    def top_words(self, n: int = 10) -> List[Tuple[str, int]]:
        return self._counter.most_common(n)

    def term_frequency(self, word: str) -> float:
        if self.total_words == 0:
            return 0.0
        return self._counter.get(word, 0) / self.total_words

    def relative_frequencies(self) -> Dict[str, float]:
        if self.total_words == 0:
            return {}
        return {word: count / self.total_words for word, count in self._counter.items()}

    def words_above_threshold(self, threshold: int = 1) -> List[Tuple[str, int]]:
        return [(w, c) for w, c in self._counter.items() if c > threshold]

    def __len__(self) -> int:
        return self.total_words

    def __repr__(self) -> str:
        return f"FrequencyAnalyzer({self.total_words} tokens, {self.unique_words} unique)"
