import ta

def adx(df):
    df['adx'] = ta.trend.ADXIndicator(
        df['High'], df['Low'], df['Close'], window=14).adx()
    # df['adx'] = adx
    df['+DI'] = ta.trend.ADXIndicator(
        df['High'], df['Low'], df['Close'], window=14).adx_pos()
    df['-DI'] = ta.trend.ADXIndicator(
        df['High'], df['Low'], df['Close'], window=14).adx_neg()
    if df['adx'][len(df)-1] >= 20 and df['+DI'][len(df)-1] > df['-DI'][len(df)-1]:
        return 1
    return 0
# print(df)
# print(adx(df))
