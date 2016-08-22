import pandas as pd
import os
import time
import numpy as np
import operator
import re

input_dir = 'out/drugs/'


def parse_csv_dir(dir):
    start = time.time()
    df = pd.DataFrame()
    for i in os.listdir(dir):
        print(i)
        df = df.append(pd.DataFrame.from_csv(input_dir + i))
    end = time.time()
    print(end - start)
    return df


def count_words(df):
    words = {}
    for review in df['Comments']:
        review = review.lower()
        for word in re.sub("[^\w]|_", " ", review).split():
            if word in words.keys():
                words[word] += 1
            else:
                words[word] = 1

    return words


df = pd.DataFrame.from_csv('out/merged_input.csv', parse_dates=False)
df = df.drop(['Date Added', 'Rating'], axis=1)
df = df.dropna()
# shuffled_df = df.iloc[np.random.permutation(len(df))]
words = count_words(df)
sorted_words = sorted(words.items(), key=operator.itemgetter(1),reverse=True)
print(len(sorted_words))
print(sorted_words)
