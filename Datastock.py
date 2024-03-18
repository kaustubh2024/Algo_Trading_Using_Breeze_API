from breeze_connect import BreezeConnect
import pandas as pd
import login as l
import hashlib
import hmac
import base64
import time
import datetime

def initializeSymbolTokenMap():
    #Everyday 8:00 AM updated
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
        eq_df = df[(df.EC==exchange) & (df.NS == instrumentName) & (df.SG == instrumentType)]
        return eq_df.iloc[0]
    
breeze = BreezeConnect(api_key=l.api_key)
import urllib
print("https://api.icicidirect.com/apiuser/login?api_key=" + urllib.parse.quote_plus(l.api_key))

print(breeze.generate_session(api_secret=l.api_secret, session_token=l.session_key))
initializeSymbolTokenMap()

print("Stock Cash Token")
token = getTokenInfo("IDEA", "NSE", "EQUITY")
print(token['SC'])
res = breeze.get_historical_data(interval="5minute",
                                   from_date="2024-03-01T07:00:00.000Z",
                                   to_date="2024-03-28T07:00:00.000Z",
                                   stock_code= token['SC'],
                                   exchange_code="NFO",
                                   product_type="",
                                   expiry_date="",
                                   strike_price=""
                                 )

data_items = res['Success']
print(data_items)
dlist = list(data_items)
df = pd.DataFrame(dlist)
print(df)
df.to_csv("cashdata.csv")



print("Stock Future Token")
token=getTokenInfo("IDEA", "NFO", "DERIVATIVE")
print(token)
res = breeze.get_historical_data(interval="5minute",
                                   from_date="2024-01-01T07:00:00.000Z",
                                   to_date="2024-03-01T07:00:00.000Z",
                                   stock_code= token['SC'],
                                   exchange_code="NFO",
                                   product_type="futures",
                                   expiry_date="2024-03-28T07:00:00.000Z",
                                   option_type="others",
                                   strike_price="0"
                                 )

print(res)
print(data_items)
dlist = list(data_items)
df = pd.DataFrame(dlist)
print(df)
df.to_csv("futures.csv")

print("Stock Option Token")
token=getTokenInfo("IDEA", "NFO", "DERIVATIVE")
print(token)
res = breeze.get_historical_data(interval="5minute",
                                   from_date="2024-01-11T07:00:00.000Z",
                                   to_date="2024-03-11T07:00:00.000Z",
                                   stock_code= token['SC'],
                                   exchange_code="NFO",
                                   product_type="options",
                                   expiry_date="2024-03-28T07:00:00.000Z",
                                   option_type="call",
                                   strike_price="0"
                                 )

print(res)
print(data_items)
dlist = list(data_items)
df = pd.DataFrame(dlist)
print(df)
df.to_csv("options.csv")

