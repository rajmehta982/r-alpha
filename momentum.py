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



def momentum_strategy(top_10_stocks):

    token = tick['token']
    ltp = tick['last_traded_price']
    
    # Backtest the strategy
    initial_capital = original_data['close'].iloc[0]    # Initial capital in INR
    position = 0  # 0 for no position, 1 for long position, -1 for short position
    portfolio_value = [initial_capital]  # List to store portfolio value over time
    shares_bought = 0
    profit_list = []

    use_sell_list = []

    for date, data in grouped_data:

        for i in range(0, len(data)):

            if data['Signal'].iloc[i] == 1 and position == 0:  # Buy signal and no position
                position = 1
                shares_bought = initial_capital / data['close'].iloc[i]
                initial_capital = 0

                portfolio_value.append(initial_capital + shares_bought * data['close'].iloc[i])
            
            elif data['Signal'].iloc[i] == -1 and position == 1:  # Sell signal and long position
                position = 0
                initial_capital = shares_bought * data['close'].iloc[i]
                shares_bought = 0
        
                portfolio_value.append(initial_capital + shares_bought * data['close'].iloc[i])

            else:
                portfolio_value.append(portfolio_value[-1])
            
            use_sell_list.append(use_sell)
            



