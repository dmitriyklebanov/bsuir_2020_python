from sources.text_processing import word_counter, most_common_words

from collections import Counter


class TestWordCounter:
    def test_empty(self):
        assert word_counter('') == Counter()

    def test_punctuation(self):
        text = 'a,a.a!b???b|||c    '
        counter = Counter({'a': 3, 'b': 2, 'c': 1})
        assert word_counter(text) == counter


class TestMostCommonWords:
    def test_empty(self):
        assert most_common_words('  .|?,, ,') == ''

    def test_simple(self):
        assert most_common_words('a,a?a, b, b, c', 2) == 'a b'

    def test_large_count(self):
        assert most_common_words('a', 1000) == 'a'
