from breeze_connect import BreezeConnect
from tabulate import tabulate
import pandas as pd
import login as l
import numpy as np
from datetime import datetime
from time import time, sleep
import sys
import threading
import warnings

def initializeSymbolTokenMap():
    #Every Day at 8:00 AM updated
    tokendf =pd.read_csv('https://traderweb.icicidirect.com/Content/File/txtFile/ScripFile/StockScriptNew.csv')
    l.tokendf = tokendf
    print(tokendf)

def getTokenInfo (instrumentName, exchange, instrumentType, Segment="", strike=0, optionType='', expiry=''):

    # for Cash Stock
    if instrumentType == 'EQUITY':
        df = l.tokendf
        eq_df = df[(df.EC==exchange) & (df.NS == instrumentName) & (df.SG == instrumentType)]
        return eq_df.iloc[0]
    
    # for Stock Future
    if instrumentType == 'DERIVATIVE':
        df = l.tokendf
        stockfuture = df[(df.EC==exchange) & (df.NS == instrumentName) & (df.SG == instrumentType)]
        return stockfuture.iloc[0]
    
breeze = BreezeConnect(api_key=l.api_key)
import urllib
print("https://api.icicidirect.com/apiuser/login?api_key=" + urllib.parse.quote_plus(l.api_key))

print(breeze.generate_session(api_secret=l.api_secret, session_token=l.session_key))
initializeSymbolTokenMap()
print(breeze.get_funds())

print("Index Option Token")
token=getTokenInfo("IDEA", "NFO", "DERIVATIVE")
print(token)
res = breeze.get_historical_data(interval="5minute",
                                 from_date="2024-03-01T07:00:00.000Z",
                                 to_date="2024-03-12T07:00:00.000Z",
                                 stock_code="IDECEL",
                                 exchange_code="NFO",
                                 product_type="options",
                                 expiry_date="2024-03-28T07:00:00.000Z",
                                 right="call",
                                 strike_price="14"
                                 )
print(res)
df=pd.DataFrame(res['Success'])
if not df.empty:
    print(df)
    print(df.iloc[-1])
else:
    print("DataFrame is empty")

df.to_csv("Historical_Option_Data.csv")
