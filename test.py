#!/usr/bin/env python
import unittest
import lm
import client
import server
import multiprocessing
import json

TEST_DATA = {
    'en': 'how are you doing?',
    'fr': 'comment allez-vous?',
    'de': 'wie geht es ihnen?'
}


class TestLanguageModelMethods(unittest.TestCase):

    def test_detect(self):
        model = lm.LanguageModel()
        for test_language, test_sentence in TEST_DATA.iteritems():
            detected_language, score = model.detect(test_sentence)
            self.assertEqual(detected_language, test_language)
            self.assertLess(score, 0)


class TestServer(unittest.TestCase):

    def setUp(self):
        self.port = 8001
        s = server.make_server('', self.port, server.app)
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

if __name__ == '__main__':
    unittest.main()
