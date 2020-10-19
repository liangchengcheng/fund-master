import requests
import pandas as pd
import re
import sys
import math
from frame_net import *
from config_url import *

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