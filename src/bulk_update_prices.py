import json
import logging
import time
import src.request as request
import src.sell_price as sell_price
from src.order import Order

base_url = "https://api.warframe.market"
jwt_token = request.get_jwt_token()
my_orders = []
logs_file = "logs.txt"
with open(logs_file, "w") as f:
    pass
logging.basicConfig(
    filename=logs_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def get_auth_token():
    with open('credentials.json', 'r') as credentials:
        data = json.load(credentials)

    response = request.post(logging, base_url+"/v1/auth/signin", {"Authorization": jwt_token}, data).headers["Authorization"]
    logging.info("Logged in")
    logging.info("---------------------------------------------------------------")
    return response
    
headers = {
    "Cookie": get_auth_token().replace("JWT ", "JWT="),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json"
}

def full_url(path):
    return base_url+path

def populate_my_orders():
    my_raw_orders = request.get(logging, full_url("/v2/orders/my"), headers)
    for raw_order in my_raw_orders:
        order = Order(raw_order)
        my_orders.append(order)
    return True

def retrieve_live_orders(my_order):
    live_orders = []
    raw_live_orders = request.get(logging, full_url("/v2/orders/item/"+my_order.item_id+"/top"), headers)
    if(raw_live_orders == False):
        return False
    raw_live_orders = raw_live_orders.get("sell")
    for index, raw_order in enumerate(raw_live_orders):
        order = Order(raw_order)
        live_orders.append(order)
        logging.info("Live order "+str(index)+": "+order.toString())
    return live_orders

def calculate_update_order(my_order, live_orders, current_index, my_orders_len):
    print_log = str(current_index+1) +"/"+str(my_orders_len)+" | "+"Current order: "+my_order.toString()
    calculated_sell_price = sell_price.calculate(my_order, live_orders)
    logging.info("Calculated price: "+str(calculated_sell_price)+" | Current Price: "+str(my_order.platinum))
    should_sell = sell_price.should_sell(my_order, calculated_sell_price)
    if(should_sell):
        request.patch(logging, full_url("/v2/order/"+my_order.id), headers, {
            "platinum":calculated_sell_price
        })
        print(print_log+" | Price updated:"+str(my_order.platinum)+" -> "+str(calculated_sell_price))
    else:
        logging.info("Calculated Price 0 or not changed, not updating order")
        print(print_log)
    logging.info("---------------------------------------------------------------")
    return should_sell


def update_my_order_prices(my_order, current_index, my_orders_len):
    logging.info("***Current order: "+my_order.toString()+"***")

    live_orders = function_interval(retrieve_live_orders, my_order)
    function_interval(calculate_update_order, my_order, live_orders, current_index, my_orders_len)

def function_interval(function, *args):
    start_time = time.perf_counter()
    res = function(*args)
    interval = 0 if res == False else 0.34
    elapsed_time = time.perf_counter() - start_time
    sleep_time = interval - elapsed_time
    if(sleep_time > 0):
        time.sleep(sleep_time)
    return res

def main():
    function_interval(populate_my_orders)
    my_orders_len = len(my_orders)
    for index, order in enumerate(my_orders):
        update_my_order_prices(order, index, my_orders_len)

    # update_my_order_prices(my_orders[0], index, my_orders_len)