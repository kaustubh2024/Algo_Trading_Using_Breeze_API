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

if __name__ == '__main__':
    breeze = BreezeConnect(api_key=l.api_key)
    print(breeze.generate_session(api_secret=l.api_secret, session_token=l.session_key))
    initializeSymbolTokenMap()

    token=getTokenInfo("IDEA", "NFO", "DERIVATIVE")
    print(token['SC'])

    while(True):

        print("Option Quote:")
        res = breeze.get_quotes(
            stock_code=token['SC'],
            exchange_code="NFO",
            product_type="options",
            expiry_date="2024-03-28T07:00:00.000Z",
            right="call",
            strike_price="13"
        )
        data_items = res['Success']
        dlist = list(data_items)
        df = pd.DataFrame(dlist)
        if not df.empty:
            print(df.iloc[0])
        else:
            print("DataFrame is empty")
            
        sleep(5)

        print("Future Quote:")
        res = breeze.get_quotes(
            stock_code=token['SC'],
            exchange_code="NFO",
            product_type="futures",
            expiry_date="2024-03-28T07:00:00.000Z",
            right="",
            strike_price=""
        )
        data_items1 = res['Success']
        dlist1 = list(data_items1)
        df1 = pd.DataFrame(dlist1)
        if not df1.empty:
            print(df1.iloc[0])
        else:
            print("DataFrame1 is empty")
