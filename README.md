基金数据来源
需要获得3类数据，数据均来自天天基金网。

(1)基金列表
http://fund.eastmoney.com/js/fundcode_search.js
格式：["000001","HXCZ","华夏成长","混合型","HUAXIACHENGZHANG"]


1. 公司列表(Github上直接打开好像会提示not found,复制到浏览器上方直接进入即可)：[http://fund.eastmoney.com/js/jjjz_gs.js]()
2. 基金列表：http://fund.eastmoney.com/js/fundcode_search.js
3. 基金信息1：http://fund.eastmoney.com/pingzhongdata/'+code+'.js‘
    其中,code为6位整数，如000001的URL位=为http://fund.eastmoney.com/pingzhongdata/000001.js
4. 基金信息2:http://fund.eastmoney.com/f10/tsdata_'+code+'.html'，同上
5. 基金经理信息:http://fundf10.eastmoney.com/jjjl_'+code+'.html',同上





(2)基金净值数据
http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=377240
http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=160220&page=1
http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=160220&page=1&per=50
http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=377240&page=1&per=20&sdate=2017-03-01&edate=2017-03-01




格式：var apidata={ content:"<table class='w782 comm lsjz'><thead><tr><th class='first'>净值日期</th><th>单位净值</th><th>累计净值</th><th>日增长率</th><th>申购状态</th><th>赎回状态</th><th class='tor last'>分红送配</th></tr></thead><tbody><tr><td>2017-03-01</td><td class='tor bold'>2.1090</td><td class='tor bold'>2.1090</td><td class='tor bold red'>0.29%</td><td>开放申购</td><td>开放赎回</td><td class='red unbold'></td></tr></tbody></table>",records:1,pages:1,curpage:1};

格式化以后：
净值日期	单位净值	累计净值	日增长率	申购状态	赎回状态	分红送配
2017-03-01	2.1090	2.1090			0.29%		开放申购	开放赎回





(3)基金增幅排名
http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=zzf&st=desc&sd=2016-03-29&ed=2017-03-29&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.6370068000914493
ft： fund type类型 所有-all 股票型-gp 混合型-hh 债券型-zq 指数型-zs 保本型-bb QDII-qdii LOF-lof


更多筛选
http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=3yzf,50&gs=0&sc=3yzf&st=desc&sd=2016-03-29&ed=2017-03-29&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.013834315347261095
http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=6yzf,20&gs=0&sc=6yzf&st=desc&sd=2016-03-29&ed=2017-03-29&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.5992681832027366
http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=1nzf,20&gs=0&sc=1nzf&st=desc&sd=2016-03-29&ed=2017-03-29&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.6093838416906625

rs=3yzf,50 近3月涨幅排名前50
rs=1nzf,20 近1年涨幅排名前20

##############基金公司
http://fund.eastmoney.com/company/default.html


############## 经理的资质
序号	姓名	所属公司	现任基金	累计从业时间	现任基金资产总规模	现任基金最佳回报
1	艾定飞	华商基金	共2只:华商电子行业量化华商计算机行业量	1年又327天	11.07亿元	55.60%
2	艾小军	国泰基金	共24只:国泰黄金ETF联国泰黄金ETF联更多>	6年又280天	503.13亿元	136.11%
http://fund.eastmoney.com/manager/#dt14;mcreturnjson;ftall;pn50;pi1;scabbname;stasc

############## 基金评级
http://fund.eastmoney.com/data/fundrating.html
