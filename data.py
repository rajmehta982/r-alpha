
import urllib
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger

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

def get_ltp(instrument_list,ticker,exchange="NSE"):
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



####### Websocket V2 sample code #######

def get_data_stream(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN, token_list ):
    correlation_id = "abc123"
    action = 1
    mode = 1
    
    #retry_strategy=0 for simple retry mechanism
    sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=2, retry_strategy=0, retry_delay=10, retry_duration=30)

    #retry_strategy=1 for exponential retry mechanism
    # sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=3, retry_strategy=1, retry_delay=10,retry_multiplier=2, retry_duration=30)

    # def on_open(wsapp):
    #     logger.info("on open")
    #     some_error_condition = False
    #     if some_error_condition:
    #         error_message = "Simulated error"
    #         if hasattr(wsapp, 'on_error'):
    #             wsapp.on_error("Custom Error Type", error_message)
    #     else:
    #         sws.subscribe(correlation_id, mode, token_list)
    #         # sws.unsubscribe(correlation_id, mode, token_list1)

    def on_control_message(wsapp, message):
        logger.info(f"Control Message: {message}")

    # def on_error(wsapp, error):
    #     logger.error(error)

    def on_close(wsapp):
        logger.info("Close")

    def close_connection():
        sws.close_connection()

    # Assign the callbacks.
    # sws.on_open = on_open
    # sws.on_error = on_error
    sws.on_close = on_close
    sws.on_control_message = on_control_message

    return sws

    

