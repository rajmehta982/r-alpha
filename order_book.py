def token_lookup(ticker, instrument_list, exchange="NSE"):
        for instrument in instrument_list:
            if instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[-1] == "EQ":
                return instrument["token"]
            
def symbol_lookup(token,exchange="NSE"):
    for instrument in instrument_list:
        if instrument["token"] == token and instrument["exch_seg"] == exchange:
            return instrument["symbol"][:-3]

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

def expected_buy_price(tick, pos_size):
    ask_prices = [float(tick[i]) for i in tick if i[:2]=="sp"]
    ask_sizes = [float(tick[i]) for i in tick if i[:2]=="bs"]

    cum_pos = 0
    cum_size = 0
    prev_fill = 0
    prev_price = 0
    
    for i in range(len(ask_prices)):
        cum_pos+= ask_prices[i]*ask_sizes[i]
        cum_size+= ask_sizes[i]
        if pos_size <= cum_pos:
            return ((prev_price*prev_fill) + (ask_prices[i]*(pos_size - prev_fill)))/pos_size
        else:
            prev_fill = cum_pos
            prev_price = round(cum_pos/cum_size,2)
    return round(cum_pos/cum_size,2)
        
def expected_sell_price(tick, pos_size):
    bid_prices = [float(tick[i]) for i in tick if i[:2]=="bp"]
    bid_sizes = [float(tick[i]) for i in tick if i[:2]=="bq"]
    
    cum_pos = 0
    cum_size = 0
    prev_fill = 0
    prev_price = 0
    
    for i in range(len(bid_prices)):
        cum_pos+= bid_prices[i]*bid_sizes[i]
        cum_size+= bid_sizes[i]
        if pos_size <= cum_pos:
            return ((prev_price*prev_fill) + (bid_prices[i]*(pos_size - prev_fill)))/pos_size
        else:
            prev_fill = cum_pos
            prev_price = round(cum_pos/cum_size,2)
    return round(cum_pos/cum_size,2)
    
            
def trend_detection(ratio_list):
    if len(ratio_list) >= 30 and max(ratio_list) >= 10 and min(ratio_list) >= 5 and mean(ratio_list) >= 8:
        return "Buy"
    elif len(ratio_list) >= 30 and min(ratio_list) <= 0.1 and max(ratio_list) <= 0.2 and mean(ratio_list) <= 0.125 :
        return "Sell"
    else:
        return 0

def exit_long(ratio_list):
        if max(ratio_list) <= 4 and min(ratio_list) <= 1.5 and mean(ratio_list) <= 2:
            return True
        else:
            return False
        
def exit_short(ratio_list):
    if min(ratio_list) >= 0.25 and max(ratio_list) >= 0.65 and mean(ratio_list) >= 0.4:
        return True
    else:
        return False

bid_ask_ratio = {}
long_trades = {}
short_trades = {}

for ticker in ticker_list:
    bid_ask_ratio[ticker] = []
    long_trades[ticker] = []
    short_trades[ticker] = []

pos_size = 10000

long_pos = []
short_pos = []


def order_book_strategy(tick):
    token = tick['token']
    tot_bid_vol = 0
    tot_ask_vol = 0
    buy_data = tick['best_5_buy_data']
    sell_data = tick['best_5_sell_data']
    for bd in buy_data:
        tot_bid_vol+= int(bd['quantity'])
    for sd in sell_data:
        tot_ask_vol+= int(sd['quantity'])

    bid_ask_ratio[symbol_lookup(token)].append(tot_bid_vol/tot_ask_vol)
    if len(bid_ask_ratio[symbol_lookup(token)]) > 30:
        bid_ask_ratio[symbol_lookup(token)].pop(0)
    
    if symbol_lookup(token) not in long_pos:
        if trend_detection(bid_ask_ratio[symbol_lookup(token)]) == "Buy":
            print("{}: buy {} at price {} : total bid volume = {}, total ask volume = {}".format(dt.datetime.now(),symbol_lookup(token),expected_buy_price(tick,pos_size),tot_bid_vol,tot_ask_vol))
            long_pos.append(symbol_lookup(token))
            long_trades[symbol_lookup(token)].append([expected_buy_price(tick,pos_size)])
    else:
        if exit_long(bid_ask_ratio[symbol_lookup(token)]):
            print("{}: close long {} at price {} : total bid volume = {}, total ask volume = {}".format(dt.datetime.now(),symbol_lookup(token),expected_sell_price(tick,pos_size),tot_bid_vol,tot_ask_vol))
            long_pos.remove(symbol_lookup(token))
            long_trades[symbol_lookup(token)][-1].append(expected_sell_price(tick,pos_size))
    if symbol_lookup(token) not in short_pos:
        if trend_detection(bid_ask_ratio[symbol_lookup(token)]) == "Sell":    
            print("{}: sell {} at price {}: total bid volume = {}, total ask volume = {}".format(dt.datetime.now(),symbol_lookup(token),expected_sell_price(tick,pos_size),tot_bid_vol,tot_ask_vol))
            short_pos.append(symbol_lookup(token))
            short_trades[symbol_lookup(token)].append([expected_sell_price(tick,pos_size)])
    else:
        if exit_short(bid_ask_ratio[symbol_lookup(token)]):
            print("{}: close short {} at price {} : total bid volume = {}, total ask volume = {}".format(dt.datetime.now(),symbol_lookup(token),expected_buy_price(tick,pos_size),tot_bid_vol,tot_ask_vol))
            short_pos.remove(symbol_lookup(token))
            short_trades[symbol_lookup(token)][-1].append(expected_buy_price(tick,pos_size))

    print(symbol_lookup(token), "last 5 bid ask ratios :", bid_ask_ratio[symbol_lookup(token)][-5:])

def on_data(ws, message):
    order_book_strategy(message)

def run_order_book_strat(sws):
    sws.on_data = on_data