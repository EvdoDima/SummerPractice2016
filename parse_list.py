import string
import requests
import random
import StringIO
import re
import BeautifulSoup as BS

# 'http://webcache.googleusercontent.com/search?q=cache:' + \
            
url = 'http://www.askapatient.com/viewrating.asp?drug=%s&name=KUKUSHKA&page=1&PerPage=10000'
urls = [] # (name, url)

with open('drugs_list.txt', 'rb') as uaf:
    for ua in uaf.readlines():
        if ua:
            comps = ua.split(',')
            urls.append((comps[0], url % comps[1].strip()))


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
    proxies = []
    with open('proxy.txt', 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                proxies.append(ua.strip())
    random.shuffle(proxies)
    return proxies



user_agents = LoadUserAgents()
proxies = LoadProxies()
proxy = random.choice(proxies)
for (name, url) in urls:
    
    headers = {
        'user-agent': random.choice(user_agents),
        "Connection": "close",
        'Cookie': '__utmz=183609910.1471172088.1.1.utmccn=(referral)|utmcsr=google.ru|utmcct=/|utmcmd=referral; D_SID=178.204.169.19:ID1F7DHRP6ht486AIYwzR2IhAOQfgUTQGEFLSSXeXBA; ASPSESSIONIDSQQASABD=GCNIDKCBGNHPANIIEBJEMHAF; ASPSESSIONIDSQQBQCBC=GILLBGPBDNEMPKDDCLNAMDAG; __utma=183609910.1338363169.1471172088.1471450935.1471454680.8; __utmc=183609910; D_ZID=8D3FB4D9-86DF-3264-82D0-668C3F6A67EE; D_ZUID=02E07275-D545-34AF-8D38-C3ACAB8E30DE; __utmb=183609910; __atuvc=24%7C33; __atuvs=57b49dd7766c2847002; D_PID=F3F1AE20-D4CC-33C3-854A-1209E349330F; D_IID=B1C87246-9BAF-3781-BEE4-5476591A3FE5; D_UID=B4B3E55C-D8D3-37AD-B93F-109962C5AE57; D_HID=qhMWGl7HlD7aRi4u8LUWqHMzjnlB5iHb0l3s0PJ1wxc'
    }

    while True: 
        try:
            print('parsing ' + url + ' ' + proxy)
            r = requests.get(url, proxies={'http': proxy}, headers=headers, timeout=5)
            soup = BS.BeautifulSoup(r.text, convertEntities=BS.BeautifulSoup.HTML_ENTITIES)
            rows = soup.find('table', {"class": "ratingsTable"}).findAll('tr')[2:]
            res = []
            for tr in rows:
                curr_row = []
                for td in tr.findAll('td'):
                    curr_row.append(str(td.string))
                res.append('^'.join(curr_row))
            print('\n'.join(res))
            break
        except (requests.exceptions.RequestException):
            proxy = random.choice(proxies)
            proxies.remove(proxy)
