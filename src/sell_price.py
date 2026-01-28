def calculate(my_order, live_orders):
    live_orders[:] = [order for order in live_orders if order.id != my_order.id]
    if(len(live_orders) == 0):
        return 0
    if(live_orders[0].platinum == live_orders[-1].platinum):
        return live_orders[0].platinum
    
    # set as 2nd smallest order if exists (2nd place -1 plat)
    # for order in live_orders:
    #     if(order.platinum > live_orders[0].platinum):
    #         return order.platinum - 1

    # do not update price
    # return 0

    # if last order is bigger than before last order
    if(len(live_orders) > 1 and live_orders[-1].platinum > live_orders[-2].platinum):
        # set as last top order (last order -1 plat)
        return live_orders[-1].platinum - 1
    
    # set as equal to last top order
    return live_orders[-1].platinum

def should_sell(my_order, calculated_sell_price):
    return calculated_sell_price != 0 and calculated_sell_price != my_order.platinum