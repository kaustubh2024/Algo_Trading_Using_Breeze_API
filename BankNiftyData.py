import pandas as pd
from breeze_connect import BreezeConnect

app_key = "00IV422652arJ5788Q57i53Pz3SCZ6V6"
secret_key = "g22`35oFT9^45104737s`30822p5%1b8"
session_token = "36620824"

api = BreezeConnect(api_key=app_key)
api.generate_session(api_secret=secret_key, session_token=session_token)

try:
    data_call = api.get_historical_data(interval="5minute",
                                        from_date="2024-02-01T07:00:00.000Z",
                                        to_date="2024-03-07T07:00:00.000Z",
                                        stock_code="CNXBAN",
                                        exchange_code="NFO",
                                        product_type="options",
                                        expiry_date="2024-03-06T07:00:00.000Z",
                                        strike_price="46200")
    
    call_data = pd.DataFrame(data_call['Success'])
    print(call_data)
    call_data.to_csv('call_data.csv')
except Exception as e:
    print("In Exception")
    print("An error occurred:", e)

data_put = api.get_historical_data(interval="1minute",
                                   from_date="2024-03-01T07:00:00.000Z",
                                   to_date="2024-03-01T07:00:00.000Z",
                                   stock_code="CNXBAN",
                                   exchange_code="NFO",
                                   product_type="options",
                                   expiry_date="2024-03-06T07:00:00.000Z",
                                   strike_price="46200")

put_data = pd.DataFrame(data_put['Success'])
put_data.to_csv('put_data.csv')

"""
Banknifty = api.get_historical_data(interval="5minute",
                                    from_date="2024-02-01T07:00:00.000Z",
                                    to_date="2024-03-08T07:00:00.000Z",
                                    stock_code="CNXBAN",
                                    exchange_code="NSE")

Banknifty_data = pd.DataFrame(Banknifty['Success'])
Banknifty_data.to_csv('Banknifty_march.csv')

"""