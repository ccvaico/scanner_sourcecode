#!/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import defaultdict
import re

from similarity import similarity
from k_means import KMeans
from auto_cluster import find_optimum_k,kmeans
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf(corpus):
    vectorizer = TfidfVectorizer()
    data_vec = vectorizer.fit_transform(corpus)
    import pandas as pd
    df = pd.DataFrame(data_vec.toarray())
    df.columns = vectorizer.get_feature_names()
    return df

def word_frequencies(word_vector):
    """What percent of the time does each word in the vector appear?

    Returns a dictionary mapping each word to its frequency.

    """
    num_words = len(word_vector)
    # print "num_words:",num_words
    frequencies = defaultdict(float)
    for word in word_vector:
        frequencies[word] += 1.0 / num_words

    return dict(frequencies)


def compare_vectors(word_vector1, word_vector2):
    """Numerical similarity between lists of words. Higher is better.

    Uses cosine similarity.
    Result range: 0 (bad) - 1 (uses all the same words in the same proportions)

    """
    all_words = list(set(word_vector1).union(set(word_vector2)))
    frequency_dict1 = word_frequencies(word_vector1)
    frequency_dict2 = word_frequencies(word_vector2)

    frequency_vector1 = [frequency_dict1.get(word, 0) for word in all_words]
    frequency_vector2 = [frequency_dict2.get(word, 0) for word in all_words]

    return similarity(frequency_vector1, frequency_vector2)


def vectorize_text(text):   #返回split之后的文本单词的list，每一条漏洞返回一个list
    """Takes in text, processes it, and vectorizes it."""

    def remove_punctuation(text):
        """Removes special characters from text."""
        return re.sub('[,.:?";\-=!@#$%^&*(){}]', ' ', text)

    def remove_common_words(text_vector):
        """Removes 50 most common words in the uk english.

        source: http://www.bckelk.ukfsn.org/words/uk1000n.html

        """
        common_words = set(['the', 'and', 'to', 'of', 'a', 'I', 'in',
            'was', 'he', 'that', 'it', 'his', 'her', 'you', 'as',
            'had', 'with', 'for', 'she', 'not', 'at', 'but', 'be',
            'my', 'on', 'have', 'him', 'is', 'said', 'me', 'which',
            'by', 'so', 'this', 'all', 'from', 'they', 'no', 'were',
            'if', 'would', 'or', 'when', 'what', 'there', 'been',
            'one', 'could', 'very', 'an', 'who'])
        return [word for word in text_vector if word not in common_words]

    text = text.lower()  #转换所有字符为小写
    text = remove_punctuation(text)   #去除标点符号
    # print "text:",text
    # print 'text type:',type(text)   #string
    words_list = text.split()
    words_list = remove_common_words(words_list)
    # print "word_list:",words_list
    return words_list

def compare_texts(text1, text2):
    """How similar are the two input paragraphs?"""
    return compare_vectors(vectorize_text(text1), vectorize_text(text2))

################################

def make_word_lists(paragraphs):
    return map(vectorize_text, paragraphs)

def make_word_set(word_lists):
    """ """
    return set(word for words in word_lists for word in words)

def make_word_vectors(word_set, word_lists):

    def vectorize(frequency_dict):
        return [frequency_dict.get(word, 0) for word in word_set]
    frequencies = map(word_frequencies, word_lists)   #返回单词与词频的字典，后经过循环形成一个字典的列表
    # print "frequencies:",frequencies
    # print "frequencies_type:",type(frequencies)
    # print "frequencies_length:",len(frequencies)
    return map(vectorize, frequencies)

def translator(clusters, paragraph_map):
    """Translate vectors back into paragraphs, to make them human-readable."""
    def item_translator(vector):
        return paragraph_map.get(str(vector))

    def cluster_translator(cluster):
        return map(item_translator, cluster)

    return map(cluster_translator, clusters)

# def cluster_paragraphs(paragraphs, num_clusters=2):
#     word_lists = make_word_lists(paragraphs)
#     word_set = make_word_set(word_lists)
#     word_vectors = make_word_vectors(word_set, word_lists)
#
#     paragraph_map = dict(zip(map(str, word_vectors), paragraphs))
#
#     k_means = KMeans(num_clusters, word_vectors)
#     k_means.main_loop()
#     return translator(k_means.clusters, paragraph_map)


def cluster_paragraphs(paragraphs):
    word_lists = make_word_lists(paragraphs) #二维列表
    word_lists1 = []
    for i in range(len(word_lists)):
        str1=" ".join(word_lists[i])
        word_lists1.append(str1)
    # print "word_lists1:",word_lists1
    word_set = make_word_set(word_lists)   #所有词的集合
    vec_df = tfidf(word_lists1)
    word_vectors = make_word_vectors(word_set, word_lists)  #将每一条数据处理成一个固定长度的向量
    # print "word_vectors:",word_vectors

    paragraph_map = dict(zip(map(str, word_vectors), paragraphs))

    optimum_k = find_optimum_k(vec_df)
    k_means = KMeans(optimum_k, word_vectors)
    k_means.main_loop()
    return translator(k_means.clusters, paragraph_map)


# word_lists = make_word_lists(list)
# print "success!"
# print word_lists


# the `vectorize_text` function is not actually vectorizing, it's just
# splitting/stripping.  The vectorization happens in the `compare_texts`
# function, where the word-lists are replaced by the frequency of their
# occurence. I should rename functions to rectify.
