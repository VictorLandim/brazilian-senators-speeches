import re
import string
import unicodedata


def remove_white(str):
    """
    Remove multiple whitespaces from str.
    """
    return " ".join(str.split())


def clean(word, remove_alpha_numeric=True, remove_accents=True):
    punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

    word = word.lower()

    if remove_accents:
        word = unicodedata.normalize(
            'NFKD', word).encode('ISO-8859-1', 'ignore')
        word = word.decode('ISO-8859-1')
    if remove_alpha_numeric:
        word = re.sub(r'[^a-z ]', r'', word)
    else:
        # do not remove alpha-numeric characteres, but remove punctuation from punctuation table
        word = word.translate(punctuation_table)

    # remove white space
    word = re.sub(r'\s+', r'', word)

    return word
