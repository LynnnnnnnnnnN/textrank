from gensim.models import word2vec
import logging
 
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
sentences = word2vec.LineSentence(u'./cut_zh_wiki_00.txt')
model = word2vec.Word2Vec(sentences, size=200, window=10, min_count=64, sg=1, hs=1, iter=10, workers=25)
model.save(u'./word2vec2')