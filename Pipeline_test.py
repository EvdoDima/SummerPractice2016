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


def parse_csv_dir_to_drugs_stat(dir):
    data = pd.DataFrame(columns=['Name', 'Reviews count', 'F', 'M'])
    ind = 0

    def process_drug(drug_data):  # Drug processing. remove one gendered drug
        drug_data.fillna("", inplace=True)
        ln = len(drug_data)
        female_count = len(drug_data[drug_data["Sex"] == "F"])

        return ln, female_count, ln - female_count
    for i in os.listdir(dir):
        print(i)
        drug = pd.DataFrame.from_csv(dir + i)
        data.loc[ind] = ([i] + list(process_drug(drug)))
        ind += 1
    data.sort_values('Reviews count', inplace=True, ascending=False)
    return data


def choose_drugs(drug_data):  # Drug processing. remove one gendered drug. get the top
    return drug_data['Name'].values


def parse_drugs():
    dir = "out/drugs/"
    data = pd.DataFrame.from_csv("out/drugs_stat.csv")
    print("parsing drugs dir...")
    for i in choose_drugs(data):
        new_data = pd.DataFrame.from_csv(dir + i)
        data = data.append(new_data)
    return data





def prepare_data(data):
    data = data.dropna()
    men = data[data['Sex'] == 'M']
    women = data[data['Sex'] == 'F'].sample(len(men))
    data = men.append(women).sample(frac=1)  # reshuffle reviews, just in case.

    # regex = re.compile("([^a-zA-Z']|_)")

    def numify_sex(gender):
        return 0 if gender == "F" else 1

    data['Sex'] = data['Sex'].apply(numify_sex)

    data['Review'] = data['Side Effects'] + " " + data['Comments']
    data['Review'] = data['Review'].apply(str.lower)

    def replace_non_letters(word):
        return re.sub("([^a-zA-Z']|_)", " ", word)

    data['Review'] = data['Review'].apply(replace_non_letters)
    return data

drugs_stat = parse_csv_dir_to_drugs_stat("out/drugs/")
drugs_stat.to_csv("drugs_stat.csv")
data = parse_drugs()
data.to_csv("out/data.csv")
# data = pd.DataFrame.from_csv("out/data.csv")
dataset = prepare_data(data)

clf = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), max_features=10000))
                # ('clf', linear_model.SGDClassifier(penalty='l1',n_jobs=-1,alpha=0.0003))
                   , ('clf', linear_model.LogisticRegression(n_jobs=-1))
                ])

X = dataset['Review']
y = dataset['Sex']

print("training...")
# Train/test split
# clf.fit(X, y)
# print(len(clf.named_steps['vect'].get_feature_names()))


# cross-validation
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
