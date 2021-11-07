import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3

#准备词云所需的字词
con = sqlite3.connect('movie.db')
cur = con.cursor()
sql = 'select instroduction from movie250'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]

#print(text)
cur.close()
con.close()

#分词
cut = jieba.cut(text)
string = ' '.join(cut)
string=string.replace('的','')
string=string.replace('是','')
string=string.replace('了','')
string=string.replace('就','')
string=string.replace('都','')
string=string.replace('和','')
string=string.replace('与','')
#print(len(string))

img = Image.open(r'./static/assets/assets/img/tonghua.jpeg')   #打开遮罩图片
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path=r"Hiragino Sans GB.ttc"
)

wc.generate_from_text(string)

#绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis("off")

plt.savefig(r'./static/assets/assets/img/wordcloud08.jpeg')

