import os
import json
from pyotp import TOTP
from data import token_lookup

def place_limit_order(instrument_list,ticker,buy_sell,price,quantity,obj, exchange="NSE"):
    params = {
                "variety":"NORMAL",
                "tradingsymbol":"{}-EQ".format(ticker),
                "symboltoken":token_lookup(ticker, instrument_list),
                "transactiontype":buy_sell,
                "exchange":exchange,
                "ordertype":"LIMIT",
                "producttype":"INTRADAY",
                "duration":"DAY",
                "price":price,
                "quantity":quantity
                }
    response = obj.placeOrder(params)
    return response

def place_market_order(instrument_list,ticker,buy_sell,price,quantity,obj, sl=0,sqof=0,exchange="NSE"):
    params = {
                "variety":"NORMAL",
                "tradingsymbol":"{}-EQ".format(ticker),
                "symboltoken":token_lookup(ticker, instrument_list),
                "transactiontype":buy_sell,
                "exchange":exchange,
                "ordertype":"MARKET",
                "producttype":"INTRADAY",
                "duration":"DAY",
                "price":price,
                "quantity":quantity
                }
    response = obj.placeOrder(params)
    return response

def candel_order(order_id, obj):
        params = {
                "variety":"NORMAL",
                "orderid":order_id
                }
        response = obj.cancelOrder(params["orderid"], params["variety"])
        return response
    
def modify_order_type(instrument_list,ticker,order_id,order_type,quantity, obj):
    params = {
                "variety":"NORMAL",
                "orderid":order_id,
                "ordertype":order_type,
                "producttype":"INTRADAY",
                "duration":"DAY",
                "tradingsymbol":"{}-EQ".format(ticker),
                "quantity":quantity,
                "symboltoken":token_lookup(ticker, instrument_list),
                "exchange":"NSE"
                }
    response = obj.modifyOrder(params)
    return response


def place_sl_limit_order(instrument_list,ticker,buy_sell,price,quantity,obj, exchange="NSE"):
    params = {
                "variety":"STOPLOSS",
                "tradingsymbol":"{}-EQ".format(ticker),
                "symboltoken":token_lookup(ticker, instrument_list),
                "transactiontype":buy_sell,
                "exchange":exchange,
                "ordertype":"STOPLOSS_LIMIT",
                "producttype":"INTRADAY",
                "duration":"DAY",
                "price":price+0.05,
                "triggerprice":price,
                "quantity":quantity
                }
    response = obj.placeOrder(params)
    return response

def place_sl_market_order(instrument_list,ticker,buy_sell,price,quantity,obj, sl=0,sqof=0,exchange="NSE"):
    params = {
                "variety":"STOPLOSS",
                "tradingsymbol":"{}-EQ".format(ticker),
                "symboltoken":token_lookup(ticker, instrument_list),
                "transactiontype":buy_sell,
                "exchange":exchange,
                "ordertype":"STOPLOSS_MARKET",
                "producttype":"INTRADAY",
                "duration":"DAY",
                "triggerprice":price,
                "price":price,
                "quantity":quantity
                }
    response = obj.placeOrder(params)
    return response
