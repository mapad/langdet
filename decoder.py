import math
OUT_OF_VOCABULARY_PROBABILITY = 1e-88


class SimpleDecoder():
    def __init__(self, language_model):
        self.language_model = language_model

    def probability(self, text):
        """ computes joint probability of each token against Language Models"""
        score = {}
        for language, lm in self.language_model.LM.items():
            prob = math.log(OUT_OF_VOCABULARY_PROBABILITY)
            for token in self.language_model.tokenizer(text):
                if token in lm:
                    prob += lm[token]
                else:
                    prob += math.log(OUT_OF_VOCABULARY_PROBABILITY)
            score[language] = prob
        return text, score

    def detect(self, text, trace=True):
        """ returns most likely language """
        text, score = self.probability(text)
        if trace: print(text, score)
        return max(score.items(), key=lambda x: x[1])
