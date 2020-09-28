# coding = utf-8
from bs4 import BeautifulSoup  #网页解析，获取数据
import re  #正则表达式，文字匹配
import requests  #指定URL，获取网页数据
import xlwt #excel操作
import sqlite3  #进行sqlite操作

findlink  = re.compile(r'<a href="(.*?)">') #影片详情链接规则
findimgsrc = re.compile(r'<img .*src="(.*?)"',re.S) #影片图片规则，忽略换行符
findtitle = re.compile(r'<span class="title">(.*)</span>')
findpingfen = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findpeople = re.compile(r'<span>(\d*)人评价</span>')
findgaikuang = re.compile(r'<span class="inq">(.*)</span>')
findbd = re.compile(r'<p class="">(.*?)</p>',re.S) #因为有换行符所以re.S
def main():
    baseurl = "https://movie.douban.com/top250?start=" #添加数即可
    datalist = getData(baseurl)
    savepath = "豆瓣电影top250.xls"
    #3.保存数据
    saveData(datalist,savepath)
#爬取网页   
def getData(baseurl):
    datalist = []
    for i  in range(0,10):  #调用十次
        url = baseurl+str(i*25)
        html = getone(url) #保存获取到的网页源码
        soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all('div',class_='item'):#查找符合要求的字符串
            # print(item) 
            data = [] #保存一部电影的所有信息
            item= str(item)
            link = re.findall(findlink,item)[0]  #影片详情链接
            data.append(link)
            imgsrc = re.findall(findimgsrc,item)  #图片链接
            data.append(imgsrc)
            title = re.findall(findtitle,item) #可能只有中文名
            if len(title) ==2:
                ctitle = title[0]
                data.append(ctitle)
                otitle = title[1].replace('/','')#去掉无关符号
                data.append(otitle)
            else:
                data.append(title[0])
                data.append(' ') #外国名字留空
            pingfen = re.findall(findpingfen,item)[0]
            data.append(pingfen)
            people = re.findall(findpeople,item)[0]
            data.append(people)
            gaikuang = re.findall(findgaikuang,item)
            if len(gaikuang)==1:
                data.append(gaikuang)
            else:
                data.append(' ')
            bd = re.findall(findbd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?',' ',bd) #去掉<br/>
            data.append(bd.strip()) #去掉前后空格
            datalist.append(data) #处理好的一部信息放入datalist
    return datalist
#保存数据

#指定一个URL的网页信息
def getone(url):
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    req = requests.get(url,headers=head)
    html = req.text
    return html

def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
    col =('电影详情链接','图片链接','影片中文名','影片外文名','评分','评价数','概况','相关信息')
    for i in range(0,8):
        sheet.write(0,i,col[i]) #写好列名字
    for i in range(0,250):
        print(f'第{i}条')
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j]) #数据
    book.save(savepath)
if __name__ == "__main__":
    main()
    print('爬取完毕')