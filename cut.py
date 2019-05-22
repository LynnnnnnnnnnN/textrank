# encoding = utf-8
import jieba
import codecs
import re
f = codecs.open('D:\Study\download\TextRank4ZH-master\doc\extracted\AA\zh_wiki_00.txt', "a+",encoding='utf-8')
for line in open("D:\Study\download\TextRank4ZH-master\doc\extracted\AA\zh_wiki_00.txt",encoding='utf-8'):
    for i in re.sub('[a-zA-Z0-9]', '', line).split(' '):
        if i != '':
            data = list(jieba.cut(i, cut_all = False))
            readline = ' '.join(data) + '\n'
            f.write(readline)
f.close()