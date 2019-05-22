#!/usr/bin/env python
# -*- coding:utf-8 -*-
from gensim.models import word2vec
 
model = word2vec.Word2Vec.load("word2vec2")
 
s = model.similarity(u'武汉', u'上海')
print("'武汉'与'上海'的相似度为:",s)
 
s = model.similarity(u'武汉', u'北京')
print("'武汉'与'北京'的相似度为:",s)
print
 
print("与'武汉'最相近的词语:")
result = model.most_similar(u'武汉')
for each in result:
    print(each[0], each[1])
print
 
print("与'信息'最相近的词语:")
result = model.most_similar(u'信息')
for each in result:
    print(each[0], each[1])
print
 
print("与'大学'最相近的词语:")
result = model.most_similar(u'大学')
for each in result:
    print(each[0], each[1])