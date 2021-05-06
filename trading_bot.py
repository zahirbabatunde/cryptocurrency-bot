import time
import sys
from luno_python.client import Client

# CONSTANTS
# bitcoin account id
btc_account_id = '7228890115215648289'

# api key id
key_id = 'gswyyk6q6sye9'

# api key secret
key_secret = 'JvvuHXeLwpp_clC4uvJBMbw0z7kEFSLZgMLhG6A0_6w'

# delay to fetch order list
order_fetch = 15

# delay to limit call frequency
wait = 4

# interested currency pairs
curr_pairs = 'XBTNGN'

# rate to buy or sell
buy_rate = 0.987
sell_rate = 1.013

# connect to the client's profile
c = Client(api_key_id=key_id, api_key_secret=key_secret)


def main():
    while True:
        try:
            orders = c.list_orders(pair=curr_pairs)
            time.sleep(order_fetch)

            # SELL CONDITION MET
            if orders['orders'][0]['state'] == 'COMPLETE':

                # the rate of bitcoin to naira for the most recent transaction
                s_limit_price = float(orders['orders'][0]['limit_price'])

                # amount of bitcoin to sell or buy in btc unit
                s_volume = round(20000 / s_limit_price, 6)

                # price at which it should be sold
                s_sell_price = round(s_limit_price * sell_rate)

                # price at which it should be bought
                s_buy_price = round(s_limit_price * buy_rate)

                # place buy order if previous sell condition was met
                try:
                    time.sleep(wait)
                    c.post_limit_order(pair=curr_pairs, type='BID', volume=s_volume, price=s_buy_price)
                    time.sleep(wait)
                except Exception as e:
                    print(e)
                    sys.exit()

                # place sell order if previous sell condition was met
                try:
                    time.sleep(wait)
                    c.post_limit_order(pair=curr_pairs, type='ASK', volume=s_volume, price=s_sell_price)
                    time.sleep(wait)
                except Exception as e:
                    print(e)
                    sys.exit()

                # stop the previous buy order if previous sell condition was met
                try:
                    time.sleep(wait)
                    c.stop_order(orders['orders'][1]['order_id'])
                    time.sleep(wait)
                except Exception as e:
                    print(e)

                # combined wallet value
                print('Stock was sold.\nTotal Balance :', get_total_balance())

            orders = c.list_orders(pair=curr_pairs)
            time.sleep(order_fetch)

            # BUY CONDITION MET
            if orders['orders'][1]['state'] == 'COMPLETE':

                # the rate of bitcoin to naira for the most recent transaction
                b_limit_price = float(orders['orders'][1]['limit_price'])

                # amount of bitcoin to sell or buy in btc unit
                b_volume = round(20000 / b_limit_price, 6)

                # price at which it should be sold
                b_sell_price = round(b_limit_price * sell_rate)

                # price at which it should be bought
                b_buy_price = round(b_limit_price * buy_rate)

                # place buy order if previous buy condition was met
                try:
                    time.sleep(wait)
                    c.post_limit_order(pair=curr_pairs, type='BID', volume=b_volume, price=b_buy_price)
                    time.sleep(wait)
                except Exception as e:
                    print(e)
                    sys.exit()

                # place sell order if previous sell condition was met
                try:
                    time.sleep(wait)
                    c.post_limit_order(pair=curr_pairs, type='ASK', volume=b_volume, price=b_sell_price)
                    time.sleep(wait)
                except Exception as e:
                    print(e)
                    sys.exit()


                # stop the previous sell order if previous buy condition was met
                try:
                    time.sleep(wait)
                    c.stop_order(orders['orders'][0]['order_id'])
                    time.sleep(wait)
                except Exception as e:
                    print(e)

                # combined wallet value
                print('Stock was bought.\nTotal Balance :', get_total_balance())

        except Exception as e:
            print(e)

        time.sleep(wait)


def get_total_balance():
    try:
        ngn_balance = round(float(c.get_balances('NGN')['balance'][0]['balance']), 2)
        xbt_balance = float(c.get_balances('XBT')['balance'][0]['balance'])
        ticker = float(c.get_ticker('XBTNGN')['last_trade'])
        total_balance = round(float(ticker * xbt_balance) + ngn_balance)
        time.sleep(wait)
        return total_balance

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

