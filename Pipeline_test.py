from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn import linear_model, cross_validation, svm
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


def prepare_data(data):
    data = data.dropna()
    men = data[data['Sex'] == 'M']
    women = data[data['Sex'] == 'F'].sample(len(men))
    data = men.append(women)
    # regex = re.compile("([^a-zA-Z']|_)")

    data['Review'] = data['Side Effects'] + " " + data['Comments']
    data['Review'] = data['Review'].apply(str.lower)

    def replace_non_letters(word):
        return re.sub("([^a-zA-Z']|_)", " ", word)

    data['Review'] = data['Review'].apply(replace_non_letters)
    return data

data = pd.DataFrame.from_csv("out/data.csv")
dataset = prepare_data(data)

y = dataset['Sex']
X = dataset['Review']
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)


clf = Pipeline([('vect', CountVectorizer()),
                ('tf-idf', TfidfTransformer()),
                ('clf', MultinomialNB())
                ])

clf.fit(X_train, y_train)

predicted = clf.predict(X_test)
report = classification_report(y_test, predicted, target_names=["F", "M"])

print(report)
