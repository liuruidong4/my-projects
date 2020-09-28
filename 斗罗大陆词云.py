# -*- coding: utf-8 -*-
from pickle import STRING
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba
#打开文本
text = open('斗罗大陆.txt',encoding='utf-8').read()
#分词
text = ' '.join(jieba.cut(text))
#生成对象
mask = np.array(Image.open('timg.jpg'))
wc = WordCloud(mask = mask ,font_path='STCAIYUN.TTF',background_color='white')
wc.generate_from_text(text)
#显示词云
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
#plt.show()
plt.savefig('dlal.jpg',dpi=300)