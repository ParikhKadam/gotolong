from breeze_connect import BreezeConnect

import json
import hashlib
from datetime import datetime
import http.client
import sys

if len(sys.argv) < 4:
    print ('args ', sys.argv)

    sys.exit(1)

your_api_key = sys.argv[1]
your_secret_key = sys.argv[2]
your_api_session = sys.argv[3]

# default for gotolong-localhost
if your_api_key == "1":
    your_api_key="D7T4594=608421)4Q46)20a6476vc536"
if your_secret_key == "2":
    your_secret_key="8h3C35`e4qa3551R19yF9e38893M62g0"

print ('api_key ' + your_api_key)
print ('secret_key ' + your_secret_key)
print ('api_session ' + your_api_session)

# Initialize SDK
breeze = BreezeConnect(api_key=your_api_key)

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
import urllib
print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(your_api_key))

# App related Secret Key
# your_secret_key="8h3C35`e4qa3551R19yF9e38893M62g0"

# 'body' is the request-body of your current request
# payload = json.dumps(body, separators=(',', ':'))


# Generate Session
breeze.generate_session(api_secret=your_secret_key,
                        session_token=your_api_session)

get_demat_holdings = False

if get_demat_holdings:

    # Get Demat Holding details of your account.
    data_json = breeze.get_demat_holdings()

    print('Status : ', data_json['Status'])
    print('Error : ', data_json['Error'])

    stock_records = data_json['Success']

    print ('Total stock records : ', len(stock_records))

    for stock in stock_records:
        print(stock['stock_code'], stock['stock_ISIN'], stock['quantity'])


get_portfolio_holdings = True

if get_portfolio_holdings:
    for exchange_code in ["BSE", "NSE"]:

        # Get Portfolio Holding details of your account.
        data_json = breeze.get_portfolio_holdings(exchange_code="NSE")

        print('Status : ', data_json['Status'])
        print('Error : ', data_json['Error'])

        stock_records = data_json['Success']

        print ('Total stock records : ', len(stock_records))
        dumped_once = False 
        for stock in stock_records:
            if not dumped_once:
                dumped_once = True 
                print(stock)

            print(stock['stock_code'], stock['quantity'], stock['average_price'], stock['current_market_price'])


get_customer_details = True
if get_customer_details:
    # customer information - begin
    data_json = breeze.get_customer_details(api_session=your_api_session)
    print(data_json)
    # customer information - end


sys.exit(1)

#time_stamp & checksum generation for request-headers
time_stamp = datetime.utcnow().isoformat()[:19] + '.000Z'
checksum = hashlib.sha256((time_stamp+payload+secret_key).encode("utf-8")).hexdigest()



# Generate ISO8601 Date/DateTime String
import datetime
iso_date_string = datetime.datetime.strptime("21/03/2022","%d/%m/%Y").isoformat()[:10] + 'T05:30:00.000Z'
iso_date_time_string = datetime.datetime.strptime("21/03/2022 23:59:59","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'

# Following are the complete list of API method:

# Get Customer details by api-session value.
get_customer_details(api_session="your_api_session")


# Get Funds details of your account.
breeze.get_funds()
