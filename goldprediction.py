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
df = df[['cur day']]

feauture_length = 5  # магия - чем меньше, тем точнее
for i in range(1, feauture_length):
    df['-' + str(i) + ' day'] = df['cur day'].shift(i)

forecast_time = 1

df['label'] = df['cur day'].shift(-forecast_time)
df.dropna(inplace=True)

# print(df[-10:])
#
X = np.array(df.drop('label', axis=1))
y = df['label']

test_time = 300
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

clf = svm.SVR()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
###########################################################################
print(accuracy)
forecast_set = clf.predict(X_lately)

result = df.tail(test_time)
result['Forecast'] = forecast_set
result['Real'] = result['cur day']

result['Forecast'].plot()
result['Real'].plot()

plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')

plt.show()
