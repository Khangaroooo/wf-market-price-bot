import src.bulk_update_prices
import src.request

#WIP untested
def main():
    user_input = input("Please enter orderId to delete: ")
    src.request.delete(src.bulk_update_prices.base_url+"/v2/order/"+user_input, src.bulk_update_prices.headers)

if __name__ == "__main__":
    main()