import json
import requests
import re
import os

def getQweatherData(sid):
    #定义正则
    r=[]
    r.append(re.compile(r'<td>瞬时温度</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>24小时变温</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>地面气压</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>相对湿度</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>10分钟平均风向</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>10分钟平均风速</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>1小时降水</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>24小时降水</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>一分钟平均能见度</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>瞬时温度</td>\s*<td>.*?</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>24小时降水</td>\s*<td>.*?</td>\s*<td>(.*?)</td>'))
    r.append(re.compile(r'<td>10分钟平均能见度</td>\s*<td>(.*?)</td>'))

    ele=['t','dt','p','rh','wd','wv','rf','24hrain','vd','date','24hraintime','v'] #设置元素

    page = requests.get("http://q-weather.info/weather/"+str(sid)+"/realtime/")
    page = page.text
    d = {}
    for i in range(len(r)):
        if(len(r[i].findall(page)) != 0):
            d[ele[i]]= r[i].findall(page)[0]
        elif(r[i].findall(page) == "-"):
            d[ele[i]] = "N/A"
        else:
            d[ele[i]]="N/A"
    d['date'] = d['date'][0:16]
    d['24hraintime'] = d['24hraintime'][0:16]
    return d

def Record(path,text):
    file = open(path,'a',encoding='utf-8')
    file.write(text)
    file.close()

if __name__ == "__main__":
    #Load config
    configFile = open("config.cfg",'r',encoding='utf-8')
    config = json.loads(configFile.read(),encoding='utf-8')
    configFile.close()

    data = {}
    if config["stations"]:
        for sid in config["stations"]:
            path = "data/"+str(sid)+".csv"
            if os.path.exists(path) == False:
                Record(path,"Date,t,24h_dt,RH,p,wv,wd,1h_prec,24h_prec,Date_of_24h_prec,1min_v,10min_v\n")
            print("Loading "+str(sid))
            data = getQweatherData(sid)
            print(data)
            text = data["date"]+","+data["t"]+","+data["dt"]+","+data["rh"]+","+data["p"]+","+data["wv"]+","+data["wd"]+","+data["rf"]+","+data["24hrain"]+","+data["24hraintime"]+data["vd"]+","+data["v"]+"\n"
            Record(path,text)

