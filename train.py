import pandas as pd
from sklearn import preprocessing, cross_validation, svm
import numpy as np

df = pd.DataFrame.from_csv('out/dataset.csv')

def numify_sex(gender):
	return 0 if gender == "F" else 1

X = np.array(df.drop('Sex', axis=1))
y = df['Sex'].apply(numify_sex)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = svm.SVC()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print(accuracy)