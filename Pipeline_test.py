from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import os, re


def parse_csv_dir(dir):
    data = pd.DataFrame()
    for i in os.listdir(dir)[::10]:
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
    data = men.append(women)
    regex = re.compile("([^a-zA-Z']|_)")

    data['Review'] = data['Side Effects'] + " " + data['Comments']
    data['Review'] = data['Review'].apply(str.lower)

    # data['Review'] = data['Review'].apply(re.sub, args={'pattern': regex, 'repl': " "}) #какая то фигня

    print(data['Review'])
    return data


dataset = prepare_data('out/drugs/')
dataset = dataset.dropna()
y = dataset['Sex']
X = dataset['Review']

data_transformer = Pipeline([('vect', CountVectorizer()),
                             ('tf-idf', TfidfTransformer())
                             ])

dataset = data_transformer.fit_transform(X, y)

print(data_transformer.named_steps['vect'].get_stop_words())
