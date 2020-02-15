from ..text_processing import word_counter, most_common_words

from collections import Counter

import unittest


class TestWordCounter(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(word_counter(''), Counter())

    def test_punctuation(self):
        text = 'a,a.a!b???b|||c    '
        counter = Counter({'a': 3, 'b': 2, 'c': 1})
        self.assertEqual(word_counter(text), counter)


class TestMostCommonWords(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(most_common_words('  .|?,, ,'), '')

    def test_simple(self):
        self.assertEqual(most_common_words('a,a?a, b, b, c', 2), 'a b')

    def test_large_count(self):
        self.assertEqual(most_common_words('a', 1000), 'a')
