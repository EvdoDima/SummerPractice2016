import pandas as pd
import os
import time
import numpy as np

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


df = pd.DataFrame.from_csv('out/merged_input.csv',parse_dates=False)
df = df.drop(['Date Added','Rating'], axis=1)
# df = df.dropna()
shuffled_df = df.iloc[np.random.permutation(len(df))]

print(shuffled_df)
