import requests
headers = {
    'Host': 'coomer.party',
    'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8 rv:4.0; sl-SI) AppleWebKit/533.48.7 (KHTML, like Gecko) Version/5.0 Safari/533.48.7',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Postman-Token': '9937706e-6c0b-440d-aa3e-8dc6cc60c249',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}
import pycurl
import certifi
from io import BytesIO
import json
import threading
import requests

# buffer = BytesIO()
# c = pycurl.Curl()
# c.setopt(c.URL, 'https://coomer.party/api/onlyfans/user/cosplayers.momodayo')
# c.setopt(c.WRITEDATA, buffer)
# c.setopt(c.CAINFO, certifi.where())
# c.perform()
# c.close()

# body = json.loads(buffer.getvalue())
# Body is a byte string.
# We have to know the encoding in order to print it to a text file
# such as standard output.
# print(body)
# /d7/c7/d7c7aa652d69b552a0e58e5bc30d85e68832977c900e6f3279d7c6b44686b64f.m4v
# r = requests.get("https://coomer.party/api/onlyfans/user/cosplayers.momodayo").json()



# import requests

from clint.textui import progress
# url = "https://coomer.party/api/onlyfans/user/cosplayers.momodayo"
url = 'https://coomer.party/d7/c7/d7c7aa652d69b552a0e58e5bc30d85e68832977c900e6f3279d7c6b44686b64f.m4v'

# with open('python.m4v', 'wb') as f:
#     cl = pycurl.Curl()
#     cl.setopt(cl.URL, url)
#     cl.setopt(pycurl.COOKIE,  '__ddg2: mionaganoharaisbestgirl')
#     cl.setopt(pycurl.HTTPHEADER, ['User-Agent: User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/34.0'])
#     cl.setopt(cl.WRITEDATA, f)
#     cl.perform()
#     cl.close()

# import requests
from requests import Session
cookies = {}
def get_ddg_cookies(url):
    global cookies
    r = requests.get('https://check.ddos-guard.net/check.js', headers = {
        'referer': url
    })
    r.raise_for_status()
    cookies = r.cookies.get_dict()
    return r.cookies.get_dict()['__ddg2']

# k = requests.get(url, cookies = { '__ddg2': get_ddg_cookies('https://coomer.party') })
# print(k.raise_for_status())
# print(k.text)

s = Session()
s.max_redirects = 100
get_ddg_cookies('https://coomer.party')
print(cookies)
r = s.get(url, stream=True, cookies = cookies)
# print(r.text)
with open("python.m4v", "wb") as Pypdf:

    total_length = int(r.headers.get('content-length'))

    for ch in progress.bar(r.iter_content(chunk_size = 1024), expected_size=(total_length/1024) + 1):

        if ch:

            Pypdf.write(ch)


# data = []
# for a in body:
#     tgl = a['published'].split(" ")
#     filetype = ""
#     if "path" in a['file'] and str(a['file']['path']).find("m4v") != -1:
#         filetype = "m4v"

#     print (tgl[1], tgl[2], tgl[3])
#     print(filetype)
#     print()