import requests
import pandas as pd
import numpy as np
import re
import sys
import math
from frame_net import *
from config_url import *
from frame_read import *
from frame_solve import *
from frame_sql_2 import *
import uuid
import csv

"""
①: 获取基金的列表
:param url: 基金概况信息的URL - 基金的列表
:return: 将基金统计信息存入当前目录Data/fund_list.csv中,返回基金代码号列表
"""
def get_fund_list():
    url = URL_FUND
    data = {}
    response = get_resonse(url)
    code_list = []
    abbreviation_list = []
    name_list = []
    type_list = []
    name_en_list = []
    tmp = re.findall(r"(\".*?\")", response)
    for i in range(0, len(tmp)):
        if i % 5 == 0:
            code_list.append(eval(tmp[i]))
        elif i % 5 == 1:
            abbreviation_list.append(eval(tmp[i]))
        elif i % 5 == 2:
            name_list.append(eval(tmp[i]))
        elif i % 5 == 3:
            type_list.append(eval(tmp[i]))
        else:
            name_en_list.append(eval(tmp[i]))
    data['code'] = code_list
    data['abbreviation'] = abbreviation_list
    data['name'] = name_list
    data['type'] = type_list
    data['name_en'] = name_en_list
    df = pd.DataFrame(data)
    df.to_csv('data/fund_list.csv', encoding='UTF-8')
    return code_list

"""
① 保存基金的列表到数据库里面去
: fund_info 表
: fund_list.cvs
"""
def save_fund_list():
    dbUtil = DBUtil()
    df = pd.read_csv('data/fund_list.csv', encoding='UTF-8')
    code = {}
    name = {}
    type = {}
    name_en = {}
    for i in range(len(df)):
        code[i] = df["code"][i]
        name[i] = df["name"][i]
        type[i] = df["type"][i]
        name_en[i] = df["name_en"][i]
        id = uuid.uuid1()
        code2 = '%06d' % code[i]
        sql = "INSERT INTO fund_info(`id`, `code`, `name`, `type`, `name_en`) VALUES ('%s', '%s', '%s', '%s', '%s')" % (id, code2, name[i], type[i], name_en[i])
        print(sql)
        print("save执行结果：" + str(DBUtil.save(dbUtil, sql)))

def get_fund_info(code):
    failed_list = []
    data_list = {}
    url = 'http://fund.eastmoney.com/pingzhongdata/'+code+'.js'
    response = get_resonse(url)
    # 爬取失败等待再次爬取
    if response is '':
        return ''
    else:
        strs = re.findall(r'var(.*?);',response)
        for i in range(0, len(strs)):
            tmp = strs[i].split('=')
            var_name = tmp[0].strip()
            data_list[var_name] = [tmp[1]]
        return data_list

"""
:param url: 基金的基本面信息
:return: 将基金统计信息存入当前目录Data/fund_list.csv中,返回基金代码号列表
    股票仓位测算图 ->Data_fundSharesPositions
    Data_netWorthTrend 单位净值走势 equityReturn-净值回报 unitMoney-每份派送金  ->Data_netWorthTrend
    累计净值走势 -> Data_ACWorthTrend
"""
def get_pingzhong_data():
    data = pd.read_csv('data/fund_list.csv', encoding='UTF-8')
    code_list = data['code']
    data = {'fS_name':[],
            'fS_code':[],
            'fund_sourceRate':[]
            ,'fund_Rate':[]
            ,'fund_minsg':[]
            ,'stockCodes':[]
            ,'zqCodes':[]
            ,'syl_1n':[]
            ,'syl_6y':[]
            ,'syl_3y':[]
            ,'syl_1y':[]
            ,'Data_holderStructure':[]
            ,'Data_assetAllocation':[]
            ,'Data_currentFundManager':[]
            ,'Data_buySedemption':[]
            ,'Data_fundSharesPositions':[]
            ,'Data_netWorthTrend':[]
            ,'Data_ACWorthTrend':[]
            }
    failed_list = []
    for i in range(0, len(code_list)):
        code = '%06d' % code_list[i]
        progress = i/len(code_list)*100
        print('爬取'+code+'中，进度', '%.2f'%progress+'%')
        progress_bar(i , len(code_list))
        fund_info = get_fund_info(code)
        if fund_info is '':
            failed_list.append(code)
        else:
            for key in data.keys():
                if key in fund_info.keys():
                    if 'Data' not in key and key != 'zqCodes':
                        data[key].append(eval(fund_info[key][0]))
                    else:
                        data[key].append(fund_info[key][0])
                else:
                    data[key].append('')
    df = pd.DataFrame(data)
    df.to_csv('data/crawler3.csv', encoding='UTF-8')
    df_fail = pd.DataFrame(failed_list)
    df_fail.to_csv('data/fail.csv', encoding='UTF-8')

