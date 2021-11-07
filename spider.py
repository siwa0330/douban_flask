from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error,urllib.parse
import sqlite3
import ssl

def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    baseurl = "https://movie.douban.com/top250?start="


    #1.爬取网页
    # datalist = getData(baseurl)
    # html = askUrl(baseurl)
    # soup = BeautifulSoup(html, "html.parser")
    # for item in soup.find_all('div', class_='item'):
    #     print(item)

    datalist = getData(baseurl)
    #print(datalist)
    dbpath = "movie.db"
    saveData2DB(datalist,dbpath)


    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    # }
    # req = urllib.request.Request(url=url,headers=headers)
    # response = urllib.request.urlopen(req)
    # print(response.read().decode('utf8'))

    # data = bytes(urllib.parse.urlencode({"wo":'zheng'}), encoding='utf8')
    # response = urllib.request.urlopen('http://httpbin.org/post', data= data)
    # print(response.read().decode('utf8'))

#正则匹配模版
findLink = re.compile(r'<a href="(.*?)">')
findImg = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findScore = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

#爬取全部网页数据
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askUrl(url)

    #逐一解析数据

        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_='item'):
            data = []    #保存一部电影的所有信息
            item = str(item)

            #影片详情链接
            link = re.findall(findLink, item)[0]
            data.append(link)

            img = re.findall(findImg,item)[0]
            data.append(img)

            titles = re.findall(findTitle,item)  #片名不止一个
            if (len(titles) == 2):
                ctitle = titles[0]   #添加中文片名
                data.append(ctitle)
                otitle = titles[1].replace('/','')  #去掉无关符号
                otitle = otitle.replace(r'\xa0','')  #去掉&nbsp类空格
                data.append(otitle)   #添加外文片名
            else:
                data.append(titles[0])
                data.append(' ')

            score = re.findall(findScore, item)[0]
            data.append(score)

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")    #去掉句号
                data.append(inq)
            else:
                data.append(" ")     #留空

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)     #去掉<br/>
            bd = re.sub('/', ' ',bd)    #替换/
            bd = bd.replace(r'\xa0','')
            data.append(bd.strip())

            datalist.append(data)

    return datalist

def saveData2DB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index==4 or index==5:
                continue
            data[index] = '"'+data[index]+'"'
        sql = """
                insert into movie250(
                info_link,pic_link,cname,oname,score,judge,instroduction,info)
                values (%s)"""%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def init_db(dbpath):
    sql = """
        create table movie250
        (
        id integer primary key autoincrement ,
        info_link text,
        pic_link text,
        cname varchar,
        oname varchar,
        score numeric,
        judge numeric,
        instroduction text,
        info text
        )
    """
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

#获取一个指定url的网页
def askUrl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    request = urllib.request.Request(url,headers=head)
    html=""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf8')
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)

    return html



def saveData():
    pass

if __name__ == "__main__":
    main()