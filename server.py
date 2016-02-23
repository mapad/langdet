#!/usr/bin/python
# -*- coding: utf-8 -*-
from wsgiservice import *
from wsgiref.simple_server import make_server
import lm

model = lm.LanguageModel()


@mount('/')
class Document(Resource):
    NOT_FOUND = (KeyError,)

    def POST(self, text):
        lang, score = model.detect(text)
        return {'language': lang}

app = get_app(globals())


def start_server(app, port=8001):
    print "Running on port {0}".format(port)
    make_server('', port, app).serve_forever()

if __name__ == '__main__':
    start_server(app, 8001)
