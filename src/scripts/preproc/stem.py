from nltk.stem import SnowballStemmer
from nltk.stem import RSLPStemmer


def stem(word):
    stemmer = RSLPStemmer()
    # stemmer = SnowballStemmer('portuguese')

    return stemmer.stem(word)
