#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import lm
import json
import decoder
from testing_data import *

class TestLanguageModelMethods(unittest.TestCase):

    def test(self):

        self.model = lm.LanguageModel()

        # test count()
        for language, text in TRAINING_DATA.items():
            self.model.count(language, text)
        self.assertEqual(self.model.LM['en'], FAKE_LM['en'])

        # test normalize()
        self.model.normalize()
        import math
        N = len('training')
        self.assertEqual(self.model.LM['en'],
                         FAKE_LM_NORMALIZED['en'])

        # test save() and load()
        import tempfile
        import os
        file_name = tempfile.mktemp()
        self.model.save(file_name)
        self.model.LM = {}
        self.model.load(file_name)
        os.unlink(file_name)
        self.assertEqual(self.model.LM['en'], FAKE_LM_NORMALIZED['en'])

class TestSimpleDecoder(unittest.TestCase):
    def setUp(self):
        model = lm.LanguageModel()
        model.LM = FAKE_LM_NORMALIZED
        self.simple_decoder = decoder.SimpleDecoder(model)

    def test_detect(self):
        for test_language, test_sentence in TEST_DATA.iteritems():
            detected_language, score = self.simple_decoder.detect(
                test_sentence)
            self.assertEqual(detected_language, test_language)
            self.assertLess(score, 0)
