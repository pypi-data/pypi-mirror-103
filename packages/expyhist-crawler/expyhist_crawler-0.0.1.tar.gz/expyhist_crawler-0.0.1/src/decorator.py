# -*- coding:utf-8 -*-
#!/usr/bin/env python


import time
import random
import traceback
import sqlite3
from datetime import datetime
from functools import wraps
import pandas as pd


def save_decorator(table_name,database_path,if_exists):
    def decorator(func):
        db_create_time = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
        @wraps(func)
        def wrapper(*args,**kwargs):
            print("=" * 20 + "\n" + func.__name__ + " start saving,time:{}".format(db_create_time))
            print(database_path)
            # connect sqlite3
            conn = sqlite3.connect(database_path)
            try:
                if type(func(*args,**kwargs)) == pd.DataFrame:
                    # get df of copy
                    df = func(*args,**kwargs).copy()
                    df["db_create_time"] = db_create_time
                    # write data to database
                    df.to_sql(name=table_name,con=conn,if_exists=if_exists,index=False)
                    print("save success")
                    time.sleep(random.random() * 10 / 5)
                else:
                    print("result is not DataFrame")
            except:
                print("save fail")
                traceback.print_exc()
            finally:
                # close connection of database
                conn.close()
        return wrapper
    return decorator



if __name__ == "__main__":
    pass
