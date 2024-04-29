import login as l
import json

from datetime import datetime
from time import time, sleep
import sys

# Define Contract
stock = 'IDECEL'
order_id = ""
price = 11.15
cost = 0
trailing_stoploss = 0
order_id = ""
qty = 12500
# Create an empty list to store holding dictionaries
holding_dicts = []


# Import Libraries
from datetime import time
from time import sleep
from breeze_connect import BreezeConnect

# Define the target time
target_time = time(15, 30)  # 3:30 PM
print("\nTarget time is: " + str(target_time) + ".\n")


# Setup my API keys 
api = BreezeConnect(api_key=l.api_key)
api.generate_session(api_secret=l.api_secret,session_token=l.session_key)

def add_funds(amt):
    api.set_funds(transaction_type="credit", amount=amt, segment="Equity")
    print("\n************\n")
    print("Updated balance is: ")
    print(api.get_funds())
    print("\n************\n")

def buy_stock_in_cash(stock_code, qty):
    global order_id
    # Place order
    buy_order = api.place_order(stock_code=stock_code,
                                exchange_code="NSE",
                                product="cash",
                                action='buy',
                                order_type='limit',
                                stoploss="",
                                quantity=qty,
                                price="12.95",
                                validity="day"
                                )
    print("\n*** Printing buy_order ***\n")
    print(buy_order)

    # Store Order ID
    order_id = buy_order['Success']['order_id']
    print("\n*****\n")

    print("Order ID is: " + str(order_id) )

    print("\n****** Order Placed ******\n")

    print("\n*** Order Details ***\n")
    print(api.get_order_detail(exchange_code="NSE",
                            order_id=order_id))
    print("\n*****\n")

    print("\n*** Trade Details ***\n")
    print(api.get_trade_detail(exchange_code="NSE",
                            order_id=order_id))
    print("\n*****\n")


    print(stock, " - *** \n")

# Get current cost
def get_cost(order_id):
    global trailing_stoploss
    global price
    global trailing_stoploss
    # Get the buy price of order
    try:
        cost = float(api.get_order_detail('NSE',order_id)['Success'][0]['average_price'])
        trailing_stoploss = round((cost - 0.05),2)
        price = cost
    except:
        print("\nException while getting the cost price. Cost price set to 0.0\n")
        cost = 0
        trailing_stoploss = cost

    print("\nCost is: " + str(cost))
    return cost

def get_my_portfolio_holdings():
    portfolio = api.get_portfolio_holdings("NSE", "", "", stock, "")
    print(portfolio)

    # Create an empty list to store holding dictionaries
    global holding_dicts

    # Check if portfolio is not empty and contains 'Success' key
    if 'Success' in portfolio:
        holding_list = portfolio['Success']
        if holding_list:
            print("\n*** Portfolio Begins ***\n")
            # Iterate over each holding in the portfolio
            for holding in holding_list:
                # Create a new dictionary for each holding
                holding_dict = {}
                # Populate the dictionary with details of the holding
                holding_dict['stock_code'] = holding['stock_code']
                holding_dict['quantity'] = holding['quantity']
                holding_dict['average_price'] = holding['average_price']
                # Add more details as needed
                # Append the holding dictionary to the list
                holding_dicts.append(holding_dict)
        else:
            print("\nPortfolio is empty.\n")
    else:
        print("\nFailed to fetch portfolio holdings.\n")

    # Print the list of holding dictionaries
    for holding_dict in holding_dicts:
        print(holding_dict)
    print("\n*** Portfolio End ***\n")

    
    # Check if portfolio is not empty and contains 'Success' key
    if 'Success' in portfolio:
        holding_list = portfolio['Success']
        if holding_list:
            print("\nPortfolio Holdings:\n")
            # Iterate over each holding in the portfolio
            for holding in holding_list:
                print("\n")
                print(type(holding))
                print("\n")
                # Print details of each holding
                print("Stock Code:", holding['stock_code'])
                print("Quantity:", holding['quantity'])
                print("Average Price:", holding['average_price'])
                # Add more details as needed

                print("\n")  # Add a newline for better readability between holdings
        else:
            print("\nPortfolio is empty.\n")
    else:
        print("\nFailed to fetch portfolio holdings.\n")

    


