import english_words
import random


def scramble_word(word):
    word = list(word)
    random.shuffle(word)
    return ''.join(word)


def get_random_lower_word():
    return random.choice(list(english_words.english_words_lower_alpha_set))