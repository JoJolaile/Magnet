import requests
import bs4
import urllib.request
import urllib.parse
import json
import re
import numpy as np
import random

'''
注意网址的变化，执行不成功时，首先检查网址是否变化
'''

USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 "
    "Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 "
    "Safari/535.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
    "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 "
    "TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 "
    "LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
    "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; "
    "360SE)",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X "
    "MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "]
    
#反反爬虫，增加header模拟浏览器访问
headers = {'User-Agent':random.choice(USER_AGENTS)}

URLlist = []

#获得磁力链接
def GetCili(ciliurl):

    hisspd = ""

    rescili = requests.get(ciliurl,headers=headers)
    soupcili = bs4.BeautifulSoup(rescili.text,'html.parser')

    #获取text area内容的方法
    magnet = soupcili.textarea.get_text()

    # div后为字符串，使用文件大小关键字后10为再通过‘<'来去掉多余字符
    size   = "Size:   " + str(soupcili.find_all('div',class_='bt-info')).split("文件大小：")[1][0:10]

    hisspd = "Speed:  " + '\n' + speed(magnet)

    #换行
    print(magnet,'\n',size.split('<')[0],'\n',hisspd,'\n')

def speed(content):

    result = ""
    url = 'http://tools.bugscaner.com/api/magnetspeed/'
    data ={}

    data['User-Agent'] = random.choice(USER_AGENTS)
    data['MIME 类型'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    data['magnet'] = content

    #data = urllib.parse.urlencode(data).encode('utf-8')

    req = requests.post(url=url, data=data, headers=headers)

    #此时req的返回是jason，str类型
    #print(type(req.text))

    #此处使用ulr 没有加header，改用requests访问
    #response = urllib.request.urlopen(url,data)

    #json转化为dic
    target = json.loads(req.text)

    if target['secess'] == True:
        #将结果'45.53MB/s<br>44.35MB/s<br>26.47MB/s<br>19.67MB/s’，只保留数据后，转为float
        #类型，再取平均数
        #spdlst = list(map(float,re.findall(r"\d+\.?\d*",target['speed'])))
        #speed = round(np.mean(spdlst),2)
        #result = "speed:  " + str(speed) + "MB/s"
        #上面算平均值太费劲，直接展示了
        result = target['speed'].replace("<br>",",")
        if  result.split('/s')[0][-2] == 'M':
            #使用eval去除结果两端''
            Fastsp = eval(result.split('MB')[0])
        else:
            Fastsp = 0
        URLlist.append([content,Fastsp])
    else:
        result = "Dead Magnet!"
    
    return result


def CrXunlei(Fasturl):

    address = Fasturl.split('&')[0].split('btih:')[1]

    filenm = Fasturl.split('&dn=')[1]

    url = 'http://homecloud.remote.xiazaibao.xunlei.com/createBtTask?pid=001CC227DE9B775X0001&v=2&ct=0&callback=window.parent._POST_CALLBACK_4_'

    headers = {}

    headers['User-Agent'] = random.choice(USER_AGENTS)
    headers['Referer'] = 'http://yc.xzb.xunlei.com/'
    headers['Origin'] = 'http://yc.xzb.xunlei.com'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Cache-Control'] = 'no-cache'
    headers['Pragma'] = 'no-cache'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    headers['Upgrade-Insecure-Requests'] = '1'

    headers['Cookie'] = 'sessionid=ws001.15A25AB0D1940D53E014B25F3BBA30C8;userid=335844876'

    rawdata = '{"path":"C:/TDDOWNLOAD/","infohash":"' + address + '","name":"' + filenm + '","btSub":[0,1,2,3],"loalfile":""}'

    data = "json=" + urllib.parse.quote(rawdata)

    req = requests.post(url=url, data=data, headers=headers)

    print(req.text.encode('utf8'))

def run():

    # 输入要查找的番号
    print ('-----要查个番号呢----')
    fanhao = input ('老司机输入吧:  ')
    
    url = 'http://zhongziba.biz/search?wd='+fanhao # 注意网址经常会变，之前是zhongziba.me后来改成.biz
    res = requests.get(url,headers=headers)
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    # 使用与要查找位置最近的DIV后的class=的关键字查找
    targets = soup.find_all('div',class_='media-body')

    for each in targets:
    # 使用a标签的超链接href关键字搜索字典
        targeturl = "http://zhongziba.biz" + each.a.attrs['href']
        GetCili(targeturl)

    # 选出最快的链接，创建迅雷下载，链接速度放在URLlist中，结构为列表中的列表【种子，速度】

    def TakeSecond(elem):
        return elem[1]

    # 指定第二个元素排序
    if URLlist != []:
        URLlist.sort(key=TakeSecond,reverse=True)
        Fasturl = URLlist[0][0]
        print(Fasturl)
        CrXunlei(Fasturl)
    else:
        print('没有可用链接')

if __name__ == "__main__":
    run()
