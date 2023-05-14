import streamlit as st
import data as d
import pandas_datareader as data
import datetime
import numpy
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
from keras.models import load_model
from keras.layers import LSTM
import keras.backend as K
from numpy import array
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
st.set_page_config(
    page_title="AI STOCK RECOMMENDOR"
)

st.write("Setting up things for you ")
d.data()

# st.write("# Welcome to Streamlit! 👋")

# st.sidebar.success("Select a demo above.")

#GRAPH1-------------------------------------------------------------
user_input = st.text_input("Enter the stock ticker", "SBIN")
start_date = datetime.datetime.now()- datetime.timedelta(days=3650)
end_date = datetime.datetime.now()
stock = yf.download(user_input + '.NS', start=start_date,
                                end=end_date, interval='1d')

# df1=stock.reset_index()['Close']
today=datetime.date.today()
today.strftime("%B %d, %Y")
st.subheader(f"data from 2022 to {today}")
# st.write(df1.columns)
# print(df1.columns())

st.subheader("closing price vs time chart MAX")
fig = plt.figure(figsize=(12, 6))
plt.plot(stock['Close'])
st.pyplot(fig)

#GRAPH2---------------------------------------------------------------

model=load_model("future122_new.h5")
training_size=int(len(stock)*0.65)

scaler=MinMaxScaler(feature_range=(0,1))
df1=scaler.fit_transform(numpy.array(stock['Close']).reshape(-1,1))
# print(df1)
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]
# print(train_data)
time_step = 300
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return numpy.array(dataX), numpy.array(dataY)
 # reshape into X=t,t+1,t+2,t+3 and Y=t+4
X_test, ytest = create_dataset(test_data, time_step)
X_train, y_train = create_dataset(train_data, time_step)
# print(X_train.shape[0])
# print(X_train)
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)





### Lets Do the prediction and check performance metrics
train_predict=model.predict(X_train)
test_predict=model.predict(X_test)



##Transformback to original form
train_predict=scaler.inverse_transform(train_predict)
test_predict=scaler.inverse_transform(test_predict)


look_back=300
trainPredictPlot = numpy.empty_like(df1)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(train_predict)+look_back, :] = train_predict
# shift test predictions for plotting
testPredictPlot = numpy.empty_like(df1)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(train_predict)+(look_back*2)+1:len(df1)-1, :] = test_predict
# plot baseline and predictions
fig = plt.figure(figsize=(12, 6))
st.subheader("Train,test and original")
plt.plot(scaler.inverse_transform(df1))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
# plt.show()
plt.legend(['original','test','train'], loc='upper left')
st.pyplot(fig)



#GRAPH3---------------------------------------------------------------

x_input=test_data[len(test_data)-300:].reshape(1,-1)
x_input.shape
temp_input=list(x_input)
temp_input=temp_input[0].tolist()

# demonstrate prediction for next 30 days
from numpy import array
lst_output=[]
n_steps=300
i=0
while(i<30):
    
    if(len(temp_input)>300):
        #print(temp_input)
        x_input=numpy.array(temp_input[1:])
        # print("{} day input {}".format(i,x_input))
        x_input=x_input.reshape(1,-1)
        x_input = x_input.reshape((1, n_steps, 1))
        #print(x_input)
        yhat = model.predict(x_input, verbose=0)
        # print("{} day output {}".format(i,yhat))
    
        temp_input.extend(yhat[0].tolist())
        temp_input=temp_input[1:]
        #print(temp_input)
        lst_output.extend(yhat.tolist())
        i=i+1
    else:
        x_input = x_input.reshape((1,n_steps,1))
        yhat = model.predict(x_input, verbose=0)
        # print(yhat[0])
        temp_input.extend(yhat[0].tolist())
        # print(len(temp_input))
        lst_output.extend(yhat.tolist())
        i=i+1

# print(lst_output)
day_new=numpy.arange(1,301)
day_pred=numpy.arange(301,331)
fig = plt.figure(figsize=(12, 6))
st.subheader("predicted graph")
plt.plot(day_new,scaler.inverse_transform(df1[len(df1)-300:]))
plt.plot(day_pred,scaler.inverse_transform(lst_output))
st.pyplot(fig)

# #GRAPH4---------------------------------------------------------------

df3=df1.tolist()
df3.extend(lst_output)
# st.subheader("Known + predicted graph")
# fig = plt.figure(figsize=(12, 6))
# plt.plot(df3[2640:])
# st.pyplot(fig)

#GRAPH5---------------------------------------------------------------

# fig2 = plt.figure(figsize=(12, 6))
prediction=scaler.inverse_transform(lst_output)
# st.markdown(prediction.index.tolist())
st.subheader("30 DAYS PREDICTED STOCK PRICES")
st.write(prediction)
# st.pyplot(fig2)



#GRAPH6---------------------------------------------------------------
st.subheader("MAX with prediction")
df3=scaler.inverse_transform(df3).tolist()
fig=plt.figure(figsize=(12,6))
plt.plot(df3)
st.pyplot(fig)