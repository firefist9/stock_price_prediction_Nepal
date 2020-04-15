import numpy as np
from datetime import date, timedelta
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from keras.models import load_model

model = load_model('NBL_LSTM_new_1bz_1epoc.h5')
df = pd.read_csv("NBL.txt")
#Create a new dataframe with only the 'Close' column
data = df.filter(['Close'])
#Converting the dataframe to a numpy array
dataset = data.values
scaler = MinMaxScaler(feature_range=(0, 1)) 
scaled_data = scaler.fit_transform(dataset)


def predict_stock(symbol): 
    #print("Enter the symbol again")
    #symbol = input()
    textfile = str(symbol)+".txt"
    print("Enter the date to be predicted")
    #input_date = date(2020,3,20)
    #input_date = input()
    year = int(input('Enter a year'))
    month = int(input('Enter a month'))
    day = int(input('Enter a day'))
    input_date = date(year, month, day)
    
    with open(textfile, 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        x = int(last_line[:4])
        y = int(last_line[5:7])
        z = int(last_line[8:10])
    ldate = date(x, y, z)
    delta = input_date - ldate
    date_close_df = df.filter(['Date'] + ['Close'])

    
    
    
    for i in range(delta.days):
        #Create a new dataframe
        new_df = date_close_df.filter(['Close'])
        #Get teh last 60 day closing price 
        last_60_days = new_df[-60:].values
        #Scale the data to be values between 0 and 1
        last_60_days_scaled = scaler.transform(last_60_days)
        #Create an empty list
        X_test = []
        #Append teh past 60 days
        X_test.append(last_60_days_scaled)
        #Convert the X_test data set to a numpy array
        X_test = np.array(X_test)
        #Reshape the data
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        #Get the predicted scaled price
        pred_price = model.predict(X_test)
        #undo the scaling 
        pred_price = scaler.inverse_transform(pred_price)
        #print(int(pred_price))
        
        new_day = ldate + timedelta(days=i+1)
        #print(new_day)
        #print("\t")
        fd = pd.DataFrame([[new_day, int(pred_price)]], columns=('Date','Close'))
        print(fd)
        date_close_df = date_close_df.append(fd, ignore_index=True)
    return(date_close_df)


