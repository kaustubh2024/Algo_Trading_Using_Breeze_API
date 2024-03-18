
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

print("\n\n\n*********\n\n\n")
#funds = breeze.get_funds()
#print("Total funds are: " + str(funds))
print(breeze.get_funds())
#customer_details = breeze.get_customer_details(l.session_key)
#print(customer_details)

#print(breeze.get_demat_holdings())

print("\n\n\n*********\n\n\n")

#print("\nStock Equity Order\n")
token=getTokenInfo("IDEA", "NSE", "EQUITY")
print("\n\n\n*****Current funds...*****")
print(breeze.get_funds())
#print(token['SC'])
print("\n\n\n*****Reducing funds...*****")
breeze.set_funds(transaction_type="debit", amount="280", segment="Equity")
print(breeze.get_funds())
"""
print("\n\n\n ****** Placing order now...*******")

orderid = breeze.place_order(stock_code=token['SC'],
                                   exchange_code="NSE",
                                   product="cash",
                                   action="buy",
                                   order_type="limit",
                                   price="13.85",
                                   stoploss="",
                                   quantity="2",
                                   validity="day",
                                   user_remark="My Algo Trading"
                                 )
print(orderid)
print("\n\n\nAvailable funds now are: \n\n\n")
print(breeze.get_funds())
"""

"""
print("Stock Future Order")
token=getTokenInfo("IDEA", "NFO", "DERIVATIVE")
print(token)
orderid = breeze.place_order(stock_code=token['SC'],
                                   exchange_code="NFO",
                                   product_type="futures",
                                   action="buy",
                                   order_type="market",
                                   stop_loss="13",
                                   quantity=str(token['LS']),
                                   price=0,
                                   validity="day",
                                   validity_date="2024-03-12T07:00:00.000Z",
                                   disclosed_quantity="0",
                                   expiry_date="2024-03-28T07:00:00.000Z",
                                   right="others",
                                   strike_price="0",
                                   user_remark="Kaustubh's Algo Trading"
                                 )
print(orderid)


print("Stock Option Order")
token=getTokenInfo("IDEA", "NFO", "DERIVATIVE")
print(token)
orderid = breeze.place_order(stock_code=token['SC'],
                                   exchange_code="NFO",
                                   product_type="options",
                                   action="buy",
                                   order_type="limit",
                                   stop_loss="13",
                                   quantity=str(token['LS']),
                                   price=0,
                                   validity="day",
                                   validity_date="2024-03-12T07:00:00.000Z",
                                   disclosed_quantity="0",
                                   expiry_date="2024-03-28T07:00:00.000Z",
                                   right="call",
                                   strike_price="14",
                                   user_remark="Kaustubh's Algo Trading"
                                 )
print(orderid)
"""