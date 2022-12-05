import json
import nltk
from nltk.util import ngrams
import operator


# Функция поиска ngram
def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


def extract_ngrams(data, num):
    words = nltk.word_tokenize(data, language='russian')
    words = [word.lower() for word in words if word.isalpha()]
    n_grams = ngrams(words, num)
    return [' '.join(grams) for grams in n_grams]


dgram_stats = {}
# Чтение постов из дампа json
with open('vk_dump.json', encoding='utf8') as f:
    posts = json.load(f)
for post in posts:
    for ngram in extract_ngrams(post['text'], 2):
        dgram_stats[ngram] = dgram_stats.get(ngram, 0) + 1

stats_list = sorted(dgram_stats.items(), key=operator.itemgetter(1))
for ngram, count in stats_list:
    print("%-32s %d" % (ngram, count))
