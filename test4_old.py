import yfinance as yf
from curl_cffi import requests
import pandas as pd
import sqlite3
import numpy as np


def update_stock_sql(s_code):
#    s_code="BX"
    session=requests.Session(impersonate="chrome")
    s_ticker=yf.Ticker(s_code,session=session)
    h_data=s_ticker.history(period='1d',interval="1d")
    c_price=h_data[['Close']].values.tolist()
    try:
        close_price=c_price[0][0]
    except:
        print(h_data)

    try:
        print(close_price)
    except:
        print(c_price)
        close_price=0
        print("close price error")
    return close_price


con = sqlite3.connect("stock.db")
cur = con.cursor()
cur.execute(f"SELECT name FROM corp")

# 結果セットを取得
data = cur.fetchall()

df1=np.array(data)
df1=df1.tolist()


#株価の更新
for ii in df1:
    print(ii[0])
    xx=update_stock_sql(ii[0])
    xx=round(xx,2)
    print(xx)
    cur.execute(f"update corp set price={xx} where name='{ii[0]}'")
    con.commit()



#保有株式数の更新
for ii in df1:
    print(ii[0])
    cur.execute(f"select sum(num) from trade where name='{ii[0]}' and trade='buy'")
    jj=cur.fetchone()
    print(jj)
    cur.execute(f"select sum(num) from trade where name='{ii[0]}' and trade='sell'")
    kk=cur.fetchone()
    print(kk)
    if kk[0] is None:
        ll=jj[0]
    else:
        ll=jj[0]-kk[0]
    print(ll)
    if ll is None:
        nn=0;
    else:
        cur.execute(f"update corp set stock_num={ll} where name='{ii[0]}'")
        con.commit()
        cur.execute(f"select sum(cost) from (select cost from trade where name='{ii[0]}' and trade='buy' order by date DESC limit {ll})")
        mm=cur.fetchone()
        print(mm,'is mm')
        if ll is 0:
            nn=0
        elif mm[0] is None:
            nn=0
        else:
            nn=abs(float(mm[0]))
            nn=round(nn,2)
            
    cur.execute(f"update corp set stock_cost={nn} where name='{ii[0]}'")
    con.commit()


# 接続を閉じる
con.close()
