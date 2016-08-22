import pandas as pd
import os
import time
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
    df['Review'] = df['Comments']+' '+df['Side Effects']
    for review in df['Review']:
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
sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)

MIN_WORD_COUNT = 2
sorted_words = [word for word in sorted_words if word[1] > MIN_WORD_COUNT]
print(len(sorted_words))
print(sorted_words)
