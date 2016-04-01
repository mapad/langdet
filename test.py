#!/usr/bin/env python
import unittest
import lm
import decoder
import client
import server
import multiprocessing
import json

TEST_DATA = {
    'en': 'how are you doing?',
    'fr': 'comment allez-vous?',
    'de': 'wie geht es ihnen?'
}

TRAINING_TRIGRAMS = {('<s>', 't', 'r'): 1,
                     ('t', 'r', 'a'): 1,
                     ('i', 'n', 'g'): 1,
                     ('<s>', '<s>', 't'): 1,
                     ('a', 'i', 'n'): 1,
                     ('n', 'i', 'n'): 1,
                     ('r', 'a', 'i'): 1,
                     ('i', 'n', 'i'): 1}


class TestLanguageModelMethods(unittest.TestCase):

    def setUp(self):
        self.model = lm.LanguageModel()

    def test_count(self):
        """ check all trigrams are properly counted """
        self.model.count('en', 'training')
        self.assertEqual(self.model.LM['en'], TRAINING_TRIGRAMS)

    def test_normalize(self):
        """ check all trigrams occurences are properly normalized """
        self.model.normalize()
        import math
        N = len('training')
        self.assertEqual(self.model.LM['en'].values(),
                         [math.log10(1.0 / N)] * N)


class TestSimpleDecoder(unittest.TestCase):
    def setUp(self):
        self.simple_decoder = decoder.SimpleDecoder(lm.languageModel())

    def test_detect(self):
        for test_language, test_sentence in TEST_DATA.iteritems():
            detected_language, score = self.model.detect(test_sentence)
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

    @unittest.skip("to be updated")
    def test_server(self):

        for test_language, test_sentence in TEST_DATA.iteritems():
            ret = client.send_request(test_sentence)
            detected_language = json.loads(ret)['language']
            self.assertEqual(detected_language, test_language)

if __name__ == '__main__':
    unittest.main()
