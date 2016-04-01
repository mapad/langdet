# -*- coding: utf-8 -*-
from collections import Counter
from collections import defaultdict
import math


class LanguageModel():
    """ Creates a trigram language model """

    # this holds several language model for each language
    LM = defaultdict(Counter)

    def count(self, language, text):
        """ this could be parallelized """

        for token in self.tokenizer(text):
            self.LM[language][token] += 1

    def normalize(self):
        """ reduce """
        for language in self.LM.keys():
            lm = self.LM[language]
            N_entries = len(lm)
            for entry, count in lm.items():
                # normalize
                lm[entry] = math.log10(lm[entry] / float(N_entries))

    def tokenizer(self, text):
        """ iterates in text with left and right context """
        history = ['<s>', '<s>']
        for character in text:
            if character in ['\\', '!', ',', ';', '.', '/', ']', '[', '?']:
                continue
            else:
                yield (history[0], history[1], character.lower())
                history.pop(0)
                history.append(character)

    def save(self, file_name):
        """ save to disk for future usage """
        raise 'not implemented'
