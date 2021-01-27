from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import six

import re
import time

scoreList = []
commentList = []

print('move_number?')
number = input()

print('how page?')
HowPage = int(input())*20+20

for page in range(0,HowPage,20):
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    url = requests.get('https://movie.douban.com/subject/'+ str(number) +'/comments?start=' + str(page) + '&limit=20&sort=new_score&status=P', headers=headers)
    print(url)
    soup = BeautifulSoup(url.text)
    tags = soup("div", {"class": "comment"})
    # print(url.text)
    # print('text')
    for tag in tags:

        # 获取短评信息
        comment = tag.p.getText()
        

        # 获取得分信息
        try:
            score = tag.find(class_ = re.compile("star"))['class'][0]
        except:
            score = 'NA'

        # 总和列表
        commentList.append(comment)
        scoreList.append(score)

    # 设置间隔时间，并输出循环爬取信息
    print(page)
    time.sleep(np.random.uniform(1, 2))

import jieba
from wordcloud import WordCloud
text = ''
for i in range(len(commentList)):
    text = text + commentList[i]
removes =['这个','电影','没用','就是','一个','导演','还是','不够','故事','这样','可以','没有']
for w in removes:
    jieba.del_word(w)
words = jieba.lcut(text)
cuted = ' '.join(words)
fontpath='PingFang.ttc'

import numpy as np
from PIL import Image
##aimask = np.array(Image.open("ai-mask.jpg"))

wc = WordCloud(font_path=fontpath,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=1000,  # 词云显示的最大词数
               max_font_size=500,  # 字体最大值
               min_font_size=10, #字体最小值
               random_state=42, #随机数
               collocations=False, #避免重复单词
               ##mask=aimask,
               width=1000,height=600,margin=5, #图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
              )
wc.generate(cuted)

import matplotlib.pyplot as plt
plt.figure(dpi=150)
plt.imshow(wc, interpolation='catrom',vmax=1000)
plt.axis("off") #隐藏坐标
plt.show()