import pandas as pd
import os
import time
import operator
import re
import math

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
    df['Review'] = df['Comments'] + ' ' + df['Side Effects']
    for review in df['Review']:
        review = review.lower()
        for word in re.sub("[^a-zA-Z]|_", " ", review).split():
            if word in words.keys():
                words[word] += 1
            else:
                words[word] = 1

    sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
    MIN_WORD_COUNT = 2
    sorted_words = [word for word in sorted_words if word[1] > MIN_WORD_COUNT]

    return sorted_words


df = pd.DataFrame.from_csv('out/merged_input.csv', parse_dates=False)
df['Review'] = df['Comments'] + ' ' + df['Side Effects']

df = df.drop(['Date Added'], axis=1)
df = df.dropna()

# words = count_words(df)
# words_df = pd.DataFrame(words)
# words_df.columns = ['Word', 'Count']
# words_df.to_csv('out/words.csv')

m_rev = df[df['Sex'] == 'M']['Review']
f_rev = df[df['Sex'] == 'F']['Review']

m_rev_len = len(m_rev)
f_rev_len = len(f_rev)

m_rev_concat = " ".join(m_rev)
f_rev_concat = " ".join(f_rev)

def tf_idf(df):
    
    res = []
    for w, c in zip(df["Word"], df["Count"]):
        num = f_rev_len * m_rev_concat.count(w)
        den = m_rev_len * f_rev_concat.count(w)
        if den == 0 or num == 0:
            continue
        com = float(num) / den
        res = c * math.log(com)
        print(res)
    return res

words_from = pd.DataFrame.from_csv('out/words.csv')
words_from["Weight"] = tf_idf(words_from)

print(words_from.head())