if __name__ == '__main__':

    #Connect to websocket
    api.ws_connect()

    # Get portfolio holdings
    print("\nGetting portfolio holdings\n")
    get_my_portfolio_holdings()
    

    add_funds(10)

    # Stock = IDECEL, QTY = 2
    buy_stock_in_cash(stock, qty)

    #quote = api.get_quotes(stock_code=stock,
    #            exchange_code="NSE",
    #            product_type="cash"
    #            )
    #print(quote)
    #price = quote['Success'][0]['ltp']
    #price = quote['Success']['ltp']
    #print("\nCurrent price is: " + str(price))

    print("\n*** Extracting Cost and setting Trailing Stop-loss ***\n")
    cost = float(get_cost(order_id))
    #trailing_stoploss = round((cost - 0.10),2)
    #trailing_stoploss = cost
    print("\nCurrent trailing_stoploss is: " + str(trailing_stoploss))

    # Callback to receive ticks
    def on_ticks(ticks):
        global price
        #print("Ticks: {}".format(ticks['last']))
        #price = quote['Success'][0]['ltp']
        price = ticks.get("last")


    def monitor_stoploss_and_square_off():

        global trailing_stoploss
        # Subscribe stocks feeds
        api.subscribe_feeds(exchange_code="NSE", 
                                stock_code="IDECEL", 
                                product_type="cash", 
                                get_exchange_quotes=True, 
                                get_market_depth=False
                                )
        
        api.on_ticks = on_ticks
        print("\n*** Monitoring live price quotes for stop loss *** \n")
        print ("\n**********\n")
        print ("Price is: " + str(price) + " , Cost is: " + str(cost) + " and trailing stoploss is: " + str(trailing_stoploss) )
        print ("\n**********\n")
        if cost == 0:
            print("\n Cost is 0. It means BUY order was not executed. Exiting...\n")
            # Terminate the program with exit code 1 (indicating an error)
            sys.exit(1)

        #IF Condition 0
        if (price > cost * 1.05):
            # Place square off order 
            print ("Price is: " + str(price) + " , Cost is: " + str(cost) + " and trailing stoploss is: " + str(trailing_stoploss) )
            
            print("\n*** Squaring off at IF condition 0 *** at price: " + str(price) + ".\n")
            # Place sell order
            
            sell_order = api.place_order(stock_code=stock,
                        exchange_code="NSE",
                        product="cash",
                        action='sell',
                        order_type='market',
                        stoploss="",
                        quantity=qty,
                        price="",
                        validity="day"
                        )
            
        if(price < trailing_stoploss - 0.05):
            # Place square off order 
            print ("Price is: " + str(price) + " , Cost is: " + str(cost) + " and trailing stoploss is: " + str(trailing_stoploss) )
            
            print("\n*** Squaring off at IF condition 1 *** at price: " + str(price) + ".\n")
            # Place sell order
            
            sell_order = api.place_order(stock_code=stock,
                        exchange_code="NSE",
                        product="cash",
                        action='sell',
                        order_type='market',
                        stoploss="",
                        quantity=qty,
                        price="",
                        validity="day"
                        )
            
            # Terminate the program with exit code 0
            sys.exit(0)

        if(price < (cost - 0.05)):
            # Place square off order 
            print ("Price is: " + str(price) + " , Cost is: " + str(cost) + " and trailing stoploss is: " + str(trailing_stoploss))
            
            print("\n*** Squaring off at IF condition 2 *** at price: " + str(price) + ".\n")

            # Place sell order
            
            sell_order = api.place_order(stock_code=stock,
                        exchange_code="NSE",
                        product="cash",
                        action='sell',
                        order_type='market',
                        stoploss="",
                        quantity=qty,
                        price="",
                        validity="day"
                        )
            
            # Terminate the program with exit code 0
            sys.exit(0)
        
        elif (price > trailing_stoploss + 0.10):
            trailing_stoploss = round((price - 0.05), 2)
            print("\n*** Revised trailing stoploss to: " + str(trailing_stoploss))

        else:
            print("\nPrice = " + str(price) + " and trailing_stoploss = " + str(trailing_stoploss) + ".\n")

        sleep(2)

    
    #while(True):
    while datetime.now().time() < target_time:
        monitor_stoploss_and_square_off()
        sleep(2)


    print("\n\n\n*** It's now 3:30 PM. Exiting the trading desk ***\n\n\n")
