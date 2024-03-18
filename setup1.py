from breeze_connect import BreezeConnect
import pandas as pd
import login as l

def initializeSymbolTokenMap():
    tokendf =pd.read_csv('https://traderweb.icicidirect.com/Content/File/txtFile/ScripFile/StockScriptNew.csv')
    print(tokendf)

breeze = BreezeConnect(api_key=l.api_key)

breeze.generate_session(api_secret=l.api_secret, session_token=l.session_key)

print(breeze.get_funds())

customer_details = breeze.get_customer_details()
print(customer_details)

initializeSymbolTokenMap()

