import pandas as pd
import streamlit as st

df = pd.read_excel('AICP_LT.xlsx', index_col='Symbol')
df['weights'] = 0

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

def alpha_beta(df):
    
    df.loc[df['Alpha']<0 , 'weights'] +=0 
    df.loc[df['Alpha']>0 , 'weights'] +=1 
    df.loc[df['Alpha']>1.5, 'weights']+=1 
    df.loc[df['Alpha']>3 , 'weights'] +=1 
    df.loc[df['Alpha']>7 , 'weights'] +=1 

    
    df.loc[df['Beta']<0.5 , 'weights'] +=1 
    df.loc[df['Beta']<1 , 'weights'] +=1 
    df.loc[df['Beta']<1.5, 'weights']+=1 
    df.loc[df['Beta']<2 , 'weights'] +=1 
    df.loc[df['Beta']>2 , 'weights'] +=0 

def Market_Cap(df):
    df.loc[df['Market Cap.']>45000 , 'weights'] +=0
    df.loc[df['Market Cap.']>100000 , 'weights'] +=1 
    df.loc[df['Market Cap.']>300000 , 'weights'] +=1  
    df.loc[df['Market Cap.']>500000 , 'weights'] +=1 

def ROE(df):
    df.loc[df['ROE']>0 , 'weights'] +=0 
    df.loc[df['ROE']>12 , 'weights'] +=1
    df.loc[df['ROE']>15 , 'weights'] +=1 
    df.loc[df['ROE']>25 , 'weights'] +=1 

def NPM(df):
    df.loc[df['Net profit margin']>0 , 'weights'] +=0 
    df.loc[df['Net profit margin']>10 , 'weights'] +=1 
    df.loc[df['Net profit margin']>15 , 'weights'] +=1 
    df.loc[df['Net profit margin']>20 , 'weights'] +=1 


def Current(df):
    df.loc[df['Current ratio']>0 , 'weights'] +=0 
    df.loc[df['Current ratio']>0.5 , 'weights'] +=1 
    df.loc[df['Current ratio']>1 , 'weights'] +=1 
    df.loc[df['Current ratio']>1.5 , 'weights'] +=1 
    df.loc[df['Current ratio']>3 , 'weights'] +=1 

def PE(df):
    df.loc[(df['PE']-df['SectorPE'])>5 , 'weights'] +=0
    df.loc[(df['PE']-df['SectorPE'])<5 , 'weights'] +=0.25
    df.loc[(df['PE']-df['SectorPE'])<0 , 'weights'] +=0.50
    df.loc[(df['PE']-df['SectorPE'])<-5 , 'weights'] +=0.75
    df.loc[(df['PE']-df['SectorPE'])<-10 , 'weights'] +=1

def EBIDTA(df):
    df.loc[df['DiffEBIDTA']<0 , 'weights'] +=0
    df.loc[df['DiffEBIDTA']>0 , 'weights'] +=0.25
    df.loc[df['DiffEBIDTA']>1000 , 'weights'] +=0.5
    df.loc[df['DiffEBIDTA']>2000 , 'weights'] +=0.75
    df.loc[df['DiffEBIDTA']>3500 , 'weights'] +=1

df=filterByCapital(df)
df=filtersector(df)
EBIDTA(df)
alpha_beta(df)
PE(df)
Current(df)
NPM(df)
ROE(df)
Market_Cap(df)
df=df.sort_values(by=['weights'],ascending=False)
st.dataframe(df)










