# import necessary packages
from __future__ import unicode_literals
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from hazm import sent_tokenize
from sklearn.neighbors import KDTree
from gensim.models import Word2Vec
from sklearn import preprocessing
from parsivar import FindStems
from parsivar import POSTagger
from itertools import chain
from tqdm.auto import tqdm
import multiprocessing
from time import time
import pandas as pd
import numpy as np
import operator
import logging
import pickle
import json
import os
from Normalizer.Normalizer import Normalizer
from Tokenizer.Tokenizer import Tokenize

class similarity_model_trainer:
    stemmer = FindStems()
    normalizer = Normalizer()
    tagger = POSTagger(tagging_model="wapiti")
    word2vec_input_data = []
    persian_stop_words = None
    hamshahri_corpus = None
    bjkhan_corpus = None
    cwiki_address = None
    tfidf_model = None
    w2v_model = None
    kdt = None
    data_parsed = 0
    queries = []
    query_dict = {}

    def my_normalizer(self, text):
        return self.normalizer.normalizeText(text)

    def my_stem_finder(self, word):
        return self.stemmer.convert_to_stem(word)

    def edit_stop_words(self, persian_stop_words):
        persian_stop_words = [self.my_normalizer(text) for text in persian_stop_words]
        return persian_stop_words

    def load_persian_stop_words(self, address):
        persian_stop_words_raw = open(address, 'r', encoding="utf8").read().split('\n')
        self.persian_stop_words = self.edit_stop_words(persian_stop_words_raw)
        return

    def load_hamshahri_corpus(self, address):
        self.hamshahri_corpus = open(address, 'r', encoding="utf8").read()
        return

    def load_bjkhan_corpus(self, address):
        self.bjkhan_corpus = open(address, 'r', encoding="utf8").read()
        return

    def set_cwiki_address(self, address):
        self.cwiki_address = address
        return
    
    def load_query_list(self, queries):
        self.queries = queries
        return 
    
    def load_queries(self, address):

        l_queries = []
        l_query_dict = {}

        with open(address, encoding='UTF-8') as f:
            data = json.load(f)

        if type(data) == dict:
            l_query_dict = data
        else:
            for d in data:
                l_query_dict.update(d)

        queries_list = list(l_query_dict.items())
        l_queries += [a for (a, b) in queries_list]

        return l_queries, l_query_dict

    def load_train_queries(self, address):

        self.queries, self.query_dict = self.load_queries(address)

        return
    
    def save_kdtree(self, address):
        with open(address, 'wb') as f:
             pickle.dump(self.kdt, f)       
        
    def load_kdtree(self, address):
        with open(address, 'rb') as f:
            self.kdt = pickle.load(f)
            
    def save_tfidf_model(self, address):
        with open(address, 'wb') as f:
             pickle.dump(self.tfidf_model, f)       
        
    def load_tfidf_model(self, address):
        with open(address, 'rb') as f:
            self.tfidf_model = pickle.load(f)
                
    def sent_to_words(self, sentence):
        words = []

        sent_norm = self.my_normalizer(sentence)
        sent_cl = sent_norm.translate(str.maketrans('_،؛/:.,;!·–•—…', '              ',
                                                    '"#$%&\'()*+-<=>?@[\]^`{|}~؛»«ـ'))
        words_raw = Tokenize(stanford_tokenize=True).stanford_tokenize(sent_cl)

        for word in words_raw:
            words += [self.my_stem_finder(word)]

        for del_word in self.persian_stop_words:
            words = list(filter((del_word).__ne__, words))

        return words

    def text_to_word2vec_input(self, texts, print_process):

        n_texts = len(texts)

        word2vec_input = []
        
        if print_process:
            for text_i in tqdm(texts):

                norm_text = self.my_normalizer(text_i)
                sentences = sent_tokenize(norm_text)

                for sentence in sentences:
                    word2vec_input.append(self.sent_to_words(sentence))
        
        else:
            for text_i in texts:

                norm_text = self.my_normalizer(text_i)
                sentences = sent_tokenize(norm_text)

                for sentence in sentences:
                    word2vec_input.append(self.sent_to_words(sentence))

        return word2vec_input

    def bjkhan_to_word2vec_input(self, print_process):
        bj_lines = self.bjkhan_corpus.split('\n')

        bj_texts = []
        temp = ''

        for i in range(2, len(bj_lines) - 1):
            splitted = bj_lines[i].split('    ')
            if splitted[0] != '#':
                if splitted[1] != 'DELM':
                    temp += ' ' + str(splitted[0])
            else:
                if len(temp) > 0:
                    bj_texts.append(temp)
                    temp = ''

        bj_word2vec_input = self.text_to_word2vec_input(bj_texts, print_process)

        return bj_word2vec_input

    def hamshahri_to_word2vec_input(self, print_process):
        hm_raw_texts = self.hamshahri_corpus.split('.DID')
        hm_raw_texts = hm_raw_texts[1:]

        hm_texts = []

        for i, text_i in enumerate(hm_raw_texts):
            temp = text_i.split('.Cat	')
            head, tail = temp[1].split('\n', 1)
            hm_texts.append(tail)

        hm_word2vec_input = self.text_to_word2vec_input(hm_texts, print_process)

        return hm_word2vec_input

    def cwiki_to_word2vec_input(self, print_process):
        level_files = os.listdir(self.cwiki_address)
        cw_texts = []
        for level in level_files:
            l_address = self.cwiki_address + '/' + level
            l_files = os.listdir(l_address)
            for file in l_files:
                file_address = l_address + '/' + file
                f = open(file_address, 'r', encoding='utf8').read()
                cw_texts.append(f)

        cw_word2vec_input = self.text_to_word2vec_input(cw_texts, print_process)

        return cw_word2vec_input

    def load_word2vec_input(self, input_list):
        self.data_parsed = 1
        self.word2vec_input_data = []
        for input_name in input_list:
            with open(input_name, 'rb') as f:
                data = pickle.load(f)
            self.word2vec_input_data = self.word2vec_input_data + data
        
        return

    def load_pos_tags(self, address):
        all_pos = open(address, encoding = 'utf8').read().split('\n')
        all_pos_list = []
        for sent in all_pos:
            temp = []
            for p1 in sent.split('('):
                for p2 in p1.split(')'):
                    if '\'' in p2:
                        p3 = p2.split('\',')
                        word = p3[0][1:]
                        pos = p3[1][2:-1]
                        temp.append((word, pos))
            all_pos_list.append(temp)
        
        return all_pos_list
    
    def train_word2vec_model(self, min_count, window, print_process, update):
        if not self.data_parsed:
            print('Parsing BJ-Khan')
            bj_word2vec_input = self.bjkhan_to_word2vec_input(print_process)
            print('Parsing Hamshahri')
            hm_word2vec_input = self.hamshahri_to_word2vec_input(print_process)
            print('Parsing Cooking Wiki')
            cw_word2vec_input = self.cwiki_to_word2vec_input(print_process)
            self.word2vec_input_data = bj_word2vec_input + hm_word2vec_input + cw_word2vec_input 
            self.data_parsed = 1

        logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt='%H:%M:%S', level=logging.INFO)
        cores = multiprocessing.cpu_count()
        print(cores)
        
        if not update:
            self.w2v_model = Word2Vec(min_count=min_count, window=window, workers=cores - 1)
        
        t = time()
        
        if update:
            self.w2v_model.build_vocab(self.word2vec_input_data, progress_per=10000, update=True)
        else:
            self.w2v_model.build_vocab(self.word2vec_input_data, progress_per=10000)

        print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

        t = time()
        
        if update:
            self.w2v_model.train(self.word2vec_input_data, total_examples=self.w2v_model.corpus_count, 
                                 epochs=self.w2v_model.epochs, report_delay=1)
        else:
            self.w2v_model.train(self.word2vec_input_data, total_examples=self.w2v_model.corpus_count, 
                                 epochs=40, report_delay=1)

        print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

        return self.w2v_model

    def save_word2vec(self, address):
        self.w2v_model.save(address)
        return

    def load_word2vec(self, address):
        self.w2v_model = Word2Vec.load(address)
        return self.w2v_model

    def query_to_vec(self, query, tf_idf):

        q_vec = list(np.zeros((100, 1)).ravel())
        q_vecs = []
        w_tf_idf = []
        words = self.sent_to_words(query)
        n_words = 0
        n_all_words = len(words)
        n_w2v = 0
        
        for word in words:
            if word in self.w2v_model.wv.vocab:   
                n_w2v+=1
                if tf_idf:
                    q_vecs.append(self.w2v_model.wv[word])
                    if word in self.tfidf_model:
                        w_tf_idf.append(self.tfidf_model[word])
                    else: 
                        w_tf_idf.append(1)
                        
                else:
                    q_vec += self.w2v_model.wv[word]
                    n_words += 1

        if tf_idf:
            if len(q_vecs) == 0:
                q_vec_mean = list(np.zeros((100, 1)).ravel())
            else:
                sum_w = sum(w_tf_idf)
                q_mean = np.matmul(np.array([w_tf_idf]), np.array(q_vecs)) / sum_w
                q_vec_mean = q_mean[0]
        else:
            q_vec_mean = [q / (n_words + 1) for q in q_vec]
            
        word_perc = n_w2v / n_all_words * 100
        
        return q_vec_mean

    def build_query_kdt(self, print_progress, tf_idf):

        query_vecs = []

        if print_progress == 1:
            for i, q in enumerate(tqdm(self.queries)):
                query_vecs.append(self.query_to_vec(q, tf_idf))
        else:
            for i, q in enumerate(self.queries):
                query_vecs.append(self.query_to_vec(q, tf_idf))

        X = np.array(query_vecs)
        Xn = preprocessing.normalize(X)
        self.kdt = KDTree(Xn, leaf_size=30, metric='euclidean')

        return

    def find_similar_queries(self, query, k, tf_idf):
        dist_list, idx_list = self.kdt.query(preprocessing.normalize([self.query_to_vec(query, tf_idf)]), k=k,
                                             return_distance=True)
        return dist_list, idx_list

    def print_similar_queries(self, query, k, tf_idf):
        dist_list, idx_list = self.find_similar_queries(query, k, tf_idf)

        for i, idxs in enumerate(idx_list):
            print(']')
            for j, idx in enumerate(idxs):
                print('{"text:"' + self.queries[idx] + "," + ' "distance":' + str(dist_list[i][j]) + '}')
            print('[')

        return

    def similar_queries_list_of_dicts(self, query, k, tf_idf):
        dist_list, idx_list = self.find_similar_queries(query, k, tf_idf)
        similar_queries_list_of_dicts = list()

        for i, idxs in enumerate(idx_list):
            for j, idx in enumerate(idxs):
                dict_similar_queries = dict()
                dict_similar_queries["text"] = self.queries[idx]
                dict_similar_queries["distance"] = dist_list[i][j]
                similar_queries_list_of_dicts.append(dict_similar_queries)

        return similar_queries_list_of_dicts

    def recall_at_k(self, query, query_urls, k, tf_idf):
        dist_list, idx_list = self.find_similar_queries(query, k, tf_idf)
        similar_queries = [self.queries[i] for i in idx_list[0]]
        similar_queries_urls = set(list(chain.from_iterable(([self.query_dict[i] for i in similar_queries]))))

        n_tot = len(query_urls)
        n_sim = 0
        for url in query_urls:
            if url in similar_queries_urls:
                n_sim += 1

        recall_at_k = n_sim / n_tot * 100

        return recall_at_k 
    
    def my_pos_tagger(self, sent):
        sent_words = self.sent_to_words(sent)
        query_pos = self.tagger.parse(sent_words)
        return query_pos
    
    def save_pos_queries(self, queries, address, print_process):
        f = open(address, 'w', encoding='utf8')
        f.close()
        
        if print_process:
            for query in tqdm(queries):
                f = open(address, 'a', encoding='utf8')
                if type(query) != str:
                    que = str(query)
                if not pd.isna(query) :
                    query_pos = self.my_pos_tagger(query)
                    f.write(str(query_pos))
                f.write('\n')
                f.close()
        else:
            for query in queries:
                f = open(address, 'a', encoding='utf8')
                if type(query) != str:
                    que = str(query)
                if not pd.isna(query) :
                    query_pos = self.my_pos_tagger(query)
                    f.write(str(query_pos))
                f.write('\n')
                f.close()
        return
    
    def word2vec_to_tf_idf_input(self, texts):
        tf_texts = []
        for sent in texts:
            str_sent = ''
            for word in sent:
                str_sent+= ' ' + word
            tf_texts.append(str_sent)
        return tf_texts

    
    def tf_idf_weights_dict(self):
        data = self.word2vec_to_tf_idf_input(self.word2vec_input_data)
        n = len(self.word2vec_input_data)
        cv = CountVectorizer(tokenizer = Tokenize(stanford_tokenize=True).stanford_tokenize)
        data = cv.fit_transform(data)
        tfidf_transformer = TfidfTransformer()
        tfidf_matrix = tfidf_transformer.fit_transform(data)
        tfidf_model = dict(zip(cv.get_feature_names(), tfidf_transformer.idf_))
        return tfidf_model, n
    
    def merge_idf(self, n1, n2, idf1, idf2):
        df1 = np.round(((n1+1) / np.exp(idf1-1)) - 1)
        df2 = np.round(((n2+1) / np.exp(idf2-1)) - 1)
        idf_t = np.log((n1+n2+1)/(df1+df2+1)) + 1
        return idf_t

    def merge_tfidf_dict(self, n1, n2, dict1, dict2):
        dict_t = {k: self.merge_idf(n1, n2, dict1.get(k, np.log(n1+1)+1), dict2.get(k, np.log(n2+1)+1))
                  for k in set(dict1) | set(dict2)}
        return dict_t

    def train_tfidf(self, input_list):
        for i, input_data in enumerate(tqdm(input_list)):
            self.load_word2vec_input([input_data])
            if i == 0:
                dict1, n1 = self.tf_idf_weights_dict()
            else:
                dict2, n2 = self.tf_idf_weights_dict()
                dict1 = self.merge_tfidf_dict(n1, n2, dict1, dict2)
                n1 = n1 + n2
        
        self.tfidf_model = dict1
        return self.tfidf_model
        
    def get_word_tfidf(self, word):
        return self.tfidf_model[word]
    
    def url_similarity_sym(self, url1, url2):
        intersection = list(set(url1) & set(url2))
        union = list(set(url1) | set(url2))
        s = len(intersection) / len(union)
        return s
    
    def url_recall(self, rel, ret):
        intersection = list(set(rel) & set(ret))
        r = len(intersection) / len(rel)
        return r
    
    def similar_queries_by_urls(self, rel, k):
        q_recalls = []

        for query in self.queries:
            ret = self.query_dict[query]
            r = self.url_recall(rel, ret)
            if r > 0:
                q_recalls.append((query, r))
        
        if len(q_recalls) > 0:
            q_recalls.sort(key=operator.itemgetter(1), reverse=1)
        
        if len(q_recalls) >= k:
            q_recalls = q_recalls[0:k]
            
        return q_recallsw