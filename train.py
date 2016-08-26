import pandas as pd
from sklearn import preprocessing, cross_validation, svm, linear_model, neural_network
from sklearn.metrics import classification_report
import numpy as np

df = pd.DataFrame.from_csv('out/dataset.csv')

def numify_sex(gender):
	return 0 if gender == "F" else 1


X = np.array(df.drop('Sex', axis=1))
X = preprocessing.scale(X)
y = df['Sex'].apply(numify_sex)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

print("starting training...")
# clf = linear_model.LogisticRegression(solver='sag', max_iter=1e3)
clf = svm.SVC()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
report = classification_report(y_test, y_pred, target_names=["F", "M"])
print(sum(y_pred))
# accuracy = clf.score(X_test, y_test)

print(report)