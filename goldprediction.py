import pandas as pd
import quandl as qd
import numpy as np
import datetime
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

from matplotlib import style

#
style.use('ggplot')

df = qd.get('LBMA/GOLD', authtoken="-q7sQoHnvKQEyMbu4qqR")

df['cur day'] = df['USD (AM)']
df['-1 day'] = df['USD (AM)'].shift(1)
df['-2 day'] = df['USD (AM)'].shift(2)
df['-3 day'] = df['USD (AM)'].shift(3)
df['-4 day'] = df['USD (AM)'].shift(4)
df['-5 day'] = df['USD (AM)'].shift(5)

forecast_time = 1

df = df[['cur day', '-1 day', '-2 day', '-3 day', '-4 day', '-5 day']]
df['label'] = df['cur day'].shift(-forecast_time)
df.dropna(inplace=True)

# print(df[-10:])
#
X = np.array(df.drop('label', axis=1))
y = df['label']

test_time = 10
X = preprocessing.scale(X)
X_lately = X[-test_time:]
X = X[:-test_time]
y_lately = y[-test_time:]
y = y[:-test_time]

# print(X_lately)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
# y_test = y_test.shift(-forecast_time)
# y_test.dropna(inplace=True)
# X_test = X_test[:-forecast_time]

clf = LinearRegression()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
############################################
# print('X =', len(X), 'X_lately =', len(X_lately), 'df =',len(df))
print(accuracy)

forecast_set = clf.predict(X_lately)
print(forecast_set)
print(y_lately)
