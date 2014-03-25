#!/usr/bin/python
import urllib2
import urllib

def send_request(text):
  params = urllib.urlencode({'text': text})
  request = urllib2.Request("http://127.0.0.1:8001/", data=params, headers={"Accept": "application/json"})
  f = urllib2.urlopen(request)
  print 'send text to server for identification: ', text
  print 'answer: ', f.read()

send_request('how are you doing?')
send_request('comment allez-vous?')
send_request('wie geht es ihnen?')

