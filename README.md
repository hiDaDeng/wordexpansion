

# 一、项目意义

情感分析大多是基于情感词典对文本数据进行分析，所以情感词典好坏、是否完备充足是文本分析的关键。

目前常用的词典都是基于形容词，有

- 知网HowNet
- 大连理工大学情感本体库

但是形容词类型的词典在某些情况下不适用，比如

**华为手机外壳采用金属制作，更耐摔**

由于句子中没有形容词，使用形容词情感词典计算得到的情感得分为0。但是**耐摔**这个动词具有**正面积极情绪**，这个句子的情感的分理应为**正**



可见能够简单快速构建不同领域(手机、汽车等)的情感词典十分重要。但是人工构建太慢，如果让机器帮我们把最有可能带情感的候选词找出来，人工再去筛选构建词典，那该多好啊。那么如何构建呢？



# 二、构建方法

计算机领域有一个算法叫做SO_PMI，互信息。简单的讲个体之间不是完全独立的，往往物以类聚，人以群分。如果我们一开始设定少量的

- 初始正面种子词
- 初始负面种子词

程序会按照“物以类聚人以群分”的思路，

- 根据**初始正面种子词**找到很多大概率为**正面情感的候选词**
- 根据**初始负种子词**找到很多大概率为**负面情感的候选词**

这个包原始作者刘焕勇，项目地址https://github.com/liuhuanyong/SentimentWordExpansion 我仅仅做了简单的封装

# 三、安装

### 2.1 方法一

最简单的安装,现在由于国内外网络不稳定，可能需要尝试几次

```
pip3 install wordexpansion
```

### 2.2 加镜像站点

有的童鞋已经把pip默认安装镜像站点改为国内，如果国内镜像还未收录我的这个包，那么可能会安装失败。只能从国外https://pypi.org/simple站点搜索wordexpansion资源并安装

```
pip3 install wordexpansion -i https://pypi.org/simple
```

### 2.3 国内镜像安装

如果国内镜像站点已经收录，那么使用这个会更快

```
pip3 install wordexpansion -i https://pypi.tuna.tsinghua.edu.cn/simple/
```



# 四、使用方法

### 4.1 文件目录

```
|--test                           #情感词典扩展与构建测试文件夹
     |--find_newwords.py          #测试代码
     |--test_corpus.txt           #语料（某领域）文本数据，5.5M
     |--test_seed_words.txt       #情感种子词，需要手动构建
      
     |--neg_candi.txt             #find_newwords.py运行后发现的负面候选词
     |--pos_candi.txt             #find_newwords.py运行后发现的正面候选词

```

完整项目请移步至https://github.com/thunderhit/wordexpansion

### 4.2 构建种子词

可能我们希望的情感词典几万个，但是种子词100个（正面词50个，负面词50个）说不定就可以。

手动构建的种子词典**test_seed_words.txt**中

- 每行一个词
- 每个词用neg或pos标记
- 词与标记用空格间隔

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



### 4.2 准备发现情感新词

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



### 4.3 输出的结果

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



# 五、注意：
1、so_pmi算法效果受训练语料影响，语料规模越大，效果越好  
2、so_pmi算法效率受训练语料影响，语料越大，训练越耗时。100个种子词，5M的数据，大约耗时62.679秒  
3、候选词的选择，可根据PMI值，词长，词性设定规则，进行筛选  



# 支持一下

![](https://github.com/thunderhit/DaDengAndHisPython/blob/master/img/my_zanshang_qrcode.jpg)

# 更多
- [B站:大邓和他的python](https://space.bilibili.com/122592901/channel/detail?cid=66008)
- 公众号：大邓和他的python
- [知乎专栏：数据科学家](https://zhuanlan.zhihu.com/dadeng)
- [《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)，已经于近期重新录制上传



> README.md为本人所写，代码底层完全为刘焕勇设计。
>
> 大邓项目地址https://github.com/thunderhit/wordexpansion
>
> 原项目(刘焕勇)地址https://github.com/liuhuanyong/SentimentWordExpansion



