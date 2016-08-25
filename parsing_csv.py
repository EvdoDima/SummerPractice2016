import pandas as pd
import os, time, operator, re, math,string
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


def count_bi_grams(df):
    global_bi_grams = {}
    df['Review'] = df['Comments'] + ' ' + df['Side Effects']
    for review in df['Review']:
        review = review.lower()
        words = re.sub("[^a-zA-Z']|_", " ", review).split()
        bigrams = zip(words, words[1:])
        bigrams = [bigram[0] + ' ' + bigram[1] for bigram in bigrams]
        for bigram in bigrams:
            if bigram in global_bi_grams.keys():
                global_bi_grams[bigram] += 1
            else:
                global_bi_grams[bigram] = 1

    sorted_global_bi_grams = sorted(global_bi_grams.items(), key=operator.itemgetter(1), reverse=True)
    MIN_BIGRAM_COUNT = 13
    sorted_global_bi_grams = [word for word in sorted_global_bi_grams if word[1] >= MIN_BIGRAM_COUNT]
    return sorted_global_bi_grams


def prepare_dataset(words, bigrams, data):
    # data = data[100:110]
    print(len(words))
    print(len(bigrams))
    data['Review'] = data['Review'].apply(str.replace, args=["[^a-zA-Z']|_", " "])

    print('adding words...')

    for index, word in words.iterrows():
        data[word['Word']] = data['Review'].apply(str.count, args=[word['Word']])

    print('adding bigrams...')

    for index, bigram in bigrams.iterrows():
        data[bigram['Bigram']] = data['Review'].apply(str.count, args=[bigram['Bigram']])
    return data.drop('Age', axis=1)


def write_dataset(df):
    DATASET_LENGTH = 6000
    df = df.sample(DATASET_LENGTH)
    words_wieghted = pd.DataFrame.from_csv('out/weighted_words.csv')
    bigrams_weighted = pd.DataFrame.from_csv('out/weighted_bigrams.csv')
    MIN_WEIGHT_WORD = 1
    MIN_COUNT_WORD = 3

    MIN_WEIGHT_Bi = 1.7
    MIN_COUNT_Bi = 2
    dataset = prepare_dataset(
        words_wieghted[
            (abs(words_wieghted['Weight']) >= MIN_WEIGHT_WORD) & (words_wieghted['Count'] >= MIN_COUNT_WORD)],
        bigrams_weighted[
            (abs(bigrams_weighted['Weight']) >= MIN_WEIGHT_Bi) & (bigrams_weighted['Count'] >= MIN_COUNT_Bi)],
        df)
    dataset = dataset.drop(['Rating', 'Reason', 'Side Effects', 'Comments', 'Duration/Dosage', 'Drug Name', 'Review'],
                           axis=1).sample(DATASET_LENGTH)
    print('writing file...')
    dataset.to_csv('out/dataset.csv')
    print(dataset.columns)


def parse_and_write_words():
    words = count_words(df)
    words_df = pd.DataFrame(words)
    words_df.columns = ['Word', 'Count']
    words_df.to_csv('out/words.csv')


def parse_and_write_bigrams():
    bigrams = count_bi_grams(df)
    bigrams_df = pd.DataFrame(bigrams)
    bigrams_df.columns = ['Bigram', 'Count']
    bigrams_df.to_csv('out/bigrams.csv')


def get_and_weight_words():
    words_from = pd.DataFrame.from_csv('out/words.csv')
    words_from["Weight"] = words_from['Word'].apply(tf_idf)
    words_from["Weight_Abs"] = words_from['Weight'].apply(abs)
    # scaler = preprocessing.MaxAbsScaler()
    # words_from["Weight_Scaled"] = scaler.fit_transform(words_from['Weight'])
    words_from.sort_values('Weight_Abs', axis=0, inplace=True)
    return words_from


def get_and_weight_bigrams():
    bigrams = pd.DataFrame.from_csv('out/bigrams.csv')
    bigrams["Weight"] = bigrams['Bigram'].apply(tf_idf)
    bigrams["Weight_Abs"] = bigrams['Weight'].apply(abs)
    # scaler = preprocessing.MaxAbsScaler()
    # words_from["Weight_Scaled"] = scaler.fit_transform(words_from['Weight'])
    bigrams.sort_values('Weight_Abs', axis=0, inplace=True)
    return bigrams


def load_df():
    df = pd.DataFrame.from_csv('out/merged_input.csv', parse_dates=False)
    df['Review'] = df['Comments'] + ' ' + df['Side Effects']

    df = df.drop(['Date Added'], axis=1)
    df = df.dropna()
    df['Review'] = df['Comments'] + ' ' + df['Side Effects']
    return df


df = load_df()

m_rev = df[df['Sex'] == 'M']['Review']
f_rev = df[df['Sex'] == 'F']['Review']

m_rev_len = len(m_rev)
f_rev_len = len(f_rev)

m_rev_concat = " ".join(m_rev)
f_rev_concat = " ".join(f_rev)


def tf_idf(word):
    w = word
    # c = word['Count']
    num = f_rev_len * m_rev_concat.count(w)
    den = m_rev_len * f_rev_concat.count(w)
    if den == 0 or num == 0:
        return 0
    com = float(num) / den
    # res = c * math.log(com)
    res = math.log(com)

    print(word, res)
    return res


write_dataset(df)

# bigrams = get_and_weight_bigrams()
# bigrams.to_csv('out/weighted_bigrams.csv')
# write_dataset(df)
# dataset = pd.DataFrame.from_csv('out/dataset.csv')
# print(dataset.head())
