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
 http://fund.eastmoney.com/manager/default.html?rd=0.3588226733578517#dt14;mcreturnjson;ftall;pn50;pi1;scabbname;stasc
 URL_JJJL = 'http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn=50&sc=abbname&st=asc&pi='
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
        pages = re.findall(r'pages:(.*?),curpage', enddata)[0]
        curpage = re.findall(r'curpage:(.*?)}', enddata)[0]
        arrsysdata = datas[0]
        listdata = eval(arrsysdata)
        for i in range(0, len(listdata)):
            onedata = listdata[i]
            code = onedata[0]
            leng1 = len(onedata)
            va1 = onedata[leng1 -1]
            print("save执行结果：")
            managercode = onedata[0]
            managername = onedata[1]
            companycode = onedata[2]
            companyname = onedata[3]
            fundcodelist = onedata[4]
            fundnamelist = onedata[5]
            workdays = onedata[6]
            dbjjhb = onedata[7]
            ddjjcode = onedata[8]
            ddjjname = onedata[9]
            jjzgm = onedata[10]
            zjhb = onedata[11]
            id = uuid.uuid1()
            sql = "INSERT INTO fund_manager_info(`id`, `managercode`, `managername`, `companycode`, `companyname`, `fundcodelist`, `fundnamelist`, `workdays`, `dbjjhb`, `ddjjcode`, `ddjjname`,  `jjzgm`, `zjhb`) VALUES ('%s','%s','%s','%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                id, managercode, managername, companycode, companyname, fundcodelist, fundnamelist, workdays, dbjjhb, ddjjcode, ddjjname, jjzgm, zjhb)
            print(sql)
            print("save执行结果：" + str(DBUtil.save(dbUtil, sql)))
        curpage = int(curpage) + 1
        if curpage < int(pages):
            download_fund_base_info(str(curpage))