import requests
import pandas as pd
import re
import sys
import math
from frame_net import *
from frame_solve import *
from config_url import *

"""
 下载基金经理的信息 这个是采用解析html标签的形式
"""
def download_manager_info():
    data = pd.read_csv('data/fund_list.csv', encoding='UTF-8')
    code_list = data['code']
    for i in range(0, len(code_list)):
        progress_bar(i, len(code_list))
        name = '%06d' % code_list[i]
        url = 'http://fundf10.eastmoney.com/jjjl_'+name+'.html'
        file_name = 'data/manager/' + name + '.json'
        response = get_resonse(url)
        with open(file_name, 'w', encoding='utf-8') as f:
            print(response, file = f)
"""
 解析基金经理的信息
"""
def solve_manager_info():
    rootDir = 'data/manager/'
    org_data_list = data_read(rootDir)[0]
    name_list = []
    manager_info_list={'name':[],'code':[]}
    for i in range(0, len(org_data_list)):
        data_list = {'姓名':[], '上任日期':[],'经理代号':[],'简介':[], '基金名称':[],'基金代码':[],'基金类型':[],'起始时间':[],'截止时间':[],'任职天数':[],'任职回报':[],'同类平均':[],'同类排名':[]}
        # 姓名
        a = re.findall(r'姓名(.*?)<div class="space10"></div>', org_data_list[i])
        for ii in range(0, len(a)):
            b = a[ii]
            name = re.findall(r'\">(.*?)</a></p><p><strong>', b)[0]
            if name not in name_list:
                name_list.append(name)
                duty_date = re.findall(r'上任日期：</strong>(.*?)</p>', b)[0]
                brief_intro = re.findall(r'</p><p>(.*?)</p><p class="tor">', b)[0].split('<p>')[-1]
                # manager_code = re.findall(r'"http://fund.eastmoney.com/manager/(.*?).html',b)[0]
                data_list['姓名'].append(name)
                data_list['上任日期'].append(duty_date)
                data_list['经理代号'].append('无')
                data_list['简介'].append(brief_intro)
                fund_info_list = re.findall(r'html\"(.*?)</tr>', b)[1:]

                # manager list
                manager_info_list['name'].append(name)
                manager_info_list['code'].append('manager_code')

                for iii in range(0, len(fund_info_list)):
                    fund_list = re.findall(r'>(.*?)</td>' or r'>(.*?)</a></td>',fund_info_list[iii])
                    fund_list[0] = fund_list[0].split('<')[0]
                    fund_list[1] = re.findall(r'>(.*?)<', fund_list[1])[0]
                    data_list['基金名称'].append(fund_list[1])
                    data_list['基金代码'].append(fund_list[0])
                    data_list['基金类型'].append(fund_list[2])
                    data_list['起始时间'].append(fund_list[3])
                    data_list['截止时间'].append(fund_list[4])
                    data_list['任职天数'].append(fund_list[5])
                    data_list['任职回报'].append(fund_list[6])
                    data_list['同类平均'] .append(fund_list[7])
                    data_list['同类排名'] .append(fund_list[8])
                    if iii>0:
                        data_list['姓名'].append('')
                        data_list['上任日期'].append('')
                        data_list['经理代号'].append('')
                        data_list['简介'].append('')
                dir = 'data/managerSlv/'+name+'.csv'
                df = pd.DataFrame(data_list)
                order = ['姓名','上任日期','经理代号','简介','基金名称','基金代码','基金类型','起始时间','截止时间','任职天数','任职回报','同类平均','同类排名']
                df = df[order]
                df.to_csv(dir, encoding='UTF-8')
    df_manager_info_list = pd.DataFrame(manager_info_list)
    df_manager_info_list.to_csv('Data/manager.csv', encoding='UTF')
