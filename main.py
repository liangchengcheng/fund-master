# !/usr/bin/python
# -*- coding: utf-8 -*-
from info_company import *
from info_fund import *
from info_manager import *
from info_fund_jjjz import *
from info_all import *

if __name__ == '__main__':
    print("开始获取基金公司的列表的数据信息")
    # get_company_list()
    # save_fund_list()
    # get_company_list()
    # get_all_company_list()
    print("结束获取基金公司的列表的数据信息")

    print("开始获取基金的列表的数据信息")
    # get_fund_list()
    print("结束获取基金的列表的数据信息")

    print("开始获取基金的经理列表的数据信息")
    # download_manager_info()
    # solve_manager_info()
    print("结束获取基金的经理列表的数据信息")
    print("开始获取基金的经理列表的数据信息")


    print("---")
    # get_pingzhong_data()
    # solve_pingzhong_data()



    print("std和夏普比率信息处理")
    # download_f10_ts_data()
    # solve_f10_data()

    # download_risk_info()

    # download_fund_jingzhi_info()

    download_fund_base_info('1')