# 优化自https://github.com/cyloveyou/SentinelData_Download2023/blob/main/readme.md

# 哨兵1号数据批量下载


3. 哥白尼数据空间生态系统**新网址**: https://dataspace.copernicus.eu/
4. 由于哥白尼旧的平台已经正式关闭了，旧平台关闭也就意味着旧平台的数据API接口失效，而目前网络上大部分介绍的脚本都或多或少出现有下载慢、难调试等各种问题，**本脚本根据市场目前已有的脚本加以改善，在脚本中加入科学上网，提高了下载速度；同时自主优化了检索脚本，使得检索调试变得简；最后结合多进程技术提高下载速度。**

---

## 🍀脚本构成

1. 脚本中主要包含一个SentinelDownload类用来组织各种下载函数，其具体包含有以下函数
   - CreatURL:构造检索URL
   - GetAccessToken:根据用户名和密码获取token（下载文件时需要token+下载链接）
   - Search:根据检索URL检索数据
   - Download1:单个数据文件的下载
   - SingleDownload:单一进程下载
   - MultiDownload:多进程下载
2. 代码入口程序包含了一些参数设置，具体设置教程见下文。

---

## 🌸使用教程

主要包括：设置SearchURL、设置本地代理，设置保存路径，设置用户名和密码四个部分

### 设置SearchURL

1. 获取SearchURL，进入[哥白尼数据中心Copernicus Browser](https://dataspace.copernicus.eu/browser/?zoom=3&lat=25.95804&lng=0&themeId=DEFAULT-THEME&visualizationUrl=https%3A%2F%2Fsh.dataspace.copernicus.eu%2Fogc%2Fwms%2Fa91f72b5-f393-4320-bc0f-990129bd9e63&datasetId=S2_L2A_CDAS&demSource3D="MAPZEN"&cloudCoverage=30)，像正常检索数据意义设置好各种参数，包括不限于感兴趣区域的设置、数据等级、传感器日期范围等字段的设置。各项参数设置完毕后，先别着急点击Search。
   ![image-20231118151450498](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/202311181514712.png)
2. 鼠标右键打开开发者模式(检查)，按下图操作
   ![image-20231118151722972](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/202311181517068.png)
3. 根据下图找到检索URL，将内容复制到SearchURL.txt文件中，脚本将对左侧所有检索结果（不仅仅是显示的50条，包括未显示的Load more）进行批量下载。![image-20231118151919918](https://mmbiz.qpic.cn/mmbiz_png/OTZgt9MuxqeNGKjz4wGrF4gvqMmIEgJLgR7KE0KadNs6UoTV0orsJOGf2FibXQalicYPAswCMNh8h8fQUru9fQeQ/640?wx_fmt=png&from=appmsg)
4. 至此，SearchURL设置完成。

### 设置本地代理

1. 开启科学上网，具体八仙过海，此处做不赘述。**值得注意的是：需要保证代理流量足够**

2. Windows自带搜索框，搜索`Internet属性`，按下图操作。
   ![image-20231118153242930](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/202311181532045.png)

3. 打开代码文件`NewSentinelDownload.py`，在程序中照猫画虎设置代理，注意对应代码片段位置在开头。

   ![image-20231119202727706](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/202311192027753.png)

4. 至此，代理设置完成

### 设置保存路径

1. 比较简单，看看就行，注意路径中是`/`，如果Windows直接拷贝地址需要注意修改，文件夹路径可以不存在，有创建路径的函数。

![image-20231119202619342](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/202311192026382.png)

### 设置用户名和密码

1.[Copernicus Data Space Ecosystem | Europe's eyes on Earth](https://dataspace.copernicus.eu/)的登录用户名和密码

![image-20231119202631799](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/202311192026840.png)

至此完成所有设置，执行python脚本即可进行下载，**需要注意的是**：正在下载的文件会在Temp文件夹中存在，下载完毕的文件会移动到Finish文件夹中，Finish中已经存在的文件不会进行二次下载，可以Pycharm里面执行，也可以命令行执行，下面展示Pycharm执行的效果:

![image-20231119215302326](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/202311192153412.png)

---
