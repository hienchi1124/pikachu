import urllib.request
import json
from urllib.request import Request, urlopen
import requests


def sendRequest(url):
    try:
        data = urllib.request.urlopen(url).read()
        return json.loads(data.decode("utf-8"))
    except Exception as err:
        print(str(err))

    return None


def sendRequestHttps(url):
    try:
        req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urlopen(req).read()
        return json.loads(data.decode("utf-8"))
    except Exception as err:
        print(str(err))
    return None


def sendPost(url, userName):
    try:
        data = {'input': userName}
        r = requests.post(url=url, data=data)
        return r.text.rstrip('\r\n')
    except Exception as e:
        print(e)
