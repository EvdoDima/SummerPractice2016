import random
import pandas as pd
import numpy as np
import bs4 as BeautifulSoup
import unicodedata
from parsing_Askapatient import LoadUserAgents, get_response, LoadProxies


def get_table(r):
    data = []
    soup = BeautifulSoup.BeautifulSoup(r.text, "lxml")
    table = soup.find('table', {'class': 'ratingsTable'})
    cells = table.findAll('td')
    for cell in cells:
        if 'td bgcolor' in str(cell):
            data.append(unicodedata.normalize('NFKD', cell.text.replace(',', '_')))
    return data


user_agents = LoadUserAgents()
proxies = LoadProxies()

links = pd.read_csv('/Users/evdodima/workspace/Python/ML/out/links.csv')
links['url'] = 'http://www.askapatient.com/' + links['url']

print(links.head())

outpath = '/Users/evdodima/workspace/Python/ML/out/drugs'

for index, link in links.iterrows():
    print(link['url'])
    r,proxies = get_response(link['url'], user_agents, proxies, keyword='ratingsTable')
    data = get_table(r)
    data = np.array(data)
    data = np.reshape(data, (-1, 8))
    df = pd.DataFrame(data=data,
                      columns=['Rating', 'Reason', 'Side Effects', 'Comments',
                               'Sex', 'Age', 'Duration/Dosage', 'Date Added'])
    df['Drug Name'] = link['name'].capitalize()

    # Save comments for individual drug as csv
    df.to_csv(outpath + '/' + link['name'].replace('/', '_') + '.csv')
