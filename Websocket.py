
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

    token=getTokenInfo("IDEA", "NSE", "EQUITY")
    print(token['TK'])

    #Connect to websocket
    breeze.ws_connect()

    #Callback to receive ticks
    def on_ticks(ticks):
        print("Ticks: {}".format(ticks))
    breeze.on_ticks = on_ticks
    
    print("Token is: " + str(token['TK']))
    #Subscribe to stock feeds by stock-token
    #breeze.subscribe_feeds(stock_token="4.1!{0}".format(str(token['TK'])))
    #stock_token_value = "4.1!{0}".format(str(token['TK']))
    #output_string = breeze.subscribe_feeds(stock_token=stock_token_value)
    # Parse the output string into a list of dictionaries
    #output = [eval(item.strip()) for item in output_string.strip().split("\n")]

    # Convert the list of dictionaries into a DataFrame
    #df = pd.DataFrame(output)

    # Display the DataFrame as a table
    #print(tabulate(df, headers="keys", tablefmt="pretty"))

    # Convert the output to a list of lists or a list of tuples
    #data = [list(row.values()) for row in output]

    # Display the output as a table
    #print(tabulate(data, headers=output[0].keys(), tablefmt="pretty"))

    #breeze.subscribe_feeds(stock_token="4.1!{0}".format(str(token['TK'])))
    #For options
    #breeze.subscribe_feeds(exchange_code="NFO", stock_code="YESBAN", product_type="options", expiry_date="28-Mar-2024", strike_price="25", right="Call", get_exchange_quotes=True, get_market_depth=False)
    #For futures
    breeze.ws_disconnect()
    breeze.subscribe_feeds(exchange_code="NFO", stock_code="INFTEC", product_type="futures", expiry_date="28-Mar-2024", strike_price="", right="others", get_exchange_quotes=True, get_market_depth=False)
    # subscribe stocks feeds by stock-token
    #breeze.subscribe_feeds(stock_token="1.1!532822")
    #breeze.subscribe_feeds(stock_token="4.1!14366")
    while True:
        now = datetime.now()
        if (now.hour >= 15 and now.minute >=30):
            sys.exit()
        sleep(5)
        print("New Iteration")

    