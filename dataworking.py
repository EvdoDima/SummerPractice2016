import pandas as pd
import quandl as qd
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

df = qd.get('WIKI/GOOGL')

df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low']
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open']

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

forecast_col = 'Adj. Close'
forecast_time = 30

df['label'] = df[forecast_col].shift(-forecast_time)
# df.fillna(-9999, inplace=True)

X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_time:]
X = X[:-forecast_time]

df.dropna(inplace=True)
y = np.array(df['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = LinearRegression()
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
forecast_set = clf.predict(X_lately)

print(accuracy, '\n', forecast_set)
