import string
import requests
import random
import re
import bs4 as BeautifulSoup
import pandas as pd
from time import sleep

letters = string.ascii_uppercase[:]

url = 'http://webcache.googleusercontent.com/search?q=cache:http://www.askapatient.com/drugalpha.asp?letter=%s'
urls = [url % s for s in letters]


def LoadUserAgents(uafile='user_agents.txt'):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)
    return uas


def LoadProxies():
    # r = requests.get('http://hideme.ru/proxy-list/')
    # rex = re.compile("<td class=tdl>((\d{1,4}\.){3}\d{1,4})<\/td><td>(\d{2,4})<\/td>")
    # proxies = [proxy[0] + ':' + proxy[2] for proxy in rex.findall(r.text)]
    proxies = []
    with open('proxy.txt', 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                proxies.append(ua.strip())
    random.shuffle(proxies)
    return proxies

proxies = LoadProxies()

def get_response(url, user_agents, proxy, keyword='table'):
    MAX_WAIT = 7
    headers = {
        'user-agent': random.choice(user_agents),
        "Connection": "close"
    }

    r = None
    while True:
        try:
            print(proxy)
            r = requests.get(url, proxies={'http': proxy}, headers=headers, timeout=3)

            print(r.status_code)
            r.raise_for_status()

            if not keyword in r.text:
                print(keyword + " not present")
                raise Exception()
            # sleep(MAX_WAIT * random.random())
            # proxies.append(proxy)
            break

        except requests.exceptions.HTTPError as e:
            # Need to check its an 404, 503, 500, 403 etc.
            status_code = e.response.status_code
            if status_code == 404:
                print("breaking")
                proxy = random.choice(proxies)
                break
            else:
                proxy = random.choice(proxies)
                proxies.remove(proxy)

        except:
            # print('proxy failed')
            proxy = random.choice(proxies)
            # proxies.remove(proxy)
            headers['user-agent'] = random.choice(user_agents)

    return r, proxy


if __name__ == '__main__':
    user_agents = LoadUserAgents()
    proxies = LoadProxies()
    proxy = random.choice(proxies)
    links = pd.DataFrame()
    for url in urls:
        r = get_response(url, user_agents, proxies, keyword='table')
        soup = BeautifulSoup.BeautifulSoup(r.text)
        rows = soup.find('table').findAll('tr')[1:]
        links = links.append(
            ([[row.find('a').string, 'http://www.askapatient.com/' + row.find('a').get('href')] for row in rows])
            , ignore_index=True)
        print(links.tail())

    links.columns = ['name', 'url']
    outpath = '/out'
    links.to_csv(outpath + '/' + "links.csv")
