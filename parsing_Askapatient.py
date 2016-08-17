import string
import lxml.html as html
import requests
from time import sleep

letters = string.ascii_uppercase[:]

url = "http://www.askapatient.com/drugalpha.asp?letter=%s"
urls = [url % s for s in letters]
# http_proxies = {'http': '195.239.3.102:8080'}

# headers = {'user-agent':
#                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
#                'AppleWebKit/537.36 (KHTML, like Gecko) '
#                'Chrome/52.0.2743.116 Safari/537.36',
#            'Cookie': '__utmz=183609910.1471172088.1.1.utmccn=(referral)|utmcsr=google.ru|utmcct=/|utmcmd=referral; D_SID=178.204.169.19:ID1F7DHRP6ht486AIYwzR2IhAOQfgUTQGEFLSSXeXBA; ASPSESSIONIDSQQASABD=GCNIDKCBGNHPANIIEBJEMHAF; ASPSESSIONIDSQQBQCBC=GILLBGPBDNEMPKDDCLNAMDAG; D_ZID=CDD59694-AF6E-355B-8211-4A849669F72E; D_ZUID=2B9AAE76-333C-30DD-91FF-034BF15AD40F; __utma=183609910.1338363169.1471172088.1471410909.1471429144.6; __utmc=183609910; __utmb=183609910; __atuvc=13%7C33; __atuvs=57b43a174cc5baff001; D_PID=F3F1AE20-D4CC-33C3-854A-1209E349330F; D_IID=3FD1F270-C68F-3287-9150-60C45E0D3897; D_UID=A3E3DCE9-9CD9-36FC-8839-EB5D68162434; D_HID=wX7L6QfCd3vVDWK2A7PfqGgQeyKqZTZKbtTkHFezIlY'}

# alpha_pages = []
# for url in urls:
#     page = requests.get(url)
#     alpha_pages.append(html.document_fromstring(page.text))
#     print('parsing ' + url[-1] + '...')
#     # sleep(1.05)

alpha_pages = [requests.get(url) for url in urls]

alpha_pages = [html.document_fromstring(page.text) for page in alpha_pages]

print(html.tostring(alpha_pages[-1]))
