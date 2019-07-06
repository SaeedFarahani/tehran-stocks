import re
import time

import pandas as pd
import requests

import tehran_stocks.config as db
from tehran_stocks.models import StockPrice, Stocks


def update_stock_price(code):
    try:
        q = f"select dtyyyymmdd as date from stock_price where code = {code}"
        temp = pd.read_sql(q, db.engine)
        url = "http://www.tsetmc.com/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i={}"
        df = pd.read_csv(url.format(code))
        df.columns = [i[1:-1].lower() for i in df.columns]
        df["code"] = code
        df = df[~df.dtyyyymmdd.isin(temp.date)]
        df.to_sql("stock_price", db.engine, if_exists="append", index=False)
        return True, code
    except Exception as e:
        return e, code


def update_group(code):
    stocks = db.session.query(Stocks.code).filter_by(group_code=code).all()
    for i, stock in enumerate(stocks):
        update_stock_price(stock[0])
        print(f"progress: {100*(i+1)/len(stocks):.1f}%", end="\r")