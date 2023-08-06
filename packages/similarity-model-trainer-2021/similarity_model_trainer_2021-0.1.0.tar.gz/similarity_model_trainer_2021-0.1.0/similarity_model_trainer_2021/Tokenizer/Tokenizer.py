import stanza
from symspellpy.symspellpy import SymSpell
import pickle
import re
import pathlib
import os
# ‫استفاده از یکسان‌سازی که خودمان توسعه دادیم
from ..Normalizer.Normalizer import Normalizer

with open('{}/'.format(pathlib.Path(__file__).parent.absolute()) + 'LM/dic_uni.pickle', 'rb') as f_uni:
    unigram = pickle.load(f_uni)

with open('{}/'.format(pathlib.Path(__file__).parent.absolute()) + 'LM/dic_bi.pickle', 'rb') as f_bi:
    bigram = pickle.load(f_bi)


# ‫این کلاس  شامل دو مدل واحدساز است یکی استفاده از واحدساز stanford  و ngram tokenizer
class Tokenize(object):

    def __init__(self, word_breaker=False, stanford_tokenize=False, component_words=False):
        if word_breaker:
            self.sym_spell = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
            self.dictionary_path = '{}/'.format(pathlib.Path(__file__).parent.absolute()) + \
                                   "frequency_bigramdictionary2_fa_243_342.txt"
            self.sym_spell.load_dictionary(self.dictionary_path, term_index=0, count_index=2)
        if stanford_tokenize:
            if not os.path.exists('/home/dev/stanza_resources/fa'):
                print('downloading pipline ...')
                stanza.download('fa')
            self.nlp = stanza.Pipeline(lang='fa', processors='tokenize,mwt')
        self.tokens = []
        self.my_normalizer = Normalizer()
        self.uni_prop = {}
        self.bi_prop = {}

        # it takes a long time
        if component_words:
            for key, value in unigram.items():
                self.uni_prop[key] = value / sum(unigram.values())

            for key, value in bigram.items():
                condition = key.split()[0]
                self.bi_prop[key] = (value / unigram[condition]) * self.uni_prop[condition]

    # ‫این تابع برای استفاده از واحدساز stanfordnlp است
    def stanford_tokenize(self, text):

        normalized_text = self.my_normalizer.normalizeText(text)
        doc = self.nlp(normalized_text)
        for sent in doc.sentences:
            for word in sent.words:
                self.tokens.append(word.text)
        return self.tokens

    def space_tokenize(self, text):
        normalized_text = self.my_normalizer.normalizeText(text)
        self.tokens = normalized_text.split(" ")
        return self.tokens

    # ‫این تابع برای ngram tokenizer است که n را به صورت ورودی دریافت می‌کند
    def ngramTokenize(self, text, n):
        normalized_text = self.my_normalizer.normalizeText(text)
        words = normalized_text.split()
        ngrams = zip(*[words[i:] for i in range(n)])
        self.tokens = [" ".join(ngram) for ngram in ngrams]
        return self.tokens

    def word_segmentation(self, text):
        result = self.sym_spell.word_segmentation(text)
        return self.space_tokenize(result.corrected_string)

    @staticmethod
    def ngram(text, n):
        words = text.split()
        ngrams = zip(*[words[i:] for i in range(n)])
        tokens = [" ".join(ngram) for ngram in ngrams]
        return tokens

    @staticmethod
    def perplexity(prob, n):
        perplexity = pow(1 / prob, 1 / n)
        return perplexity

    # ‫استفاده از مدلهای زبانی برای تشخیص قراردادن نیم فاصله
    def component_words(self, text):
        unigram_sample = self.ngram(text, 1)
        bigram_sample = self.ngram(text, 2)

        lst_sample_uni = [self.uni_prop[word] for word in unigram_sample if word in self.uni_prop.keys()]
        lst_sample_bi = [self.bi_prop[bi] for bi in bigram_sample if bi in self.bi_prop.keys()]

        dic_uni_per = {}
        dic_bi_per = {}

        for i, word in enumerate(unigram_sample):
            try:
                dic_uni_per[word] = self.perplexity(lst_sample_uni[i], 1)
            except:
                continue

        for i, bi in enumerate(bigram_sample):
            try:
                dic_bi_per[bi] = self.perplexity(lst_sample_bi[i], 2)
            except:
                continue

        token = []
        num_of_append = 0
        if len(unigram_sample) >= 2:
            for i in range(len(unigram_sample)):
                word1 = unigram_sample[i]
                try:
                    word2 = unigram_sample[i + 1]
                except:
                    if num_of_append == len(unigram_sample) + 1:
                        break
                    else:
                        token.append(word1)
                        break
                bi = " ".join([word1, word2])
                if bi in dic_bi_per.keys() and dic_bi_per[bi] < dic_uni_per[word1] and dic_bi_per[bi] < dic_uni_per[
                    word2]:
                    bi = "‌".join([word1, word2])
                    token.append(bi)
                    num_of_append = num_of_append + 2
                else:
                    token.append(word1)
                    num_of_append = num_of_append + 1
        else:
            token = unigram_sample
        s = " ".join(token)
        s = re.sub(r'\b(\w+)( \1\b)+', r'\1', s)
        return self.space_tokenize(s)
