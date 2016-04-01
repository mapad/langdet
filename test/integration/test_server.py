#!/usr/bin/env python
import unittest
import client
import server
import multiprocessing

class TestServer(unittest.TestCase):

    def setUp(self):
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
