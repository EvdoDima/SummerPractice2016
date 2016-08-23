import pandas as pd
import os, time, operator, re, math
from sklearn import preprocessing

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
        for word in re.sub("[^a-zA-Z']|_", " ", review).split():
            if word in words.keys():
                words[word] += 1
            else:
                words[word] = 1

    sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
    MIN_WORD_COUNT = 13
    sorted_words = [word for word in sorted_words if word[1] >= MIN_WORD_COUNT]

    return sorted_words


def prepare_dataset(words, df):
    df = df[100:110]
    print(words['Word'].tolist())

    for word in words['Word'].tolist():
        df[word] = df['Review'].apply(str.count, args=[word])

    # for index, data in df[-10:].iterrows():
    #     result_set = result_set.append([]+[data['Review'].count(word) for word in words] + [data['Sex']],
    #                                    ignore_index=True)
    return df


def parse_and_write_words():
    words = count_words(df)
    words_df = pd.DataFrame(words)
    words_df.columns = ['Word', 'Count']
    words_df.to_csv('out/words.csv')



def get_and_weight_words():
    words_from = pd.DataFrame.from_csv('out/words.csv')
    # words_from["Weight"] = tf_idf(words_from)
    words_from["Weight"] = words_from.apply(tf_idf, axis=1)
    words_from["Weight_Abs"] = words_from['Weight'].apply(abs)
    # scaler = preprocessing.MaxAbsScaler()
    # words_from["Weight_Scaled"] = scaler.fit_transform(words_from['Weight'])
    words_from.sort_values('Weight_Abs', axis=0, inplace=True)
    return words_from


df = pd.DataFrame.from_csv('out/merged_input.csv', parse_dates=False)
df['Review'] = df['Comments'] + ' ' + df['Side Effects']

df = df.drop(['Date Added'], axis=1)
df = df.dropna()
df['Review'] = df['Comments'] + ' ' + df['Side Effects']



m_rev = df[df['Sex'] == 'M']['Review']
f_rev = df[df['Sex'] == 'F']['Review']

m_rev_len = len(m_rev)
f_rev_len = len(f_rev)

m_rev_concat = " ".join(m_rev)
f_rev_concat = " ".join(f_rev)


def tf_idf(word):
    w = word['Word']
    # c = word['Count']
    num = f_rev_len * m_rev_concat.count(w)
    den = m_rev_len * f_rev_concat.count(w)
    if den == 0 or num == 0:
        return 0
    com = float(num) / den
    # res = c * math.log(com)
    res = math.log(com)

    print(res)
    return res


words_wieghted = pd.DataFrame.from_csv('out/weighted_words.csv')

# dataset = prepare_dataset(words_from[:100], df)
# dataset = dataset.drop(['Rating', 'Reason', 'Side Effects', 'Comments', 'Duration/Dosage', 'Drug Name', 'Review'],
#                        axis=1)

print(words_wieghted[::100])
