
现已将项目wordexpansion融入到[cntext](https://github.com/hidadeng/cntext)中，欢迎各位star

<br>

# 一、项目意义

情感分析大多是基于情感词典对文本数据进行分析，所以情感词典好坏、是否完备充足是文本分析的关键。

目前常用的词典都是基于形容词，有

- 知网HowNet
- 大连理工大学情感本体库

但是形容词类型的词典在某些情况下不适用，比如

**华为手机外壳采用金属制作，更耐摔**

由于句子中没有形容词，使用形容词情感词典计算得到的情感得分为0。但是**耐摔**这个动词具有**正面积极情绪**，这个句子的情感的分理应为**正**



可见能够简单快速构建不同领域(手机、汽车等)的情感词典十分重要。但是人工构建太慢，如果让机器帮我们把最有可能带情感的候选词找出来，人工再去筛选构建词典，那该多好啊。 那么如何快速自动的新建或者扩充词表呢？



<br>

# 二、构建思路

- 共现法，参考https://github.com/liuhuanyong/SentimentWordExpansion
- 词向量，参考https://github.com/MS20190155/Measuring-Corporate-Culture-Using-Machine-Learning





<br>

## 2.1 共现法扩充词表

计算机领域有一个算法叫做SO_PMI，互信息。简单的讲个体之间不是完全独立的，往往物以类聚，人以群分。如果我们一开始设定少量的

- 初始正面种子词
- 初始负面种子词

程序会按照“物以类聚人以群分”的思路，

- 根据**初始正面种子词**找到很多大概率为**正面情感的候选词**
- 根据**初始负种子词**找到很多大概率为**负面情感的候选词**

这个包原始作者刘焕勇，项目地址https://github.com/liuhuanyong/SentimentWordExpansion 我仅仅做了简单的封装





## 2.2 词向量扩充词表

共现法，词语之间的独立无相关性依然很强，依然认为词语与词语是不可以比较的。其实词语里潜藏着很多线索，例如中国传统文化中的金木水火土、性别(阴阳)等信息。例如

- “铁”、“铜”、“钢”
- “国王“、“王后“、“男人“、“女人“

如果能抽取出每个词的特征，将每个词用同样长度的向量表示，例如100维。那么咱们中学阶段的cos余弦公式可以计算任意两个词的相似度。

参照论文使用机器学习构建五类企业文化词典

> Kai Li, Feng Mai, Rui Shen, Xinyan Yan, [**Measuring Corporate Culture Using Machine Learning**](https://academic.oup.com/rfs/advance-article-abstract/doi/10.1093/rfs/hhaa079/5869446?redirectedFrom=fulltext), *The Review of Financial Studies*, 2020
>
> 代码发布在github https://github.com/MS20190155/Measuring-Corporate-Culture-Using-Machine-Learning

作者github的代码，我技术水平有限，很难直接拿来用，我修改了两处。

- 原作者使用的stanfordnlp处理英文分词；wordexpansion改为jieba处理中文、nltk处理英文

- 原作者在构建word2vec模型，考虑了Ngram；wordexpansion未考虑Ngram

  

两处更改，降低了代码的复杂程度，方便自己封装成包，供大家使用。大家也可根据自己能力，直接使用作者提供的代码。





<br>


# 三、安装



最简单的安装,现在由于国内外网络不稳定，可能需要尝试几次

```
pip3 install wordexpansion
```



<br>

# 四、test项目文件目录

>**注意：**
>所有的txt文件，不论输入的还是程序输出的结果，均采用utf-8编码。

```
|---test 
    |---共现法
       |--find_newwords.py          #共现法测试代码
       |--corpus1.txt               #语料（媒体报道）文本数据，5.5M
       |--test_seed_words.txt       #情感种子词，需要手动构建
       |--neg_candi.txt             #find_newwords.py运行后发现的负面候选词
       |--pos_candi.txt             #find_newwords.py运行后发现的正面候选词
       
    |---词向量法
       |--run_w2v.py                #词向量法测试代码
       |--corpus2.txt               #语料（企业文化）文本数据，34M
       |--seeds                     #五种企业文化初始候选词(5个txt)
       |--model                     #word2vec训练过程中的模型(运行时产生的副产品)
       |--candidate_words           #五种企业文化词典（5个txt）
       

```



# 五、共现法代码

### 5.1 准备构建种子词

可能我们希望的情感词典几万个，但是种子词100个（正面词50个，负面词50个）说不定就可以。

手动构建的种子词典**test_seed_words.txt**中

- 每行一个词
- 每个词用neg或pos标记
- 词与标记用tab键间隔

```
休克	neg
如出一辙	neg
渴求	neg
扎堆	neg
休整	neg
关门	neg
阴晴不定	neg
喜忧参半	neg
起起伏伏	neg
一厢情愿	neg
松紧	neg
最全	pos
雄风	pos
稳健	pos
稳定	pos
拉平	pos
保供	pos
修正	pos
稳	pos
稳住	pos
保养	pos
...
...
```



### 5.2 发现情感新词

已经安装好了**wordexpansion**，现在我们新建一个名为**find_newwords.py**的测试代码

代码中的

```python
from wordexpansion import ChineseSoPmi

sopmier = ChineseSoPmi(inputtext_file='test_corpus.txt',
                       seedword_txtfile='test_seed_words.txt',
                       pos_candi_txt_file='pos_candi.txt',
                       neg_candi_txtfile='neg_candi.txt')
sopmier.sopmi()
```



我们的语料数据**test_corpus.txt** 文件5.5M，100个候选词，运行程序大概耗时60s



### 5.3 输出的结果

**find_newwords.py**运行结束后，会在**同文件夹内(find_newwords.py所在的文件夹)**发现有两个新的txt文件

- pos_candi.txt
- neg_candi.txt

打开**pos_candi.txt**, 我们看到

```
word,sopmi,polarity,word_length,postag
保持,87.28493062512524,pos,2,v
风险,70.15627986116269,pos,2,n
货币政策,66.28476448498694,pos,4,n
发展,64.40272795986517,pos,2,vn
不要,63.71800916752807,pos,2,df
理念,61.2024367757337,pos,2,n
整体,59.415315156715586,pos,2,n
下,59.321140440512984,pos,1,f
引导,58.5817208758171,pos,2,v
投资,57.71720491331896,pos,2,vn
加强,57.067969337267684,pos,2,v
自己,53.25503772499689,pos,2,r
提升,52.80686380719989,pos,2,v
和,52.12334472663675,pos,1,c
稳步,51.58193211655792,pos,2,d
重要,51.095865548255034,pos,2,a
...
```

打开**neg_candi.txt**, 我们看到

```
word,sopmi,polarity,word_length,postag
心灵,33.17993872989303,neg,2,n
期间,31.77900620939178,neg,2,f
西溪,30.87839808390589,neg,2,ns
人事,29.594976229171877,neg,2,n
复杂,29.47870186147108,neg,2,a
直到,27.86014637934966,neg,2,v
宰客,27.27304813428452,neg,2,nr
保险,26.433136238404746,neg,2,n
迎来,25.83859896903048,neg,2,v
至少,25.105021416064616,neg,2,d
融资,25.09148586460598,neg,2,vn
或,24.48343281812743,neg,1,c
列,22.20695894382675,neg,1,v
存在,22.041049266517774,neg,2,v
...
```



从上面的结果看，正面候选词较好，负面候选词有点差强人意。虽然差点，但节约了很多很多时间。

现在电脑已经帮我们找出候选词，我们人类最擅长找毛病，对neg_candi.txt和pos_candi.txt我们人类只需要一个个挑毛病，把不带正负情感的词剔除掉。这样经过一段时间的剔除工作，针对具体研究领域的专业情感词典就构建出来了。



# 六、词向量法代码

## 6.1 准备种子词

词向量法程序会挖掘出原始数据中的所有词的词向量，这时候如果给词向量模型传入种子词，会根据向量的远近识别出多个近义词。人工构建了五大类企业文化词典，存放在txt中，即

- innovation.txt
- integrity.txt
- quality.txt
- respect.txt
- teamwork.txt

注意，在txt中，每行一个词语。



### 6.2 发现情感新词

已经安装好了**wordexpansion**，现在我们新建一个名为**run_w2v.py**的测试代码

代码中的

```python
from wordexpansion import W2VModels

from similarity import W2VModels
import pandas as pd
import os

#初始化模型
model = W2VModels(cwd=os.getcwd())
model.train(documents=list(open('documents.txt').readlines()))

#导入种子词
integrity = [w for w in open('seeds/integrity.txt').read().split('\n') if w!='']
innovation = [w for w in open('seeds/innovation.txt').read().split('\n') if w!='']
quality = [w for w in open('seeds/quality.txt').read().split('\n') if w!='']
respect = [w for w in open('seeds/respect.txt').read().split('\n') if w!='']
teamwork = [w for w in open('seeds/teamwork.txt').read().split('\n') if w!='']

#根据种子词，筛选出没类词最相近的前100个词
model.find(seedwords=integrity, seedwordsname='integrity', topn=100)
model.find(seedwords=innovation, seedwordsname='innovation', topn=100)
model.find(seedwords=quality, seedwordsname='quality', topn=100)
model.find(seedwords=respect, seedwordsname='respect', topn=100)
model.find(seedwords=teamwork, seedwordsname='teamwork', topn=100)

```



我们的语料数据**30+** 文件30+M，50多个候选词，运行程序大概耗时30s

<br>

### 6.3 输出的结果

**run_w2v.py**运行结束后，会在**candidate_words内**发现有5个新的txt文件

- innovation.txt
- integrity.txt
- quality.txt
- respect.txt
- teamwork.txt

打开**innovation.txt**, 我们看到

```
innovation
innovate
innovative
creativity
creative
create
passion
passionate
efficiency
efficient
excellence
pride
enhance
expertise
optimizing
adapt
capability
awareness
creating
value-added
optimize
leveraging
attract
innovative
manufacture
attracting
maximizing
fine-tune
enable
headquarter
platform
tightly
aligned
flexible
fulfillment
rationalize
back-office
...
```

打开**respect.txt**, 我们看到

```
respectful
talent
talented
employee
dignity
empowerment
empower
skills
backbone
training
database
designers
sdk
recruit
engine
dealers
selecting
resource
onsite
computer
functions
wholesalers
educational
expertise
coordination
value-added
...

```

同理，在其他几类企业文化词典txt中产生了符合预期的词语。

现在电脑已经帮我们找出5类企业文化候选词，我们人类最擅长找毛病，对5个txt文件，我们人类只需要一个个挑毛病，把不带正负情感的词剔除掉。这样经过一段时间的剔除工作，针对具体研究领域的专业情感词典就构建出来了。





<br>

# 七、注意：
1. so_pmi算法效果受训练语料影响，语料规模越大，效果越好  

2. so_pmi算法效率受训练语料影响，语料越大，训练越耗时。100个种子词，5M的数据，大约耗时62.679秒  

3. 候选词的选择，可根据PMI值，词长，词性设定规则，进行筛选  

4. **所有的txt文件，不论输入的还是程序输出的结果，均采用utf-8编码。**

5. 词向量法没有考虑Ngram，如果采用了Ngram， 可能会挖掘出该场景下的词语组合。但是程序运行时间可能会更慢。

6. 如果刚刚好也想使用**企业文化5大类**这个具体场景，记得引用论文

7. > Kai Li, Feng Mai, Rui Shen, Xinyan Yan, Measuring Corporate Culture Using Machine Learning, *The Review of Financial Studies*,2020



<br>

# 如果

如果您是经管人文社科专业背景，编程小白，面临海量文本数据采集和处理分析艰巨任务，可以参看[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)视频课。作为文科生，一样也是从两眼一抹黑开始，这门课程是用五年时间凝缩出来的。自认为讲的很通俗易懂o(*￣︶￣*)o，

- python入门
- 网络爬虫
- 数据读取
- 文本分析入门
- 机器学习与文本分析
- 文本分析在经管研究中的应用

感兴趣的童鞋不妨 戳一下[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)进来看看~

[![](img/课程.png)](https://ke.qq.com/course/482241?tuin=163164df)



# 更多

- [B站:大邓和他的python](https://space.bilibili.com/122592901/channel/detail?cid=66008)

- 公众号：大邓和他的python

- [知乎专栏：数据科学家](https://zhuanlan.zhihu.com/dadeng)

![](img/大邓和他的Python.png)
<br>





