#!/usr/bin/env python3
# coding: utf-8
# File: so-pmi.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-4-4

import jieba.posseg as pseg
import jieba
import math,time

class ChineseSoPmi:
    def __init__(self, inputtext_file, seedword_txtfile, pos_candi_txt_file, neg_candi_txtfile):

        self.text_file = inputtext_file
        self.pos_candi_txt_file = pos_candi_txt_file
        self.neg_candi_txtfile = neg_candi_txtfile
        self.seedword_txtfile = seedword_txtfile

    '''分词'''
    def seg_corpus(self, train_data, seedword_txtfile):
        #将情感词加入到用户词典当中，保证分词能够将种子情感词切开
        sentiment_words = [line.strip().split('\t')[0] for line in open(seedword_txtfile, encoding='utf-8')]
        for word in sentiment_words:
            jieba.add_word(word)
        seg_data = list()
        count = 0
        for line in open(train_data, encoding='utf-8'):
            line = line.strip()
            count += 1
            if line:
                seg_data.append([word.word for word in pseg.cut(line) if word.flag[0] not in ['u','w','x','p','q','m']])
            else:
                continue
        return seg_data

    '''统计搭配次数'''
    def collect_cowords(self, seedword_txtfile, seg_data):
        def check_words(sent):
            if set(sentiment_words).intersection(set(sent)):
                return True
            else:
                return False
        cowords_list = list()
        window_size = 5
        count = 0
        sentiment_words = [line.strip().split('\t')[0] for line in open(seedword_txtfile, encoding='utf-8')]
        for sent in seg_data:
            count += 1
            if check_words(sent):
                for index, word in enumerate(sent):
                    if index < window_size:
                        left = sent[:index]
                    else:
                        left = sent[index - window_size: index]
                    if index + window_size > len(sent):
                        right = sent[index + 1:]
                    else:
                        right = sent[index: index + window_size + 1]
                    context = left + right + [word]
                    if check_words(context):
                        for index_pre in range(0, len(context)):
                            if check_words([context[index_pre]]):
                                for index_post in range(index_pre + 1, len(context)):
                                    cowords_list.append(context[index_pre] + '@' + context[index_post])
        return cowords_list

    '''计算So-Pmi值'''
    def collect_candiwords(self, seg_data, cowords_list, seedword_txtfile):
        '''互信息计算公式'''
        def compute_mi(p1, p2, p12):
            return math.log2(p12) - math.log2(p1) - math.log2(p2)
        '''统计词频'''
        def collect_worddict(seg_data):
            word_dict = dict()
            all = 0
            for line in seg_data:
                for word in line:
                    if word not in word_dict:
                        word_dict[word] = 1
                    else:
                        word_dict[word] += 1
            all = sum(word_dict.values())
            return word_dict, all
        '''统计词共现次数'''
        def collect_cowordsdict(cowords_list):
            co_dict = dict()
            candi_words = list()
            for co_words in cowords_list:
                candi_words.extend(co_words.split('@'))
                if co_words not in co_dict:
                    co_dict[co_words] = 1
                else:
                    co_dict[co_words] += 1
            return co_dict, candi_words
        '''收集种子情感词'''
        def collect_sentiwords(seedword_txtfile, word_dict):
            pos_words = set([line.strip().split('\t')[0] for line in open(seedword_txtfile, encoding='utf-8') if
                             line.strip().split('\t')[1] == 'pos']).intersection(set(word_dict.keys()))
            neg_words = set([line.strip().split('\t')[0] for line in open(seedword_txtfile, encoding='utf-8') if
                             line.strip().split('\t')[1] == 'neg']).intersection(set(word_dict.keys()))
            return pos_words, neg_words
        '''计算sopmi值'''
        def compute_sopmi(candi_words, pos_words, neg_words, word_dict, co_dict, all):
            pmi_dict = dict()
            for candi_word in set(candi_words):
                pos_sum = 0.0
                neg_sum = 0.0
                for pos_word in pos_words:
                    p1 = word_dict[pos_word] / all
                    p2 = word_dict[candi_word] / all
                    pair = pos_word + '@' + candi_word
                    if pair not in co_dict:
                        continue
                    p12 = co_dict[pair] / all
                    pos_sum += compute_mi(p1, p2, p12)

                for neg_word in neg_words:
                    p1 = word_dict[neg_word] / all
                    p2 = word_dict[candi_word] / all
                    pair = neg_word + '@' + candi_word
                    if pair not in co_dict:
                        continue
                    p12 = co_dict[pair] / all
                    neg_sum += compute_mi(p1, p2, p12)

                so_pmi = pos_sum - neg_sum
                pmi_dict[candi_word] = so_pmi
            return pmi_dict

        word_dict, all = collect_worddict(seg_data)
        co_dict, candi_words = collect_cowordsdict(cowords_list)
        pos_words, neg_words = collect_sentiwords(seedword_txtfile, word_dict)
        pmi_dict = compute_sopmi(candi_words, pos_words, neg_words, word_dict, co_dict, all)
        return pmi_dict

    '''保存结果'''
    def save_candiwords(self, pmi_dict, pos_candi_txt_file, neg_candi_txtfile):
        def get_tag(word):
            if word:
                return [item.flag for item in pseg.cut(word)][0]
            else:
                return 'x'
        pos_dict = dict()
        neg_dict = dict()
        f_neg = open(neg_candi_txtfile, 'w+', encoding='utf-8')
        f_pos = open(pos_candi_txt_file, 'w+', encoding='utf-8')

        for word, word_score in pmi_dict.items():
            if word_score > 0:
                pos_dict[word] = word_score
            else:
                neg_dict[word] = abs(word_score)

        for word, pmi in sorted(pos_dict.items(), key=lambda asd:asd[1], reverse=True):
            f_pos.write(word + ',' + str(pmi) + ',' + 'pos' + ',' + str(len(word)) + ',' + get_tag(word) + '\n')
        for word, pmi in sorted(neg_dict.items(), key=lambda asd:asd[1], reverse=True):
            f_neg.write(word + ',' + str(pmi) + ',' + 'neg' + ',' + str(len(word)) + ',' + get_tag(word) + '\n')
        f_neg.close()
        f_pos.close()
        return

    def sopmi(self):
        print('step 1/4:...seg corpus ...')
        start_time  = time.time()
        seg_data = self.seg_corpus(self.text_file, self.seedword_txtfile)
        end_time1 = time.time()
        print('step 1/4 finished:...cost {0}...'.format((end_time1 - start_time)))
        print('step 2/4:...collect cowords ...')
        cowords_list = self.collect_cowords(self.seedword_txtfile, seg_data)
        end_time2 = time.time()
        print('step 2/4 finished:...cost {0}...'.format((end_time2 - end_time1)))
        print('step 3/4:...compute sopmi ...')
        pmi_dict = self.collect_candiwords(seg_data, cowords_list, self.seedword_txtfile)
        end_time3 = time.time()
        print('step 1/4 finished:...cost {0}...'.format((end_time3 - end_time2)))
        print('step 4/4:...save candiwords ...')
        self.save_candiwords(pmi_dict, self.pos_candi_txt_file, self.neg_candi_txtfile)
        end_time = time.time()
        print('finished! cost {0}'.format(end_time - start_time))

def test():
    sopmier = ChineseSoPmi(inputtext_file='corpus.txt',
                           seedword_txtfile='seed_words.txt',
                           pos_candi_txt_file='neg_candi.txt',
                           neg_candi_txtfile='pos_candi.txt')
    sopmier.sopmi()

#test()
