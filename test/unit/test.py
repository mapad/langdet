#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import lm
import json
import decoder

TRAINING_DATA = {
    'en': 'training',
    'fr': 'entraînement'}

TEST_DATA = {
    'en': 'jumping',
    'fr': 'sportivement'}

# Language models trained on word 'training' and 'entraînement'
FAKE_LM = {
    'en': {('<s>', 't', 'r'): 1,
           ('t', 'r', 'a'): 1,
           ('i', 'n', 'g'): 1,
           ('<s>', '<s>', 't'): 1,
           ('a', 'i', 'n'): 1,
           ('n', 'i', 'n'): 1,
           ('r', 'a', 'i'): 1,
           ('i', 'n', 'i'): 1},
    'fr': {('e', 'n', 't'): 2,
           ('\xc3', '\xae', 'n'): 1,
           ('<s>', 'e', 'n'): 1,
           ('n', 't', 'r'): 1,
           ('t', 'r', 'a'): 1,
           ('m', 'e', 'n'): 1,
           ('a', '\xc3', '\xae'): 1,
           ('r', 'a', '\xc3'): 1,
           ('n', 'e', 'm'): 1,
           ('<s>', '<s>', 'e'): 1,
           ('\xae', 'n', 'e'): 1,
           ('e', 'm', 'e'): 1}
        }


class TestLanguageModelMethods(unittest.TestCase):

    def setUp(self):
        self.model = lm.LanguageModel()

    def test_count(self):
        """ check all trigrams are properly counted """
        self.model.count('en', 'training')
        self.assertEqual(self.model.LM['en'], FAKE_LM['en'])

    def test_normalize(self):
        """ check all trigrams occurences are properly normalized """
        self.model.normalize()
        import math
        N = len('training')
        self.assertEqual(self.model.LM['en'].values(),
                         [math.log10(1.0 / N)] * N)



class TestSimpleDecoder(unittest.TestCase):
    def setUp(self):
        lm.LanguageModel.LM = FAKE_LM
        language_model = lm.LanguageModel()
        self.simple_decoder = decoder.SimpleDecoder(language_model)

    def test_detect(self):
        for test_language, test_sentence in TEST_DATA.iteritems():
            detected_language, score = self.simple_decoder.detect(
                test_sentence)
            self.assertEqual(detected_language, test_language)
            self.assertLess(score, 0)
