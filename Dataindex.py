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
        stockfuture = df[(df.EC==exchange) & (df.NS == instrumentName) & (df.SG == instrumentType)]
        return stockfuture.iloc[0]
    
"""
def getTokenInfo(instrumentName, exchange, instrumentType, Segment="", strike=0, optionType='', expiry=''):
    print("Inside getTokenInfo(). instrumentType is: " + instrumentType )
    print("Inside getTokenInfo(). instrumentName is: " + instrumentName )
    print("Inside getTokenInfo(). exchange is: " + exchange )
    
    
    # for Cash Stock
    if instrumentType == 'EQUITY':
        df = l.tokendf
        #print("Token ID is: " + df)
        print("df.EC is: " + df.EC)
        print("df.NS is: " + df.NS)
        print("df.SG is: " + df.SG)
                
        eq_df = df[(df.EC == exchange) & (df.NS == instrumentName) & (df.SG == instrumentType)]
        print("eq_df: ", eq_df)  # Add this line for debugging
        return eq_df.iloc[0]
    
    # for Stock Future
    if instrumentType == 'DERIVATIVE':
        df = l.tokendf
        stockfuture = df[(df.EC == exchange) & (df.NS == instrumentName) & (df.SG == instrumentType)]
        print("stockfuture: ", stockfuture)  # Add this line for debugging
        return stockfuture.iloc[0]
    
    else:
        print("Not matching any if condition")
        print("Inside getTokenInfo(). instrumentType is: " + instrumentType )
        print("Inside getTokenInfo(). instrumentName is: " + instrumentName )
        print("Inside getTokenInfo(). exchange is: " + exchange )
"""
        
breeze = BreezeConnect(api_key=l.api_key)
import urllib
print("https://api.icicidirect.com/apiuser/login?api_key=" + urllib.parse.quote_plus(l.api_key))

print(breeze.generate_session(api_secret=l.api_secret, session_token=l.session_key))
initializeSymbolTokenMap()
print(breeze.get_funds())

"""
print("Index Spot")
token = getTokenInfo("NIFTY BANK", "BSE", "EQUITY")
print(token)
res = breeze.get_historical_data(interval="5minute",
                                   from_date="2024-03-01T07:00:00.000Z",
                                   to_date="2024-03-28T07:00:00.000Z",
                                   stock_code= token['SC'],
                                   exchange_code="BSE",
                                   product_type="",
                                   expiry_date="",
                                   option_type="",
                                   strike_price=""
                                 )

data_items = res['Success']


dlist = list(data_items)
df = pd.DataFrame(data_items)
print(df)
df.to_csv("indexspotdata.csv")
"""

print("Index Futures")
token = getTokenInfo("NIFTY BANK", "NFO", "DERIVATIVE")
print(token['SC'])
res = breeze.get_historical_data(interval="5minute",
                                   from_date="2024-03-01T07:00:00.000Z",
                                   to_date="2024-03-28T07:00:00.000Z",
                                   stock_code= token['SC'],
                                   exchange_code="NFO",
                                   product_type="",
                                   expiry_date="2024-03-28T07:00:00.000Z",
                                   option_type="others",
                                   strike_price=""
                                 )

data_items = res['Success']

dlist = list(data_items)
df = pd.DataFrame(dlist)
print(df)
df.to_csv("indexfuturesdata.csv")

print("Index Options")
token = getTokenInfo("NIFTY BANK", "NFO", "DERIVATIVE")
print(token['SC'])
res = breeze.get_historical_data(interval="5minute",
                                   from_date="2024-03-01T07:00:00.000Z",
                                   to_date="2024-03-28T07:00:00.000Z",
                                   stock_code= token['SC'],
                                   exchange_code="NFO",
                                   product_type="",
                                   expiry_date="2024-03-28T07:00:00.000Z",
                                   option_type="call",
                                   strike_price=""
                                 )

data_items = res['Success']

dlist = list(data_items)
df = pd.DataFrame(dlist)
print(df)
df.to_csv("indexoptionsdata.csv")
