#!/usr/bin/python
import urllib2
import urllib


def send_request(text, address='127.0.0.1', port=8001):
    params = urllib.urlencode({'text': text})
    request = urllib2.Request(
        "http://{0}:{1}".format(address, port),
        data=params,
        headers={"Accept": "application/json"})
    f = urllib2.urlopen(request)
    return f.read()
