import string
import lxml.html as html
import requests

letters = string.ascii_uppercase[:]

url = 'http://webcache.googleusercontent.com/search?q=cache:http://www.askapatient.com/drugalpha.asp?letter=%s'
urls = [url % s for s in letters]

alpha_pages = [requests.get(url) for url in urls]
alpha_pages = [html.document_fromstring(page.text) for page in alpha_pages]

print(html.tostring(alpha_pages[0]))
