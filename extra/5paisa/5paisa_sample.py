import json
import pprint
import readchar
import threading
import time
import websocket
import winsound
import schedule
import ta
import pandas as pd
import numpy as np
from tapy import Indicators
from py5paisa import FivePaisaClient
from py5paisa.order import Order, OrderType, Exchange, AHPlaced
from datetime import date
from datetime import timedelta
from ta.volume import VolumeWeightedAveragePrice

# 5paisa Sample from Ganesh Hegde - IIMB Friend.
# keys.conf file - in same location where the code is present
#
# [KEYS]
# APP_NAME=<provided_by_5paisa>
# APP_SOURCE=<provided_by_5paisa>
# USER_ID=<provided_by_5paisa>
# PASSWORD=<provided_by_5paisa>
# USER_KEY=<provided_by_5paisa>
# ENCRYPTION_KEY=<provided_by_5paisa>
# user=<user_provided>
# pass=<user_provided>
# dob=<user_provided>

pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None

user = ''
passwd = ''
birthdate = ''
PRINTHEADER = True

client = FivePaisaClient(email=user, passwd=passwd, dob=birthdate)


def show_help():
    print("\n")
    print("a - authenticate")
    print("b - buy")
    print("c - check login")
    print("h - holdings")
    print("o - order book")
    print("m - margins")
    print("p - positions")
    print("s - sell")
    print("t - trade book")
    print("q - quit!\n")


def print_datastream(jsondata):
    # print(jsondata)
    global CURRENT_PRICE
    global PRINTHEADER
    try:
        columns = ['Token', 'Time', 'LastRate', 'High', 'Low', 'OpenRate', 'PClose', 'TotalQty']
        df = pd.DataFrame(jsondata, columns=columns)
        prevprice = CURRENT_PRICE
        CURRENT_PRICE = df.iloc[-1, 2]
        print(df.to_string(header=PRINTHEADER, index=True), end="\r")
        PRINTHEADER = False
    except Exception:
        print('Look at this exception')


# copied from py5paisa
def streming_data(wsPayload: dict):
    web_url = f'wss://openfeed.5paisa.com/Feeds/api/chat?Value1={client.Jwt_token}|{client.client_code}'
    auth = client.Login_check()

    def on_message(ws, message):
        print_datastream(json.loads(message))
        # check_trade()

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("Streaming Stopped")

    def on_open(ws):
        ws.send(json.dumps(wsPayload))

    ws = websocket.WebSocketApp(web_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                cookie=auth)
    ws.run_forever()


def stream_price(id, type):
    # Extype - segment type
    req_list = [
        {
            "Exch": EXCHANGE,
            "ExchType": EXTYPE,
            "ScripCode": SCRIPCODE
        }, ]
    # mf - market feed
    # s - subscribe
    dict1 = client.Request_Feed('mf', 's', req_list)
    streming_data(dict1)


def getprice_history(timeperiod, duration):
    global M15_BARS
    global DAY_BARS
    today = date.today()
    yesterday = today - timedelta(days=duration)
    dh = client.historical_data(EXCHANGE,
                                EXTYPE,
                                SCRIPCODE,
                                timeperiod,
                                yesterday,
                                today)  # BANKNIFTY 29 JULY 2021
    if timeperiod == '1d':
        DAY_BARS = dh
    else:
        M15_BARS = dh


def print_history():
    print(M15_BARS)


def print_marketfeed(jsondata):
    # print (jsondata)
    columns = ['Token', 'Time', 'TimeStamp', 'LastRate', 'PClose', 'High', 'Low', 'TotalQty', ]
    df = pd.DataFrame(jsondata['Data'], columns=columns)
    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], format='%Y-%m-%dT%H:%M:%S')
    # CURRENT_PRICE = df['LastRate'] #Save this tick price to hit buy
    print(df)


def price_feed():
    req_list_ = [
        {
            "Exch": EXCHANGE,
            "ExchType": EXTYPE,
            "Symbol": "NIFTY 01 JUL 2021 CE 15800.00",
            "Expiry": "20210701",
            "StrikePrice": "15800",
            "OptionType": "CE"
        }, ]
    return client.fetch_market_feed(req_list_)


def getprice_marketfeed(stockid, stocktype):
    print("stock price : ")
    while (True):
        pf = price_feed()
        print_marketfeed(pf)
        time.sleep(15)


def getprice_datastream():
    thread = threading.Thread(target=stream_price,
                              args=("stockid", "stocktype"),
                              daemon=True)
    thread.start()


def refresh_data():
    getprice_history('15m', 2)


def schedule_datafetch(a):
    refresh_data()
    schedule.every(3).minutes.do(refresh_data)
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_bars():
    thread = threading.Thread(target=schedule_datafetch, args=('a'), daemon=True)
    thread.start()


def login():
    client.login()


def check_login():
    client.Login_check()


def show_holdings():
    print(client.holdings())


def show_margin():
    print(client.margin())


def show_position():
    print('POSITION :', client.positions())


def show_orderbook():
    print(client.order_book())


def buy_scrip():
    test_order = Order(
        order_type=BUY,
        exchange=EXCHANGE,
        exchange_segment=EXTYPE,
        scrip_code=SCRIPCODE,
        quantity=QUANTITY,
        price=CURRENT_PRICE,
        is_intraday=True,
        atmarket=False,
        ahplaced='Y')
    print('BUY :', test_order.scrip_code, test_order.quantity, test_order.price)
    show_position()


def sell_scrip():
    print('SELL :', SCRIPCODE, QUANTITY, CURRENT_PRICE)
    show_position()


def beep():
    winsound.Beep(440, 250)
    return False


# Main logic starts here
# NSE - BSE SCRIP CODE
# get the code through scripmaster
# sharekhan - tradetiger - name and code ...
# Is this ISIN -? - no ?
#
SCRIPCODE = 53179  # 224570 silver 53179 banknifty july 29
EXCHANGE = 'N'  # M - MCX , N - NSE
EXTYPE = 'D'
BUY = 'B'
SELL = 'S'
CURRENT_PRICE = 0
QUANTITY = 25
CALLOPTION = 'BANKNIFTY 01 Jul 2021 CE 35400.00'
PUTOPTION = 'BANKNIFTY 01 Jul 2021 PE 35400.00'
M15_BARS = []
DAY_BARS = []
PPTRADITIONAL = []
PPFIBONACE = []
ALLIGATOR_JAW = 0
SUPERTREND = True
TRADE = 'NO'
INTRADE = False
TRADE_PRICE = 0.0


def main():
    login()
    getpivotpoints()
    refresh_data()
    # strategy
    vwap(M15_BARS)
    getprice_datastream()
    schedule.every(3).minutes.do(refresh_data)
    while True:
        schedule.run_pending()
        time.sleep(1)

        check_trade()

        # print('action : ', end='', flush=True)
        run = readchar.readkey()
        print(run)

        if (run == 'a'):
            login()

        elif (run == 'b'):
            buy_scrip()

        elif (run == 'c'):
            check_login()

        elif (run == 'h'):
            show_holdings()

        elif (run == 'm'):
            show_margin()

        elif (run == 'p'):
            show_position()

        elif (run == 's'):
            sell_scrip()

        elif (run == 'o'):
            show_orderbook()

        elif (run == '?'):
            show_help()

        elif (run == '\r'):
            global PRINTHEADER
            PRINTHEADER = True
            refresh_data()

        elif (run == 'q'):
            print("exiting...")
            break
        else:
            show_help()


if __name__ == "__main__":
    main()
