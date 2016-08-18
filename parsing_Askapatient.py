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
    r = requests.get('http://hideme.ru/proxy-list/')
    rex = re.compile("<td class=tdl>((\d{1,4}\.){3}\d{1,4})<\/td><td>(\d{2,4})<\/td>")
    proxies = [proxy[0] + ':' + proxy[2] for proxy in rex.findall(r.text)]
    # with open('proxy.txt', 'rb') as uaf:
    #     for ua in uaf.readlines():
    #         if ua:
    #             proxies.append(ua.strip())
    random.shuffle(proxies)
    print(proxies)
    return proxies


def get_response(url, user_agents, proxies, keyword='table'):
    MAX_WAIT = 10
    headers = {
        'user-agent': random.choice(user_agents),
        "Connection": "close",
        'Cookie': '__utmz=183609910.1471172088.1.1.utmccn=(referral)|utmcsr=google.ru|utmcct=/|utmcmd=referral; ASPSESSIONIDSQQASABD=GCNIDKCBGNHPANIIEBJEMHAF; ASPSESSIONIDSQQBQCBC=GILLBGPBDNEMPKDDCLNAMDAG; __utma=183609910.1338363169.1471172088.1471450935.1471454680.8; __utmc=183609910; D_ZID=8D3FB4D9-86DF-3264-82D0-668C3F6A67EE; D_ZUID=02E07275-D545-34AF-8D38-C3ACAB8E30DE; __utmb=183609910; __atuvc=24%7C33; __atuvs=57b49dd7766c2847002; D_PID=F3F1AE20-D4CC-33C3-854A-1209E349330F; D_IID=B1C87246-9BAF-3781-BEE4-5476591A3FE5; D_UID=B4B3E55C-D8D3-37AD-B93F-109962C5AE57; D_HID=qhMWGl7HlD7aRi4u8LUWqHMzjnlB5iHb0l3s0PJ1wxc'
    }

    proxy = random.choice(proxies)
    r = None

    while True:
        try:
            # print('parsing ' + url[-1] + ' ' + proxy)
            r = requests.get(url, proxies={'http': proxy}, headers=headers, timeout=3)
            if not keyword in r.text:
                raise Exception()
            sleep(MAX_WAIT * random.random())
            break
        except:
            print('proxy failed')
            proxies.remove(proxy)
            if not proxies:
                print('reloading proxies...')
                proxies = LoadProxies()
            proxy = random.choice(proxies)

    return r, proxies


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
    outpath = '/Users/evdodima/workspace/Python/ML/out'
    links.to_csv(outpath + '/' + "links.csv")
