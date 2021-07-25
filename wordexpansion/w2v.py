from gensim.models import word2vec
import jieba
from pathlib import Path
from nltk.tokenize import word_tokenize
import multiprocessing
from multistop import Stopwords

class W2VModels(object):
    def __init__(self, cwd, lang='english'):
        """
        模型初始化设置
        :param cwd:  当前工作路径
        :param lang:  数据的语言
        """
        self.cwd = cwd
        self.lang = lang


    def __preproces(self, documents):
        """
        对数据进行预处理,分词、去除停用词；   可以加单词同类型合并的
        :param documents:  文档列表
        :return:  清洗后的文档列表
        """


        docs = []
        if self.lang=='english':
            sw = Stopwords()
            sw.setlang(lang=self.lang)
            stopwords = sw.stopwords()
            for document in documents:
                document = document.lower()
                document = [w for w in word_tokenize(document) if w not in stopwords]
                docs.append(document)
            return docs
        elif self.lang=='chinese':
            sw = Stopwords()
            sw.setlang(lang=self.lang)
            stopwords = sw.stopwords()
            for document in documents:
                words = jieba.lcut(document)
                document = [w for w in words if w not in stopwords]
                docs.append(document)
            return docs
        else:
            assert 'Do not support {} language'.format(self.lang)



    def train(self, documents, min_count=1):
        """
        训练语料库的word2vec模型
        :param documents:  传入的文档列表
        :param min_count: 模型中词语最少在语料中出现min_count次
        :return:
        """
        print('数据预处理开始.......')
        sentences = self.__preproces(documents=documents)
        print('预处理结束...........')
        print('Word2Vec模型训练开始......')
        self.model = word2vec.Word2Vec(sentences, min_count=min_count, workers=multiprocessing.cpu_count())
        modeldir = Path(self.cwd).joinpath('model')
        Path(self.cwd).joinpath('model').mkdir(exist_ok=True)
        modelpath = str(Path(modeldir).joinpath('your.model'))
        self.model.save(modelpath)
        print('已将模型存入 {} '.format(str(modelpath)))



    def __search(self, seedwords, n=50):

        self.similars_candidate_idxs = [] #seedwords的候选词
        dictionary = self.model.wv.key_to_index
        print(dictionary)
        self.seedidxs = [] #把word 转化为 index
        for seed in seedwords:
            if seed in dictionary:
                seedidx = dictionary[seed]
                self.seedidxs.append(seedidx)
        print(self.seedidxs)
        for seedidx in self.seedidxs:
            # sims_words形如[('by', 0.99984), ('or', 0.99982), ('an', 0.99981), ('up', 0.99980)]
            sims_words = self.model.wv.similar_by_word(seedidx, topn=n)
            #将词语转为index存储起来
            self.similars_candidate_idxs.extend([dictionary[sim[0]] for sim in sims_words])
        self.similars_candidate_idxs = set(self.similars_candidate_idxs)




    def find(self, seedwords, seedwordsname, topn):
        simidx_scores = []
        print('准备寻找每个seed在语料中所有的相似候选词')
        self.__search(seedwords)
        print('初步搜寻到 {} 个相似的候选词'.format(len(self.similars_candidate_idxs)))

        print('计算每个候选词 与 {seedwordsname} 的相似度， 选出相似度最高的前 {topn} 个候选词'.format(seedwordsname=seedwordsname, topn=topn))
        for idx in self.similars_candidate_idxs:
            score = self.model.wv.n_similarity([idx], self.seedidxs)
            simidx_scores.append((idx, score))
        simidxs = [w[0] for w in sorted(simidx_scores, key=lambda k:k[1], reverse=True)]

        simwords = [str(self.model.wv.index_to_key[idx]) for idx in simidxs][:topn]

        resultwords = []
        resultwords.extend(seedwords)
        resultwords.extend(simwords)

        txtdir = Path(self.cwd).joinpath('candidate_words')
        Path(self.cwd).joinpath('candidate_words').mkdir(exist_ok=True)
        candidatetxtfile = Path(txtdir).joinpath('{}.txt'.format(seedwordsname))
        with open(candidatetxtfile, 'w', encoding='utf-8') as f:
            for word in resultwords:
                f.write(word+'\n')
        print('已经 【{seedwordsname} 类】 的词语筛选，并保存于 {txtfile}'.format(seedwordsname=seedwordsname, txtfile=candidatetxtfile))
        return simwords








