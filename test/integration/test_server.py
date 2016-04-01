#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import client
import server
import multiprocessing
import lm

TRAINING_DATA = {
    'en': 'training',
    'fr': 'entraînement'}

TEST_DATA = {
    'en': 'jumping',
    'fr': 'sportivement'}

class TestServer(unittest.TestCase):

    def setUp(self):
        language_model = lm.LanguageModel()
        language_model.count()
        language_model.normalize()

        port = 8001
        s = server.make_server('', port, server.app)
        self.server_process = multiprocessing.Process(target=s.serve_forever)
        self.server_process.start()

    def tearDown(self):
        self.server_process.terminate()
        self.server_process.join()
        del(self.server_process)

    def test_server(self):

        for test_language, test_sentence in TEST_DATA.iteritems():
            ret = client.send_request(test_sentence)
            detected_language = json.loads(ret)['language']
            self.assertEqual(detected_language, test_language)