def solve_pingzhong_data():
    df = pd.read_csv('data/crawler3.csv', encoding='UTF-8')
    data_list = {}
    # 经理信息
    data_list['基金经理'] = []
    data_list['经理工作时间'] = []
    data_list['经理管理基金size'] = []
    # 占净比
    data_list['股票占净比'] = []
    data_list['债券占净比'] = []
    data_list['现金占净比'] = []
    data_list['净资产'] = []
    data_list['categories1']=[]
    # 买卖信息
    data_list['期间申购'] = []
    data_list['期间赎回'] = []
    data_list['总份额']=[]
    data_list['categories2']=[]
    # 比例信息
    data_list['机构持有比例']=[]
    data_list['个人持有比例']=[]
    data_list['内部持有比例']=[]
    data_list['categories3']=[]
    # 占净比信息
    tmp = df['Data_assetAllocation']
    for i in range(0,len(tmp)):
        strs = re.findall(r'\"data\":(.*?),\"',tmp[i])
        t = re.findall(r'\"categories\":(.*?)}',tmp[i])
        if len(strs)==4:
            data_list['股票占净比'].append(strs[0])
            data_list['债券占净比'].append(strs[1])
            data_list['现金占净比'].append(strs[2])
            data_list['净资产'].append(strs[3])
        else:
            strs = re.findall(r'\"data\":(.*?)\}',tmp[i])
            data_list['股票占净比'].append(strs[0])
            data_list['债券占净比'].append(strs[1])
            data_list['现金占净比'].append(strs[2])
            data_list['净资产'].append('')
            t = t[0].split(',"series":')
        if len(t)>0:
            data_list['categories1'].append(t[0])
        else:
            data_list['categories1'].append('')
    del df['Data_assetAllocation']

    # 买卖信息
    tmp = df['Data_buySedemption']
    if len(tmp) > 0:
        for i in range(0, len(tmp)):
            print(i)
            current = tmp[i]
            if pd.isnull(current):
                data_list['期间申购'].append('')
                data_list['期间赎回'].append('')
                data_list['总份额'].append('')
                data_list['categories2'].append('')
            else:
                print("0")
                strs = re.findall(r'\"data\":(.*?)}',tmp[i])
                t = re.findall(r'\"categories\":(.*?)}',tmp[i])
                if len(strs)>0:
                    data_list['期间申购'].append(strs[0])
                    data_list['期间赎回'].append(strs[1])
                    data_list['总份额'].append(strs[2])
                else:
                    data_list['期间申购'].append('')
                    data_list['期间赎回'].append('')
                    data_list['总份额'].append('')
                if len(t)>0:
                    data_list['categories2'].append(t[0])
                else:
                    data_list['categories2'].append('')
        del df['Data_buySedemption']

    # 经理信息
    tmp = df['Data_currentFundManager']
    for i in range(0,len(tmp)):
        name = re.findall(r'\"name\":(.*?),',tmp[i])
        workTime = re.findall(r'\"workTime\":(.*?),',tmp[i])
        fundSize = re.findall(r'\"fundSize\":(.*?),',tmp[i])
        if len(workTime)>0:
            data_list['经理工作时间'].append(eval(workTime[0]))
        else:
            data_list['经理工作时间'].append('')
        if len(name) > 0:
            data_list['基金经理'].append(name[0])
        else:
            data_list['基金经理'].append('')
        if len(fundSize) > 0:
            data_list['经理管理基金size'].append(eval(fundSize[0]))
        else:
            data_list['经理管理基金size'].append('')
    del df['Data_currentFundManager']

    # 比例信息
    tmp = df['Data_holderStructure']
    for i in range(0,len(tmp)):
        strs = re.findall(r'\"data\":(.*?)\}',tmp[i])
        t = re.findall(r'\"categories\":(.*?)}',tmp[i])
        if len(strs)>0:
            data_list['机构持有比例'].append(strs[0])
            data_list['个人持有比例'].append(strs[1])
            data_list['内部持有比例'].append(strs[2])
        else:
            data_list['机构持有比例'].append('')
            data_list['个人持有比例'].append('')
            data_list['内部持有比例'].append('')
        if len(t)>0:
            data_list['categories3'].append(t[0])
        else:
            data_list['categories3'].append('')
    del df['Data_holderStructure']
    df2 = pd.DataFrame(data_list)
    df = pd.concat([df,df2],axis=1)
    df.to_csv('data/data.csv', encoding='UTF-8')


def download_f10_ts_data():
    data = pd.read_csv('data/fund_list.csv', encoding='UTF-8')
    code_list = data['code']
    for i in range(0,len(code_list)):
        progress_bar(i,len(code_list))
        name = '%06d' % code_list[i]
        url = 'http://fund.eastmoney.com/f10/tsdata_'+name+'.html'
        file_name = 'Data/f10_ts/'+name+'.json'
        response = get_resonse(url)
        with open(file_name, 'w', encoding='utf-8') as f:
            print(response, file =f)


def solve_f10_data():
    rootDir = 'data/f10_ts/'
    org_data_list = data_read(rootDir)[0]
    data_list = {}
    data_list['基金号'] = []
    data_list['近1年std']=[]
    data_list['近2年std']=[]
    data_list['近3年std']=[]
    data_list['近1年夏普率'] = []
    data_list['近2年夏普率'] = []
    data_list['近3年夏普率'] = []

    for i in range(0,len(org_data_list)):
        content = org_data_list[i]
        a = re.findall(r'<td class=\'num\'>(.*?)</td>', content)
        if len(a)>0:
            data_list['近1年std'].append(a[0])
            data_list['近2年std'].append(a[1])
            data_list['近3年std'].append(a[2])
            data_list['近1年夏普率'].append(a[3])
            data_list['近2年夏普率'].append(a[4])
            data_list['近3年夏普率'].append(a[5])
            a = re.findall(r'tsdata_(.*?).htm',org_data_list[i])
            code = '%06d' % int(a[0])
            data_list['基金号'].append(code)
    df = pd.DataFrame(data_list, index=data_list['基金号'])
    df.to_csv('data/f10_ts_end/stdAndSharpRatio.csv', encoding='UTF-8')


def download_risk_info():
    data = pd.read_csv('data/fund_list.csv', encoding='UTF-8')
    code_list = data['code']
    for i in range(0, len(code_list)):
        progress_bar(i, len(code_list))
        name = '%06d' % code_list[i]
        url = 'http://fund.eastmoney.com/'+name+'.html'
        file_name = 'data/risk/'+name+'.json'
        response = get_resonse(url)
        with open(file_name, 'w', encoding='utf-8') as f:
            print(response, file =f)


