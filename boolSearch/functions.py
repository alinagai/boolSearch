import nltk
import pymorphy2
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
russian_stopwords = stopwords.words('russian')
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
morph = pymorphy2.MorphAnalyzer()


def stopwords(tokenized_text) :
    return [
        word.lower() for word in tokenized_text
        if word not in russian_stopwords
        and word not in punctuation
    ]


def lemma(text):
    words = []
    for word in text:
        parsed = morph.parse(word)[0]
        if parsed.tag.POS in ['NOUN', 'ADJF', 'ADJS', 'PRTF', 'PRTS']:
            words += [parsed.normal_form]
    return words


def get_tokens_list(f_count):
    tokens = {}
    for i in range(1, f_count):
        with open(f'files/{i}.txt', 'r') as d:
            d_text = d.read()
            tokenized_text = word_tokenize(d_text, language="russian")  # делаем токенизацию
            w_wtht_stopwords = stopwords(tokenized_text)
            tokens[i] = lemma(w_wtht_stopwords)
    return tokens