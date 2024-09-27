import yfinance as yf
import pandas as pd
import streamlit as st


st.title("44 MA Scanner")

uploaded_file = st.file_uploader("Upload CSV file with Nifty stock symbols", type="csv")

def is_green_candle_on_rising_44ma(stock_symbol):
    try:
        stock_data = yf.download(stock_symbol, period='100d', interval='1d')

        stock_data['44_MA'] = stock_data['Close'].rolling(window=44).mean()

        if stock_data['44_MA'].iloc[-1] > stock_data['44_MA'].iloc[-2]:
            if stock_data['Close'].iloc[-1] > stock_data['Open'].iloc[-1] and \
               stock_data['Low'].iloc[-1] <= stock_data['44_MA'].iloc[-1] <= stock_data['High'].iloc[-1]:
                return True
        return False
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return False

if uploaded_file is not None:
    stock_list = pd.read_csv(uploaded_file)

    qualifying_stocks = []

    for symbol in stock_list['stock']:
        if is_green_candle_on_rising_44ma(symbol):
            qualifying_stocks.append(symbol)

    if qualifying_stocks:
        st.success("Stocks with green candle on rising 44 MA:")
        for stock in qualifying_stocks:
            st.write(stock)
    else:
        st.warning("No stocks meet the criteria.")
