from wordexpansion import W2VModels
import pandas as pd
import os

#初始化模型
model = W2VModels(cwd=os.getcwd(), lang='english')
#df = pd.read_excel('data.xlsx')
#model.train(documents=df['text'])
model.train(documents=list(open('documents.txt').readlines()))

integrity = [w for w in open('seeds/integrity.txt').read().split('\n') if w!='']
innovation = [w for w in open('seeds/innovation.txt').read().split('\n') if w!='']
quality = [w for w in open('seeds/quality.txt').read().split('\n') if w!='']
respect = [w for w in open('seeds/respect.txt').read().split('\n') if w!='']
teamwork = [w for w in open('seeds/teamwork.txt').read().split('\n') if w!='']


model.find(seedwords=integrity, seedwordsname='integrity', topn=100)
model.find(seedwords=innovation, seedwordsname='innovation', topn=100)
model.find(seedwords=quality, seedwordsname='quality', topn=100)
model.find(seedwords=respect, seedwordsname='respect', topn=100)
model.find(seedwords=teamwork, seedwordsname='teamwork', topn=100)
