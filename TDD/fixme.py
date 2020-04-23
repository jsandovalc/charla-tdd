from collections import defaultdict


class WordCount:
    def __init__(self):
        self._count = defaultdict(int)

    def add(self, word: str):
        self._count[word.lower()] += 1

    def count(self, word: str) -> int:
        return self._count[word]
