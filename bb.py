import ta
import yfinance as yf
import datetime


def bb(df):
    indicator_bb = ta.volatility.BollingerBands(
        df['Close'], window=10, window_dev=2)
    width = indicator_bb.bollinger_wband()
    current_width = width[len(width)-1]
    prv_width = width[len(width)-2]
    pr_chng = ((current_width-prv_width)/prv_width)*100
    if pr_chng <= 0:
        return 0
    elif pr_chng <= 25:
        return 1
    elif pr_chng <= 50:
        return 2
    elif pr_chng <= 75:
        return 3
    else:
        return 4
