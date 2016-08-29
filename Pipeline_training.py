from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.metrics import classification_report
from sklearn import linear_model, cross_validation, svm
from sklearn import metrics
from sklearn import cross_validation
from sklearn import linear_model, preprocessing
import os, re, functools
import numpy as np

dataset = pd.DataFrame.from_csv("corpus.csv")
print(len(dataset))

clf = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), max_features=12000))
                # ('clf', linear_model.SGDClassifier(penalty='l1',n_jobs=-1,alpha=0.0003))
                   , ('clf', svm.SVC(kernel='gausian'))
                ])

X = dataset['Review']
y = dataset['Sex']

print("training...")

# Train/test split
# X_train,y_train,X_test,y_test  = cross_validation.train_test_split(X,y,test_size=0.1)
# clf.fit(X_train, y_train)
# print(len(clf.named_steps['vect'].get_feature_names()))


# cross-validation by Rinat
# scores = cross_validation.cross_val_score(clf, X, y, cv=5)

# K-fold CV
k_fold = KFold(n=len(X), n_folds=10)
scores = []
for train_indices, test_indices in k_fold:
    local_train_X = X.iloc[train_indices]
    local_train_y = y.iloc[train_indices]

    local_test_X = X.iloc[test_indices]
    local_test_y = y.iloc[test_indices]

    clf.fit(local_train_X, local_train_y)
    predictions = clf.predict(local_test_X)

    score = metrics.accuracy_score(local_test_y, predictions)
    scores.append(score)
    print(score)
#
scores = np.array(scores)

y_pred = clf.predict(X)
report = metrics.classification_report(y, y_pred, target_names=["F", "M"])
print(report)
print("CV accuracy: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std() * 2))
print("Full corpus accuracy : %0.3f" % metrics.accuracy_score(y, y_pred))
