import login as l

#intialize keys

#api_key = "INSERT_YOUR _APP_KEY_HERE"
#api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
#api_session = 'INSERT_YOUR_API_SESSION_HERE'



# Define Contract
#stock = 'IDEA',
#strike = '17750',
#expiry = '2023-04-20T06:00:00.000Z',      
#right = 'call',
stock = 'IDEA'
strike = '13'


# Import Libraries
from datetime import datetime
from time import time, sleep
from breeze_connect import BreezeConnect

# Setup my API keys 
api = BreezeConnect(api_key=l.api_key)
api.generate_session(api_secret=l.api_secret,session_token=l.session_key)

api.set_funds(transaction_type="credit", amount="30", segment="Equity")
print("\n************\n")
print("Updated balance is: ")
print(api.get_funds())
print("\n************\n")



# Place order
buy_order = api.place_order(stock_code=stock,
                            exchange_code="NSE",
                            product="cash",
                            action='buy',
                            order_type='market',
                            stoploss="",
                            quantity="2",
                            price="",
                            validity="day",
                            #validity_date=today,
                            disclosed_quantity="0",
                            #expiry_date=expiry,
                            #right=right,
                            #strike_price=strike
                            )

# Store Order ID
order_id = buy_order['Success']['order_id']

# Get current price
price = api.get_quotes(stock_code=stock,
                exchange_code="NFO",
                product_type="options",
                #expiry_date=expiry,
                #right=right,
                strike_price=strike
                )

# Get the buy price of order
cost = float(api.get_order_detail('nfo',order_id)['Success'][0]['average_price'])
trailing_stoploss = round(cost * 0.95,1)

# Run Loop
while(True):

    if(price > cost * 1.10):
        cost = price
        trailing_stoploss = round(cost * 0.95,1)

    elif(price < cost):

        # Place square off order 
        sq_off_order = api.square_off(exchange_code="NSE",
                    product="cash",
                    stock_code=stock,
                    #expiry_date=expiry,
                    #right=right,
                    strike_price=strike,
                    action='sell',
                    order_type="market",
                    validity="day",
                    stoploss="",
                    quantity="2",
                    price="0",
                    validity_date=datetime.now().strftime('%Y-%m-%dT06:00:00.000Z')  ,
                    trade_password="",
                    disclosed_quantity="0")


        if(sq_off_order['Status']==200) : 
            print(sq_off_order)


        break

    sleep(2)