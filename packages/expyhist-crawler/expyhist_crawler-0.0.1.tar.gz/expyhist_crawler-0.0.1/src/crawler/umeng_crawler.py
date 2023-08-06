# -*- coding:utf-8 -*-
# !/usr/bin/env python

import os
import sys
sys.path.append(os.path.abspath(".."))

import aop
import aop.api

import pandas as pd
from datetime import datetime, timedelta

if "config.ini" in os.listdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))):
    from src.setting import APIKEY, APISECURITY, APPKEYS

class UMengScrapy():

    def __init__(self):

        # 设置网关域名
        aop.set_default_server('gateway.open.umeng.com')

        # 设置apiKey和apiSecurity
        aop.set_default_appinfo(APIKEY, APISECURITY)

        # 设置appkey
        self.appkeys = APPKEYS

    def get_durations(self, app_key: str, date: str) -> pd.DataFrame:

        # 构造Request和访问协议是否是https
        req = aop.api.UmengUappGetDurationsRequest()

        # 发起Api请求
        try:
            resp = req.get_response(None, appkey=app_key, date=date, statType="daily")
            df = pd.DataFrame.from_dict(resp["durationInfos"])
            return df
        except aop.ApiError as e:
            # Api网关返回的异常
            print(e)
        except aop.AopError as e:
            # 客户端Api网关请求前的异常
            print(e)
        except Exception as e:
            # 其它未知异常
            print(e)

    def get_durations_result(self, date: str) -> pd.DataFrame:
        try:
            df = pd.concat([self.get_durations(i, date) for i in self.appkeys])
            return df.groupby(["name",df.index])["value"].sum().reset_index().sort_values(by="level_1")
        except Exception as e:
            print(e)

    def get_monthly_active_user(self, app_key: str, start_date: str, end_date:str) -> pd.DataFrame:

        # 构造Request和访问协议是否是https
        req = aop.api.UmengUappGetActiveUsersRequest()

        # 发起Api请求
        try:
            resp = req.get_response(None, appkey=app_key, startDate=start_date, endDate=end_date, periodType="monthly")
            df = pd.DataFrame.from_dict(resp["activeUserInfo"])
            return df
        except aop.ApiError as e:
            # Api网关返回的异常
            print(e)
        except aop.AopError as e:
            # 客户端Api网关请求前的异常
            print(e)
        except Exception as e:
            # 其它未知异常
            print(e)

    def get_monthly_active_user_result(self, start_date: str, end_date:str) -> pd.DataFrame:
        try:
            df = pd.concat([self.get_monthly_active_user(i, start_date, end_date) for i in self.appkeys])
            return df.groupby("date")["value"].sum().reset_index()
        except Exception as e:
            print(e)

    def get_monthly_launches(self, app_key: str, start_date: str, end_date:str) -> pd.DataFrame:

        # 构造Request和访问协议是否是https
        req = aop.api.UmengUappGetLaunchesRequest()

        # 发起Api请求
        try:
            resp = req.get_response(None, appkey=app_key, startDate=start_date, endDate=end_date, periodType="monthly")
            df = pd.DataFrame.from_dict(resp["launchInfo"])
            return df
        except aop.ApiError as e:
            # Api网关返回的异常
            print(e)
        except aop.AopError as e:
            # 客户端Api网关请求前的异常
            print(e)
        except Exception as e:
            # 其它未知异常
            print(e)

    def get_monthly_launches_result(self, start_date: str, end_date: str):
        try:
            df = pd.concat([self.get_monthly_launches(i, start_date, end_date) for i in self.appkeys])
            return df.groupby("date")["value"].sum().reset_index()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # 当日时间的月份1号
    first_date = datetime.now().date().replace(day=1)
    # 当日时间的上个月份最后一天
    end_date = first_date - timedelta(days=1)
    # 当日时间的上个月份1号
    start_date = end_date.replace(day=1)

    print(UMengScrapy().get_durations_result(end_date))
    print(UMengScrapy().get_monthly_active_user_result(start_date,end_date))
    print(UMengScrapy().get_monthly_launches_result(start_date, end_date))
