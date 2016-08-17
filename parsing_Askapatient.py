import string
import lxml.html as html
import requests
import random

letters = string.ascii_uppercase[:]

url = 'http://www.askapatient.com/drugalpha.asp?letter=%s'
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


user_agents = LoadUserAgents()
proxies = ['124.133.240.88:8080', '201.55.46.6:80', '210.101.131.231:8080', '84.28.221.68:80']
for url in urls:
    print('parsing ' + url[-1])
    proxy = random.choice(proxies)
    headers = {
        'user-agent': random.choice(user_agents),
        "Connection": "close",
        'Cookie': '__utmz=183609910.1471172088.1.1.utmccn=(referral)|utmcsr=google.ru|utmcct=/|utmcmd=referral; D_SID=178.204.169.19:ID1F7DHRP6ht486AIYwzR2IhAOQfgUTQGEFLSSXeXBA; ASPSESSIONIDSQQASABD=GCNIDKCBGNHPANIIEBJEMHAF; ASPSESSIONIDSQQBQCBC=GILLBGPBDNEMPKDDCLNAMDAG; __utma=183609910.1338363169.1471172088.1471450935.1471454680.8; __utmc=183609910; D_ZID=8D3FB4D9-86DF-3264-82D0-668C3F6A67EE; D_ZUID=02E07275-D545-34AF-8D38-C3ACAB8E30DE; __utmb=183609910; __atuvc=24%7C33; __atuvs=57b49dd7766c2847002; D_PID=F3F1AE20-D4CC-33C3-854A-1209E349330F; D_IID=B1C87246-9BAF-3781-BEE4-5476591A3FE5; D_UID=B4B3E55C-D8D3-37AD-B93F-109962C5AE57; D_HID=qhMWGl7HlD7aRi4u8LUWqHMzjnlB5iHb0l3s0PJ1wxc'
    }
    r = requests.get(url, proxies={'http': proxy}, headers=headers)
    page = html.fromstring(r.text)
    print(html.tostring(page))

# alpha_pages = [requests.get(url) for url in urls]
# alpha_pages = [html.document_fromstring(page.text) for page in alpha_pages]

# print(html.tostring(alpha_pages[0]))
