# This is my first Algorithm for the Tutorial Round
# I will only be trying to get this to work and get an idea for how things work
# Note there are only two products in this round : Pearls Bananas
from datamodel import OrderDepth, TradingState, Order
from typing import Dict, List

class Trader: 

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        timestamp = state.timestamp
        if(timestamp == 0):
            print("timestamp;product;buy_amount;buy_volume;ask_amount;ask_volume")
        print(";skip")
        for product in state.order_depths.keys():

            # check if PEARLS
            if product == 'PEARLS':
                
                # retrieve market orders
                order_depth: OrderDepth = state.order_depths[product]

                # initialize orders to be sent
                orders: list[Order] = []

                # define a fair value for PEARLS
                acceptable_price = 10000

                # check for SELL orders
                if len(order_depth.sell_orders) > 0:

                    #sort available sell orders by price 
                    #select only sell price with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    #check if the lowest ask (sell order) is lower than the above fair value
                    if best_ask < acceptable_price:
                        #print("BUY PEARLS", str(-best_ask_volume) + "x", best_ask)
                        #print(str(timestamp)+ ";" + product + ";", str(best_ask) + ";", str(best_ask_volume) + ";;")
                        orders.append(Order(product, best_ask, -best_ask_volume))

                # check for BUY orders
                if len(order_depth.buy_orders) > 0:

                    #sort available buy orders by price
                    #select buy price with highest price
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.sell_orders[best_ask]

                    if best_bid > acceptable_price: 
                        #print("SELL PEARLS", str(best_bid_volume) + "x", best_bid)
                        #print(str(timestamp)+ ";" + product + ";;;", str(best_bid) + ";", str(best_bid_volume))
                        orders.append(Order(product, best_bid, -best_bid_volume))

                result[product] = orders
            #check if BANANAS
            if product  == 'BANANAS':
                
                #retrieve market orders 
                order_depth: OrderDepth = state.order_depths[product]

                #initialize orders to be sent
                orders: list[Order] = []

                #define a fair value for BANANAS
                acceptable_price = 4898

                #check for SELL orders
                if len(order_depth.sell_orders) > 0:

                    #sort available sell orders by price 
                    #select only sell price with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    #check if the lowest ask (sell order) is lower than the above fair value
                    if best_ask < acceptable_price:
                        #print("BUY BANANAS", str(-best_ask_volume) + "x", best_ask)
                        #print(str(timestamp)+ ";" + product + ";", str(best_ask) + ";", str(best_ask_volume) + ";;")
                        orders.append(Order(product, best_ask, -best_ask_volume))

                #check for BUY orders
                if len(order_depth.buy_orders) > 0:

                    #sort available buy orders by price
                    #select buy price with highest price
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.sell_orders[best_ask]

                    if best_bid > acceptable_price: 
                        #print("SELL BANANAS", str(best_bid_volume) + "x", best_bid)
                        #print(str(timestamp)+ ";" + product + ";;;", str(best_bid) + ";", str(best_bid_volume))
                        orders.append(Order(product, best_bid, -best_bid_volume))

                result[product] = orders
            
            #Implement a backtest csv system
        own_trades = state.own_trades
            #positions = state.position

        for trade_key in own_trades:
            trades = own_trades[trade_key]
            if len(trades) > 0:
                for trade in trades: 
                    if trade.timestamp == timestamp - 100:
                        print("symbol " + trade.symbol + " price ", str(trade.price) + " quantity ", str(trade.quantity) + " timestamp ", str(trade.timestamp))
                # if len(own_trades[product] > 0):
                 #   print("TEST")
                    #for trade in own_trades[product]:
                     #   print("price", str(trade.price) + "quantity", str(quantity) + "timestamp", str(trade.timestamp))
        return result