import yfinance as yf
from datetime import datetime, timedelta

def get_top_nse_stocks_by_volume(instrument_list, last_n_days=4):
    # Get NSE tickers
    
    # Get trading volume for each ticker for the last n days
    volume_data = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=last_n_days)
    
    for ticker_data in instrument_list:
        ticker_symbol = ticker_data['name'] + '.NS'
        try:
            history = yf.download(ticker_symbol, start=start_date, end=end_date)
            print(history)
            if not history.empty:
                volume = history['Volume'].sum()
                seven_day_return = history['Close'].iloc[-1]/history['Close'].iloc[0] - 1
                if seven_day_return > 0:
                    volume_data[ticker_symbol] = volume
        except Exception as e:
            print(f"Error fetching data for {ticker_symbol}: {e}")

    # Sort stocks by volume in descending order
    sorted_stocks = sorted(volume_data.items(), key=lambda x: x[1], reverse=True)
    
    # Extract top 10 stocks
    top_10_stocks = sorted_stocks[:10]
    
    return top_10_stocks


def momentum_strategy(tick):

    global position
    global trades
    global capital
    global ticker_ltp
    ### add ltp and return to dictionary
    token = tick['token']
    ltp = tick['last_traded_price']/100

    momentum_signal = 0

    if token in ticker_ltp:
        ticker_ltp[token]['ltp'].append(ltp)
        momentum_short = pd.Series(ticker_ltp[token]['ltp']).rolling(window=momentum_short_window).mean().iloc[-1]

        ticker_ltp[token]['momentum_short'].append(momentum_short)
        momentum_long = pd.Series(ticker_ltp[token]['ltp']).rolling(window=momentum_long_window).mean().iloc[-1]
        ticker_ltp[token]['momentum_long'].append(momentum_long)
    else:
        ticker_ltp[token] = {
            'ltp': [ltp],
            'momentum_short':[None],
            'momentum_long': [None]
        }

    # print(ticker_ltp[token]['momentum_short'])

    # Check momentum signal
    if (ticker_ltp[token]['momentum_short'][-1] is not None) and (ticker_ltp[token]['momentum_long'][-1] is not None):
        if ticker_ltp[token]['momentum_short'][-1] > ticker_ltp[token]['momentum_long'][-1]:
            momentum_signal = 1
        elif ticker_ltp[token]['momentum_short'][-1] < ticker_ltp[token]['momentum_long'][-1]:
            momentum_signal = -1

    #create trade
    # print(momentum_signal)

    if momentum_signal == 1 and position == 0:
        quantity = capital / ltp
        price = ltp
        position = 1
        capital = 0

        if token in trades:
            trades[token]['buy_prices'].append(price)
            trades[token]['quantity'].append(quantity)
            trades[token]['sell_price'].append(None)
        
        else:
            trades[token] = {
            'buy_prices': [price],
            'quantity': [quantity],
            'sell_price': [None]
            }

    elif momentum_signal == -1 and position == 1:
        quantity = trades[token]['quantity'][-1]
        price = ltp
        position = 0

        capital = quantity*price
        if token in trades:
            trades[token]['sell_price'].append(price)
        
        else:
            trades[token] = {
            'sell_price':price
            }



            



