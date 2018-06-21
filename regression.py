import pandas as pd
import quandl
import math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

df = quandl.get('WIKI/GOOGL')
print("Avialable labels = ",list(df))

df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close'])/df['Adj. Close']*100.0
df['PCT_Change'] = (df['Adj. Close'] - df['Adj. Open'])/df['Adj. Open']*100.0

df = df[['Adj. Close','HL_PCT','PCT_Change','Adj. Volume']]

print(df.head())
forecast_col = 'Adj. Close'

#instead of Nan, considering as outlier for not loosing nan row other information
#inplace used for instead of reassining a slice of previous dataframe into result varriable, we directly changed the dataframe
df.fillna(-99999, inplace=True)

forecast_out = int(math.ceil(0.01*len(df)))

#Shift index by desired number of periods with an optional time freq
df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)

X = np.array(df.drop(['label'],1))
y = np.array(df['label'])
X = preprocessing.scale(X)
y = np.array(df['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = LinearRegression()
clf.fit(X_train, y_train) #train
accuracy = clf.score(X_test, y_test) #test

print(accuracy)
