import requests
import pandas as pd
import re
import sys
import math
from frame_net import *
from frame_solve import *
from config_url import *
import uuid
from frame_sql_2 import *

"""
 下载基金基本信息
"""
def download_fund_base_info(page):
    dbUtil = DBUtil()
    data_list = {}
    url = URL_JJJL + page
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

        keydata = data_list["returnjson"]
        enddata = keydata[0]
        datas = re.findall(r'data:(.*?),record', enddata)
        pages = re.findall(r'pages:(.*?),curpage', enddata)
        curpage = re.findall(r'curpage:(.*?)}', enddata)
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