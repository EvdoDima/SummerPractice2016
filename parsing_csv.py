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

    sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
    MIN_WORD_COUNT = 2
    sorted_words = [word for word in sorted_words if word[1] > MIN_WORD_COUNT]

    return sorted_words




df = pd.DataFrame.from_csv('out/merged_input.csv', parse_dates=False)
df = df.drop(['Date Added'], axis=1)
df = df.dropna()

# words = count_words(df)
# words_df = pd.DataFrame(words)
# words_df.to_csv('out/words.csv')

words_from = pd.DataFrame.from_csv('out/words.csv')


print(words_from.head())
