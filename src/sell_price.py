def calculate(my_order, live_orders):
    live_orders[:] = [order for order in live_orders if order.id != my_order.id]
    if(len(live_orders) == 0):
        return 0
    if(live_orders[0].platinum == live_orders[-1].platinum):
        return live_orders[0].platinum
    for order in live_orders:
        if(order.platinum > live_orders[0].platinum):
            return order.platinum - 1
    return 0

def should_sell(my_order, calculated_sell_price):
    return calculated_sell_price != 0 and calculated_sell_price != my_order.platinum