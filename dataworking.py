import pandas as pd
import quandl as qd
import numpy as np
import datetime
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')


df = qd.get('WIKI/GOOGL')

df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low']
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open']

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

forecast_col = 'Adj. Close'
forecast_time = 30

df['label'] = df[forecast_col].shift(-forecast_time)
# df.fillna(-9999, inplace=True) нахуй надо если мы потом все равно делаем dropna

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

# если поймешь че тут дальше происходит расскажи мне (это все чисто для графика нужно так что я не особо пытался разобраться)
last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

df['Forecast'] = np.nan

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix+=one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]


df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')

plt.show()

