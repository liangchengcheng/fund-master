import requests
import pandas as pd
import re
import sys
import math
from frame_net import *
from frame_solve import *
from config_url import *
from config_params import *
from bs4 import BeautifulSoup
import urllib

"""
 下载基金净值的信息
"""

# 20190307 --- 之前爬取历史净值的url失效, 新增爬取逻辑
def get_history_value_new(code, begin, fund_type):
    file_name = "{}_fund_value_{}_{}.csv".format(fund_type, code, DATE_NOW)
    if file_name in os.listdir(VALUE_DIR):
        return

    df_list = []
    for page_num in range(1, 10000):
        fund_url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={}&page={}&per=1000'.format(code, page_num)
        soup = BeautifulSoup(urllib.request.urlopen(url=fund_url), "lxml")
        table = soup.find("table", {"class": "w782 comm lsjz"})
        td_th = re.compile('t[dh]')
        ret_list = []
        for row in table.findAll("tr"):
            cells = row.findAll(td_th)
            row_data = dict()
            if len(cells) == 7:
                row_data[u'净值日期'] = cells[0].find(text=True)
                row_data[u'单位净值'] = cells[1].find(text=True)
                row_data[u'累计净值'] = cells[2].find(text=True)
                row_data[u'日增长率'] = cells[3].find(text=True)
            ret_list.append(row_data)

        ret = pd.DataFrame(ret_list)
        ret.drop(0, inplace=True)
        ret = ret[ret[u'净值日期'].apply(lambda x: 1 if len(str(x).split("-")) == 3 else 0) > 0]
        if ret.shape[0] <= 0:
            break

        ret[u'净值日期'] = pd.to_datetime(ret[u'净值日期'])
        if ret[u'净值日期'].min() <= pd.to_datetime(begin):
            df_list.append(ret[ret[u'净值日期'] >= pd.to_datetime(begin)])
            break
        else:
            df_list.append(ret)
    df_ret = pd.concat(df_list, axis=0)
    print(df_ret.shape)
    df_ret.to_csv(VALUE_DIR + file_name, index=False, encoding='utf-8')
    return
