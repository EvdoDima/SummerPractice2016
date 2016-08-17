import string
import lxml.html as html
import requests
import random

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


user_agents = LoadUserAgents()
for url in urls:
    print ('parsing '+url[-1])
    headers = {
        'user-agent': random.choice(user_agents),
        "Connection": "close"
    }
    r = requests.get(url, headers=headers)
    page = html.fromstring(r.text)
    print(html.tostring(page.cssselect('title').pop()))

# alpha_pages = [requests.get(url) for url in urls]
# alpha_pages = [html.document_fromstring(page.text) for page in alpha_pages]

# print(html.tostring(alpha_pages[0]))
