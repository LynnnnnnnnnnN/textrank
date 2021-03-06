# -*- coding: utf-8 -*-

import jieba  
import math  
from string import punctuation  
from heapq import nlargest  
from itertools import product, count  
from gensim.models import word2vec  
import numpy as np  

model = word2vec.Word2Vec.load("word2vec2")  
np.seterr(all='warn')  

def cut_sentences(sentence):
    puns = frozenset(u'.')
    tmp = []
    for ch in sentence:
        tmp.append(ch)
        if puns.__contains__(ch):
            yield ''.join(tmp)
            tmp = []
    yield ''.join(tmp)

# 句子中的stopwords  
def create_stopwords():  
    stop_list = [line.strip() for line in open("tingyongci.txt", 'r', encoding='utf-8').readlines()]  
    return stop_list

#计算两个句子的相似性
def two_sentences_similarity(sents_1, sents_2):
    counter = 0
    for sent in sents_1:
        if sent in sents_2:
            counter += 1
    return counter / (math.log(len(sents_1) + len(sents_2)))

#传入句子链表  返回句子之间相似度的图 
def create_graph(word_sent):  
    num = len(word_sent)  
    board = [[0.0 for _ in range(num)] for _ in range(num)]  

    for i, j in product(range(num), repeat=2):  
        if i != j:  
            board[i][j] = compute_similarity_by_avg(word_sent[i], word_sent[j])  
    return board 

#计算两个向量之间的余弦相似度
def cosine_similarity(vec1, vec2):
    tx = np.array(vec1)
    ty = np.array(vec2)
    cos1 = np.sum(tx * ty)
    cos21 = np.sqrt(sum(tx ** 2))
    cos22 = np.sqrt(sum(ty ** 2))
    cosine_value = cos1 / float(cos21 * cos22)
    return cosine_value

#对两个句子求平均词向量
def compute_similarity_by_avg(sents_1, sents_2):
    if len(sents_1) == 0 or len(sents_2) == 0:
        return 0.0
    vec1 = model[sents_1[0]]
    for word1 in sents_1[1:]:
        vec1 = vec1 + model[word1]
    vec2 = model[sents_2[0]]
    for word2 in sents_2[1:]:
        vec2 = vec2 + model[word2]
    similarity = cosine_similarity(vec1 / len(sents_1), vec2 / len(sents_2))
    return similarity

#计算句子在图中的分数，句子权重计算
def calculate_score(weight_graph, scores, i):
    length = len(weight_graph)
    d = 0.85
    added_score = 0.0
    for j in range(length):
        denominator = 0.0
        fraction = weight_graph[j][i] * scores[j]
        for k in range(length):
            denominator += weight_graph[j][k]
            if denominator == 0:
                denominator = 1
        added_score += fraction / denominator
    weighted_score = (1 - d) + d * added_score
    return weighted_score

#输入相似度的图（矩阵) ，返回各个句子的分数，句子排序
def weight_sentences_rank(weight_graph):
    scores = [0.5 for _ in range(len(weight_graph))]
    old_scores = [0.0 for _ in range(len(weight_graph))]
    while different(scores, old_scores):
        for i in range(len(weight_graph)):
            old_scores[i] = scores[i]
        for i in range(len(weight_graph)):
            scores[i] = calculate_score(weight_graph, scores, i)
    return scores

#判断前后分数有无变化
def different(scores, old_scores):  
    flag = False  
    for i in range(len(scores)):  
        if math.fabs(scores[i] - old_scores[i]) >= 0.0001:  
            flag = True  
            break  
    return flag 

def filter_symbols(sents):  
    stopwords = create_stopwords() + ['。', ' ', '.']  
    _sents = []  
    for sentence in sents:  
        for word in sentence:  
            if word in stopwords:  
                sentence.remove(word)  
        if sentence:  
            _sents.append(sentence)  
    return _sents  


def filter_model(sents):  
    _sents = []  
    for sentence in sents:  
        for word in sentence:  
            if word not in model:  
                sentence.remove(word)  
        if sentence:  
            _sents.append(sentence)  
    return _sents  

#文摘生成
def summarize(text,n):
    tokens = cut_sentences(text)
    sentences = []
    sents = []
    for sent in tokens:
        sentences.append(sent)
        sents.append([word for word in jieba.cut(sent) if word])
    #sents = filter_model(sents)
    print(len(sents))
    filter_model(sents)
    print(len(sents[0]))
    filter_model(sents)
    print(len(sents[0]))
    graph = create_graph(sents)
    scores = weight_sentences_rank(graph)
    sent_selected = nlargest(n,zip(scores,count()))
    sent_index = []
    for i in range(n):
        sent_index.append(sent_selected[i][1])
    return [sentences[i] for i in sent_index]

#主函数
if __name__ == '__main__':
    with open("test5.txt", "r",encoding=('utf-8')) as test:
        txt = [line.strip() for line in open("test5.txt", "r",encoding=('utf-8')).readlines()]
        text = test.read().replace('\n', '')
        print('原文为：')
    for i in txt:
        print (i)
    summarize_text = summarize(text,5)
    print('摘要为：')
    for i in summarize_text:
        print()


