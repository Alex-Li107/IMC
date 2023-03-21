#This is an improvement on 1.2. 
# begin to implement a moving average of the last 250 prices.
from datamodel import OrderDepth, TradingState, Order
from typing import Dict, List

dyn_avg = 50
askHistory = {'PEARLS': [], 'BANANAS': []}
bidHistory = {'PEARLS': [], 'BANANAS': []}
avg_ask_history = {'PEARLS': 0, 'BANANAS': 0}
avg_bid_history = {'PEARLS': 0, 'BANANAS': 0}
class Trader: 

    

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        limits = {'PEARLS': 20, 'BANANAS': 20}
        products  = ['PEARLS', 'BANANAS']
        result = {}
        timestamp = state.timestamp
        if(timestamp == 0):
            print("timestamp,product,buy_amount,buy_volume,ask_amount,ask_volume")
        print(",skip")

        for product in products:
            if product not in state.position.keys():
                position = 0
            else:
                position = state.position[product]
            limit = limits[product]

            #check if PEARLS
            if product  == 'PEARLS':
                
                
                
                #retrieve market orders 
                order_depth: OrderDepth = state.order_depths[product]

                #initialize orders to be sent
                orders: list[Order] = []

                #check for SELL orders
                if len(order_depth.sell_orders) > 0:

                    #sort available sell orders by price 
                    #select only sell price with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    (askHistory[product]).append(best_ask)
                    if len(askHistory[product]) > dyn_avg: 
                        askHistory[product].pop(0)
                    avg_ask_history[product] = sum(askHistory[product]) / dyn_avg

                    

                #check for BUY orders
                if len(order_depth.buy_orders) > 0:

                    #sort available buy orders by price
                    #select buy price with highest price
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]

                    bidHistory[product].append(best_bid)
                    if len(bidHistory[product]) > dyn_avg: 
                        bidHistory[product].pop(0)
                    avg_bid_history[product] = sum(bidHistory[product]) / dyn_avg

                acceptable_price = (avg_bid_history[product] + avg_ask_history[product]) / 2


                if (len(askHistory[product]) == dyn_avg and len(bidHistory[product]) == dyn_avg): 
                    #SELL ORDERS 

                    #check if we have enough limit space to complete this order
                    if position - best_ask_volume > limit:
                        #best_bid_volume = -limit-position
                        best_ask_volume = position - limit

                    #check if the lowest ask (sell order) is lower than the above fair value
                    if best_ask < acceptable_price:
                        #print("BUY PEARLS", str(-best_ask_volume) + "x", best_ask)
                        #print(str(timestamp)+ ";" + product + ";", str(best_ask) + ";", str(best_ask_volume) + ";;")
                        orders.append(Order(product, best_ask, -best_ask_volume))

                    #BUY ORDERS 

                    #check if we have enough limit space to complete this order
                    #if best_bid_volume > -(limit + position):
                    if position - best_bid_volume < -limit:
                        #best_bid_volume = -limit-position
                        best_bid_volume = limit+position

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

                #check for SELL orders
                if len(order_depth.sell_orders) > 0:

                    #sort available sell orders by price 
                    #select only sell price with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    (askHistory[product]).append(best_ask)
                    if len(askHistory[product]) > dyn_avg: 
                        askHistory[product].pop(0)
                    avg_ask_history[product] = sum(askHistory[product]) / dyn_avg

                    

                #check for BUY orders
                if len(order_depth.buy_orders) > 0:

                    #sort available buy orders by price
                    #select buy price with highest price
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]

                    bidHistory[product].append(best_bid)
                    if len(bidHistory[product]) > dyn_avg: 
                        bidHistory[product].pop(0)
                    avg_bid_history[product] = sum(bidHistory[product]) / dyn_avg

                acceptable_price = (avg_bid_history[product] + avg_ask_history[product]) / 2


                if (len(askHistory[product]) == dyn_avg and len(bidHistory[product]) == dyn_avg): 
                    #SELL ORDERS 

                    #check if we have enough limit space to complete this order
                    if position - best_ask_volume > limit:
                        #best_bid_volume = -limit-position
                        best_ask_volume = position - limit

                    #check if the lowest ask (sell order) is lower than the above fair value
                    if best_ask < acceptable_price:
                        #print("BUY PEARLS", str(-best_ask_volume) + "x", best_ask)
                        #print(str(timestamp)+ ";" + product + ";", str(best_ask) + ";", str(best_ask_volume) + ";;")
                        orders.append(Order(product, best_ask, -best_ask_volume))

                    #BUY ORDERS 

                    #check if we have enough limit space to complete this order
                    #if best_bid_volume > -(limit + position):
                    if position - best_bid_volume < -limit:
                        #best_bid_volume = -limit-position
                        best_bid_volume = limit+position

                    if best_bid > acceptable_price: 
                        #print("SELL PEARLS", str(best_bid_volume) + "x", best_bid)
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
                        if trade.buyer == "SUBMISSION":
                            print(str(trade.timestamp) + "," + trade.symbol + "," + str(trade.quantity) + "," + str(trade.price) + ",," )
                        if trade.seller == "SUBMISSION":
                            print(str(trade.timestamp) + "," + trade.symbol + ",,," + str(trade.quantity) + "," + str(trade.price))

        return result