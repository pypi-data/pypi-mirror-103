# -*- coding:utf-8 -*-
#!/usr/bin/env python

import requests
import json, re
import pandas as pd
from datetime import datetime,timedelta


def title_scrapy() -> pd.DataFrame:

    df = pd.DataFrame(
        dict(
            catg=["中间bar", "中间bar", "金象任务", "金象任务", "果园", "果园", "果园", "签到", "签到", "签到"],
            urls=["https://m.fenxianglife.com/fms/100004/552812/index.html",
                  "https://m.fenxianglife.com/fms/100004/3e0704/index.html"
                , "https://m.fenxianglife.com/fms/100004/bebf44/index.html",
                  "https://m.fenxianglife.com/fms/100004/8ceb00/index.html"
                , "https://m.fenxianglife.com/fms/100004/74a2e9/index.html",
                  "https://m.fenxianglife.com/fms/100004/5e7254/index.html"
                , "https://m.fenxianglife.com/fms/100004/0a7d50/index.html",
                  "https://m.fenxianglife.com/fms/100004/584d90/index.html"
                , "https://m.fenxianglife.com/fms/100004/e9aad0/index.html",
                  "https://m.fenxianglife.com/fms/100004/6f4eb4/index.html"]
        )
    )
    titles = []

    for i in df["urls"]:
        r = requests.get(url=i)
        r.encoding = "utf-8"
        title = re.findall(r"<title>(.*?)</title>", r.text)[0]
        titles.append(title)

    df["titles"] = titles

    return df

def user_scrapy(show_start_date : str) -> pd.DataFrame:

    today = datetime.now().date()

    params = {
        "appCode":"744b3a88c9974680982cc5b6612a4e92",
        "start_date":"2020-12-01",
        "end_date": str(today),
        # "show_start_date": show_start_date,
        # "show_end_date": str(datetime.strptime(show_start_date,"%Y-%m-%d").date()+timedelta(days=1)),
        "pageNum":"1",
        "pageSize":"5000",
    }

    r = requests.get(url="http://yunyingdaping.fenxianglife.com/self/table",params=params)
    df = pd.read_json(json.dumps(json.loads(r.text)["data"]["rows"]),"records")

    return df




if __name__ == "__main__":

    yesterday = str(datetime.now().date()-timedelta(days=1))
    today = str(datetime.now().date())

    date_range = pd.date_range(start=yesterday,end=today)
    str_date_range = [i.strftime("%Y-%m-%d") for i in date_range]
    df = pd.concat([user_scrapy(i) for i in str_date_range])

    df.to_excel("C:/Users/YangHua/Desktop/{}自营新用户.xlsx".format(today))
