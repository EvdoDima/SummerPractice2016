from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn import cross_validation
from sklearn import linear_model, preprocessing
import os, re, functools


def parse_csv_dir(dir):
    data = pd.DataFrame()
    for i in os.listdir(dir):
        print(i)
        new_data = pd.DataFrame.from_csv(dir + i)
        new_data = process_drug(new_data)
        data = data.append(new_data)
    return data


def process_drug(drug_data):  # Drug processing. remove one gendered drug
    return drug_data


def prepare_data(dir):
    data = parse_csv_dir(dir).dropna()
    men = data[data['Sex'] == 'M']
    women = data[data['Sex'] == 'F'].sample(len(men))
    data = men.append(women).sample(frac=1) # reshuffle reviews, just in case. 
    # regex = re.compile("([^a-zA-Z']|_)")

    def numify_sex(gender):
        return 0 if gender == "F" else 1

    data['Sex'] = data['Sex'].apply(numify_sex)

    data['Review'] = data['Side Effects'] + " " + data['Comments']
    data['Review'] = data['Review'].apply(str.lower)

    def replace_non_letters(word):
        return re.sub("([^a-zA-Z']|_)", " ", word)

    data['Review'] = data['Review'].apply(replace_non_letters)

    print(data['Review'])
    return data


dataset = prepare_data('out/drugs/')
dataset = dataset.dropna()
y = dataset['Sex']
X = dataset['Review']

clf = Pipeline([('vect', CountVectorizer()),
                ('tf-idf', TfidfTransformer()),
                ('clf', linear_model.LogisticRegression())
                ])


X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.1)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
report = metrics.classification_report(y_test, y_pred, target_names=["F", "M"])
print(report)


# cross-validation
# scores = cross_validation.cross_val_score(clf, X, y, cv=5)
# print(scores)
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))