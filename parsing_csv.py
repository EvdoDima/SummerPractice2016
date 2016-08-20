import pandas as pd
import os
import time


def file_len(fname):
    return len(pd.DataFrame.from_csv(fname))


count = 1
start = time.time()
for i in os.listdir('out/drugs'):
    count += file_len('out/drugs/'+i)
end = time.time()
print(count, end-start)
