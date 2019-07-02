import json
import requests
import re
import math
import time
import os

def qukuohao(val):
    if re.match("\(\S+\)",val):
        a = ""
        for i in range(len(val)-2):
            a += val[i+1]
        val = a
        val = str(round(float(val),1))
    return val

def getData(uid,pfix):
    #定义正则
    r = re.compile(r'<tbody>\s+<tr align="center">\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>\s+<tr align="center">\s+<td>.*?</td>\s+<td>(.*?)</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+<td>.*?</td>\s+</tr>')

    data = {} #创建数据集
    ele=['time','t','p','rh','wd','wv','rf','v','t12'] #设置元素

    url = "http://q-weather.info/weather/"+str(uid)+"/today/"
    try:
        page = requests.get(url)
        page = page.text
        for i in range(len(ele)):
            if r.findall(page)[0][i] == "" or r.findall(page)[0][i] == "-":
                data[ele[i]] = "9998"
            else:
                data[ele[i]] = r.findall(page)[0][i]
    except:
        print(uid,"Connection / Re failed!")
        data={'time':'No data','t':'N/A','p':'N/A','rh':'N/A','wd':'N/A','wv':'N/A','rf':'N/A','v':'N/A','t12':'N/A'}

    #拆括号
    for keys in data:
        data[keys] = qukuohao(data[keys])

    #计算部分
    #更改时间格式
    if data['time'] != 'No data':
        timeword = ""
        for j in [0,1,2,3,5,6,8,9,11,12,14,15]:
            timeword +=data['time'][j]
        data['time'] = timeword
    
    #更改风向
    if data['wd'] != "N/A" and data['wd'] != '9998':
        r = re.compile(r'(.*?)/\S*')
        data['wd'] = r.findall(data['wd'])[0]
    
    #计算露点
    if data['t']!='N/A' and data['rh']!='N/A':
        e=float(data['rh'])*0.01*6.1078*pow(2.71828,(17.2693882*float(data['t']))/(float(data['t'])+273.3))
        td = (4717.30608-35.86*math.log(e/6.1078))/(17.2693882-math.log(e/6.1078))
        data['td']=round(td-273.16,1)
    else:
        data['td']='9998'

    #计算气压
    if data['t']!='N/A' and data['t12']!='N/A' and data['p']!='N/A':
        tm = (float(data['t'])+float(data['t12']))/2+float(pfix)/400
        data['p0'] = round(float(data['p'])*pow(10,float(pfix)/(18400*(1+tm/273))),1)
    else:
        data['p0'] = '998'

    d = [data['time'],round(float(data['t']),1),data['td'],int(data['rh']),round(float(data['p']),1),data['p0'],int(data['wd']),round(float(data['wv']),1),round(float(data['rf']),1),round(float(data['v']),3)]

    return d

def SaveAsJson(uid,data):
    path = "data/"+str(uid)+".json"
    if os.path.exists(path) == False:
        file = open(path,'w',encoding='utf-8')
        file.write('{}')
        file.close()
    file = open(path,'r',encoding='utf-8')
    oridata = json.loads(file.read())
    file.close()
    oridata[data[0]] = data[1:]
    file = open(path,'w+',encoding='utf-8')
    file.write(json.dumps(oridata))
    file.close()


if __name__ == "__main__":
    #引入配置文件
    confile = open("config.cfg",'r',encoding='utf-8')
    config = json.loads(confile.read())
    confile.close()

    if config["saveAsJson"]:
        for s in config['stations']:
            data = getData(s,config['pfix'][str(s)])
            print(s,data)
            if data[0] != 'No data':
                SaveAsJson(s,data)
