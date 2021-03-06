import random
import unicodedata

import bs4 as BeautifulSoup
import numpy as np
import pandas as pd

from old.parsing_Askapatient import LoadUserAgents, get_response, LoadProxies


def get_table(r):
    data = []
    soup = BeautifulSoup.BeautifulSoup(r.text, "lxml")
    table = soup.find('table', {'class': 'ratingsTable'})
    cells = table.findAll('td')
    for cell in cells:
        if 'td bgcolor' in str(cell):
            cell_data = cell.text.replace(',', '_').replace('\n', '').replace('\r','')
            data.append(unicodedata.normalize('NFKD', cell_data))
    return data


user_agents = LoadUserAgents()
proxies = LoadProxies()
proxy = random.choice(proxies)

links = pd.read_csv('out/links.csv')
# http://webcache.googleusercontent.com/search?q=cache:
links['url'] = 'http://www.askapatient.com/' + links['url'] + "&page=1&PerPage=10000"

outpath = 'out/drugs'

links = links[:1650]
links = links[::-1]

for index, link in links.iterrows():
    print(str(index) + ' - ' + link['url'])
    r, succProxy = get_response(link['url'], user_agents, proxy, keyword='ratingsTable')
    proxy = succProxy

    if r:

        data = get_table(r)
        data = np.array(data)
        try: 
            data = np.reshape(data, (-1, 8))
        except: 
            continue

        df = pd.DataFrame(data=data,
                          columns=['Rating', 'Reason', 'Side Effects', 'Comments',
                                   'Sex', 'Age', 'Duration/Dosage', 'Date Added'])
        df['Drug Name'] = link['name'].capitalize()

        # Save comments for individual drug as csv
        df.to_csv(outpath + '/' + link['name'].replace('/', '_') + '.csv', encoding='utf-8')
