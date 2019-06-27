# Open-Weather
Open-Weather 是一个开源的气象数据获取项目

#工具
## q-weather
运行`qweather.py`可获取由[q-weather.info](http://q-weather.info)提供的国内五分钟实况数据
### 要求
程序基于Python3，**需要安装`requests`库**
### 配置文件
编辑配置文件`config.cfg`中的`stations`项可更改获取的站点(站点WMOID数组)
### 数据储存
获取的数据储存在`data`文件夹下的`WMOID.csv`文件中，**同一时间重复获取数据不会覆盖**
### 使用
运行`qweather.py`获取数据，由运行主机发起请求
