# -*- coding:utf-8 -*-
#!/usr/bin/env python

import requests
import json
import pandas as pd
from datetime import datetime, time
from src.setting import USER_AGENT, APP_DF, SLEEP_TIME
import time

class AppRankScrapy():

    def __init__(self):

        self.rank_url = "https://api.qimai.cn/app/rank"
        self.appinfo_url = "https://api.qimai.cn/app/appinfo"

        self.headers = {
            "User-Agent": USER_AGENT,
            "referer": "https://www.qimai.cn/",
            "origin": "https://www.qimai.cn"
        }

    # 获取appid对应的rank
    def get_rank(self, app_id : str, analysis : str) -> pd.DataFrame:
        try:
            params = {
                "analysis": analysis,
                "appid": app_id,
                "country": "cn",
                "brand": "free",
                "day": "0",
                "appRankShow": "1",
                "subclass": "all",
                "simple": "1",
                "type": "1",
                "rankEchartType": "0",
                "rankType": "day"
            }
            r = requests.get(url=self.rank_url, params=params, headers=self.headers)
            time.sleep(SLEEP_TIME)
            # rank
            rank = json.loads(r.text)["realTimeRank"][1][1]["ranking"]
            special_rank = json.loads(r.text)["realTimeRank"][1][2]["ranking"]
            rank_df = pd.DataFrame(
                dict(app_id=[app_id], rank=[rank], special_rank=[special_rank]
                     , create_time=[datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            )
        except Exception as e:
            rank_df = pd.DataFrame(
                dict(app_id=[app_id], rank=["-"], special_rank=["-"]
                     , create_time=[datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            )
            print("appid:" + app_id + " can't get rank")

        return rank_df

    # 获取appid对应的appname
    def get_appinfo(self, app_id : str, analysis : str) -> pd.DataFrame:

        try:
            params = {
                "analysis": analysis,
                "appid": app_id,
                "country": "cn"
            }
            r = requests.get(url=self.appinfo_url, params=params, headers=self.headers)
            time.sleep(SLEEP_TIME)
            # appname
            app_name = json.loads(r.text)["appInfo"]["appname"]
            appinfo_df = pd.DataFrame(
                dict(app_id=[app_id], app_name=[app_name], create_time=[datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            )
        except Exception as e:
            appinfo_df = pd.DataFrame(
                dict(app_id=[app_id], app_name=["-"], create_time=[datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            )
            print("appid:" + app_id + " can't get appinfo")

        return appinfo_df

    # 合并rank和appname
    def get_result(self,*args) -> pd.DataFrame:
        # 定义一个大于if-elise局部的变量
        result_df = None
        # 遍历appid和analysisi参数
        rank_df = pd.concat([self.get_rank(app_id=i, analysis=j) for i,j in
                             zip(APP_DF["app_id"].to_list(),APP_DF["rank_analysis"].to_list())])

        appinfo_df = pd.concat([self.get_appinfo(app_id=i, analysis=j) for i, j in
                             zip(APP_DF["app_id"].to_list(),APP_DF["appinfo_analysis"].to_list())])
        # 将两个df结果合并成一个df
        if len(args) == 2:
            result_df = pd.merge(args[0],args[1],on="app_id",how="left")
        else:
            result_df = pd.merge(appinfo_df,rank_df[["app_id","rank","special_rank"]],on="app_id",how="left")

        return result_df

if __name__ == "__main__":
    test = AppRankScrapy()
    print(test.get_result())
