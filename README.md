# fcode-capture 

------------------------------------------------------

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;每到mi.com新品上架，根本抢不到有木有。weibo上一些所谓的“热心人”就会扮演"救世主"，不失时机的放出F-code安慰我等屌丝，但仍是手慢无，又特么是一个坑..

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;是坑也得往里跳啊，24小时手不停的刷新并盯着微博不现实，于是fcode-capture就派上用场了


##### 原料
* cygwin/linux
* python 2.7.x
* curl
* 新浪weibo账号(可选|推荐)
* weibo.cn彩版
* 需先登录F-code购买通道: <a href="http://order.mi.com/queue/f2code" target="_blank">http://order.mi.com/queue/f2code</a>。 为了能快速响应，浏览器最好要保持mi.com登录的状态，以便挖到码时，能及时下单。
* F-code 字母前缀, 比如"XMSH", "XMXP"

##### 配置 fcode-capture 
* 找出"微博搜索"页和几个经常放码的博主主页，生成curl命令填写到curl.xml中去吧;
* 详见 curl.xml;
* 配置样例: curl.simple.xml

##### curl 命令获取方法：
* Chrome 或 Firefox， 调出“开发者工具”.
* 以Chrome为例：依次 "Network" -> "NamePath"(通常都是第一个，"Method"为"GET"的那一条数据) -> 选中并右键 ->  "Copy as cURL"

##### capture.py 的使用
<pre> <code>
Usage: 
./capture.py instance_id
    instance_id, see the xml file  
</code></pre>
一个id对应一个capture进程

------------------------------------------------------

##### fcode-capture 历史更新记录: (自2015-03-19起)

######2015-03-20 更新
    1. 可自定义任务完成时的回调命令.[新增项]
    *2. 丰富原有XMXP数据库，进一步降低‘微博搜索’误报的概率.[被丢弃]


######2015-03-19 更新
	1. 新增程序异常退出报警（响一声）.[新增项]
	2. 修复误报bug
	3. 规范返回码

--------------------------------------------------------

## capture php版

##### capture.php 
    1. 不需要微博账号
    2. 得到微博搜索页url即可
    3. 使用时需要替换$url

--------------------------------------------------------
#####[LICENSE](./LICENSE)
&copy; Deel@d-l.top | [d-l.top](http://d-l.top)
