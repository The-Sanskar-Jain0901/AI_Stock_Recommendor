import pandas as pd
import yfinance as yf
import yfinance as yf
import datetime
import adx as adx
import streamlit as st
stock_data = pd.read_excel('AICP_LT.xlsx', index_col='Symbol')
stock_data['weights'] = 0


def filterByCapital(df):
    x = st.text_input('Enter your capital')
    
    for tickerSymbol in df.index:
        try:            
            close = df[df.index == tickerSymbol]['close']
            # close = df[df['tickerSymbol'] == tickerSymbol,'close']
            print(close)
            # break
            if float(x) < close.iloc[0]:
                df.drop(tickerSymbol, inplace=True)

        except Exception as e:
            print(e)
    return df
   


def filtersector(df):
    
    option = st.selectbox(
     'Select preferred Sector or select None otherwise',
     ('Cement', 'Commodities Trading', 'Construction & Engineering','Consumer Finance','Fertilizers & Agro Chemicals','FMCG - Foods',
      'FMCG - Household Products','FMCG - Tobacco','Four Wheelers','Home Financing','Hospitals & Diagnostic Centres',
      'Insurance','Iron & Steel','IT Services & Consulting','Labs & Life Sciences Services','Metals - Aluminium','Mining - Coal','Oil & Gas - Exploration & Production',
      'Oil & Gas - Refining & Marketing','Paints','Pharmaceuticals','Ports','Power Generation','Power Transmission & Distribution','Precious Metals,Jewellery & Watches','Private Banks',
      'Public Banks','Tea & Coffee','Telecom Services','Trucks & Buses','Two Wheelers','None'))

    st.write('You selected:', option)
    if(option != 'None'):
        df1 = df[df["Sector"] == option]
    else:
        return df
    return df1


def midTerm(df):
    for tickerSymbol in df.index:
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.datetime.now()
        # st.write(tickerSymbol)
        stock = yf.download(tickerSymbol + '.NS', start=start_date,
                            end=end_date, interval='1d')
        adx_val = adx.adx(stock)
        # break
        df.loc[str(tickerSymbol) == df.index,
                    'weights'] += adx_val
        if adx_val == 1:
            rded = df.loc[str(tickerSymbol) ==
                                df.index, 'R1.5']
            r1 = df.loc[str(tickerSymbol) ==
                                df.index, 'R1']
            rsava = df.loc[str(tickerSymbol) ==
                                df.index, 'R1.25']
            if stock['Close'][len(stock)-1] > rded.iloc[0]:
                df.loc[str(tickerSymbol) == df.index,
                            'weights'] += 0
            elif stock['Close'][len(stock)-1] > r1.iloc[0]:
                df.loc[str(tickerSymbol) == df.index,
                            'weights'] += 3
            elif stock['Close'][len(stock)-1] > (r1.iloc[0]-abs(r1.iloc[0]-rsava.iloc[0])):
                df.loc[str(tickerSymbol) == df.index,
                            'weights'] += 4
            elif stock['Close'][len(stock)-1] > (r1.iloc[0]-abs(r1.iloc[0]-rded.iloc[0])):
                df.loc[str(tickerSymbol) == df.index,
                            'weights'] += 2
            else:
                df.loc[str(tickerSymbol) == df.index,
                            'weights'] += 1
    return df

df=filterByCapital(stock_data)
df=filtersector(df)
df=midTerm(df)
df=df.sort_values(by=['weights'],ascending=False)
st.dataframe(df)
# print(df)
