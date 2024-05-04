import urllib
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger
import json
import datetime as dt
import pandas as pd

def get_instrument_list():
    instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = urllib.request.urlopen(instrument_url)
    instrument_list = json.loads(response.read())
    return instrument_list

def token_lookup(ticker, instrument_list, exchange="NSE"):
    for instrument in instrument_list:
        if instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[-1] == "EQ":
            return instrument["token"]
        
def symbol_lookup(token, instrument_list, exchange="NSE"):
    for instrument in instrument_list:
        if instrument["token"] == token and instrument["exch_seg"] == exchange:
            return instrument["symbol"][:-3]

def get_ltp(obj,instrument_list,ticker,exchange="NSE"):
    params = {
                "tradingsymbol":"{}-EQ".format(ticker),
                "symboltoken": token_lookup(ticker, instrument_list)
             }
    response = obj.ltpData(exchange, params["tradingsymbol"], params["symboltoken"])
    return response["data"]["ltp"]

def stream_list(list_stocks,exchange="nse_cm"):
    #SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
    # token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
    return_string = ''
    for count,ticker in enumerate(list_stocks):
        if count != 0:
            return_string+= '&'+exchange+'|'+token_lookup(ticker,instrument_list)
        else:
            return_string+= exchange+'|'+token_lookup(ticker,instrument_list)
    return return_string

def hist_data(obj, ticker,st_date,end_date,interval,instrument_list,exchange="NSE"):
    params = {
             "exchange": exchange,
             "symboltoken": token_lookup(ticker,instrument_list),
             "interval": interval,
             "fromdate": st_date,
             "todate": end_date
             }
    hist_data = obj.getCandleData(params)
    df_data = pd.DataFrame(hist_data["data"],
                           columns = ["date","open","high","low","close","volume"])
    df_data.set_index("date",inplace=True)
    
    return df_data

def hist_data_from_now(obj, ticker,duration,interval,instrument_list,exchange="NSE"):
    params = {
             "exchange": exchange,
             "symboltoken": token_lookup(ticker,instrument_list),
             "interval": interval,
             "fromdate": (dt.date.today() - dt.timedelta(duration)).strftime('%Y-%m-%d %H:%M'),
             "todate": dt.date.today().strftime('%Y-%m-%d %H:%M')  
             }
    hist_data = obj.getCandleData(params)
    df_data = pd.DataFrame(hist_data["data"],
                           columns = ["date","open","high","low","close","volume"])
    df_data.set_index("date",inplace=True)
    df_data.index = pd.to_datetime(df_data.index)
    df_data.index = df_data.index.tz_localize(None)
    
    return df_data



####### Websocket V2 sample code #######

def get_data_stream(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN, token_list, correlation_id, action, mode):
    
    #retry_strategy=0 for simple retry mechanism
    sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=2, retry_strategy=0, retry_delay=10, retry_duration=30)

    #retry_strategy=1 for exponential retry mechanism
    # sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=3, retry_strategy=1, retry_delay=10,retry_multiplier=2, retry_duration=30)
    def on_data(wsapp, message):
        logger.info("Ticks: {}".format(message))
        # close_connection()

    def on_control_message(wsapp, message):
        logger.info(f"Control Message: {message}")

    def on_open(wsapp):
        logger.info("on open")
        some_error_condition = False
        if some_error_condition:
            error_message = "Simulated error"
            if hasattr(wsapp, 'on_error'):
                wsapp.on_error("Custom Error Type", error_message)
        else:
            sws.subscribe(correlation_id, mode, token_list)
            # sws.unsubscribe(correlation_id, mode, token_list1)

    def on_error(wsapp, error):
        logger.error(error)

    def on_close(wsapp):
        logger.info("Close")

    def close_connection():
        sws.close_connection()


    # Assign the callbacks.
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close
    sws.on_control_message = on_control_message

    return sws

    

