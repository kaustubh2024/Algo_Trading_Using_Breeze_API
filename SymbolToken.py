
from breeze_connect import BreezeConnect
import pandas as pd
import login as l

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

ls = l.tokendf[l.tokendf.EC == "NSE"].NS.unique()
print(ls[0:100])

ls = l.tokendf[l.tokendf.NS == "IDEA"].NS.unique()
print(ls[0:30])

print("Stock Cash Token")
token = getTokenInfo("IDEA", "NSE", "EQUITY")
print(token['SC'])

print("Stock Future Token")
token = getTokenInfo("IDEA", "NFO", "DERIVATIVE")
print(token['SC'])

print("Stock Option Token")
token = getTokenInfo("IDEA", "NFO", "DERIVATIVE")
print(token['SC'])

"""
print("Index Spot")
token = getTokenInfo("NIFTY BANK", "NSE", "EQUITY")
print(token['SC'])
"""
print("Index Future")
token = getTokenInfo("NIFTY BANK", "NFO", "DERIVATIVE")
print(token['TK'])

print("Index Option Token")
token = getTokenInfo("NIFTY BANK", "NFO", "DERIVATIVE")
print(token['SC'])
