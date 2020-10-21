import requests
import pandas as pd
import re
import sys
import math
from frame_net import *
from config_url import *
import json
import uuid
from frame_sql_2 import *

"""
获取基金公司的列表信息
:param url: 公司信息的URL
:return: 将结果存储在当前目录data/company_list.csv中
"""
def get_company_list():
    url = URL_COMPANY
    response = get_resonse(url)
    code_list = []
    name_list = []
    # 对数据进行处理
    tmp = re.findall(r"(\".*?\")", response)
    for i in range(0,len(tmp)):
        if i % 2 == 0:
            code_list.append(tmp[i])
        else:
            name_list.append(tmp[i])

    data = {}
    data['code']=code_list
    data['name']=name_list
    df = pd.DataFrame(data)
    df.to_csv('data/company_list.csv', encoding='UTF-8')


"""
② 
获取基金公司的列表信息 并且保存到数据库里去
http://fund.eastmoney.com/company/default.html
"""
def get_all_company_list():
    dbUtil = DBUtil()
    data_list = {}
    url = URL_COMPANY_ALL
    response = get_resonse(url)
    # 爬取失败等待再次爬取
    if response is '':
        return ''
    else:
        if response is '':
            return ''
        else:
            response = response + ";"
            strs = re.findall(r'var(.*?);', response)
            for i in range(0, len(strs)):
                tmp = strs[i].split('=')
                var_name = tmp[0].strip()
                data_list[var_name] = [tmp[1]]

        keydata = data_list["json"]
        enddata = keydata[0]
        datas = re.findall(r'datas:(.*?)}', enddata)
        arrsysdata = datas[0]
        listdata = eval(arrsysdata)
        for i in range(0, len(listdata)):
            onedata = listdata[i]
            code = onedata[0]
            name = onedata[1]
            createtime = onedata[2]
            fundcount = onedata[3]
            frdb = onedata[4]
            enname = onedata[5]
            gm = onedata[7]
            pj = onedata[8]
            simplename = onedata[9]
            datatime = onedata[11]
            id = uuid.uuid1()
            sql = "INSERT INTO fund_company_info(`id`, `code`, `name`, `createtime`, `fundcount`, `frdb`, `enname`, `gm`, `pj`, `simplename`, `datatime`) VALUES ('%s','%s','%s','%s', '%s','%s', '%s', '%s', '%s', '%s', '%s')" % (
            id, code, name, createtime, fundcount, frdb, enname, gm, pj, simplename, datatime)
            print(sql)
            print("save执行结果：" + str(DBUtil.save(dbUtil, sql)))

