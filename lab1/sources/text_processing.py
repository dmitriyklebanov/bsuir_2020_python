from string import punctuation


punctuation_translation_table = str.maketrans(punctuation, ' ' * len(punctuation))


def word_counter(text):
    '''Return dict-like object of words and their counts in the text.
    '''

    words = text.translate(punctuation_translation_table).lower().split()
    counter = {}
    for word in words:
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1
    return counter


def most_common_words(text, count=1):
    '''Return string of the most common words in the text.
    '''

    sorted_words_by_count = sorted(word_counter(text).items(), key=lambda x: x[1], reverse=True)
    if not sorted_words_by_count:
        return ''
    top_words = list(zip(*sorted_words_by_count[0:min(count, len(sorted_words_by_count))]))[0]
    return ' '.join(top_words)
