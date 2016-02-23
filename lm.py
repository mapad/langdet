# -*- coding: utf-8 -*-
from collections import Counter
import math

english_text="""English is a West Germanic language that was first spoken in early medieval England and is now the most widely used language in the world.[4] It is spoken as a first language by the majority populations of several sovereign states, including the United Kingdom, the United States, Canada, Australia, Ireland, New Zealand and a number of Caribbean nations; and it is an official language of almost 60 sovereign states. It is the third-most-common native language in the world, after Mandarin Chinese and Spanish.[5] It is widely learned as a second language and is an official language of the European Union, many Commonwealth countries and the United Nations, as well as in many world organisations.
English arose in the Anglo-Saxon kingdoms of England and what is now southeast Scotland. Following the extensive influence of Great Britain and the United Kingdom from the 17th to mid-20th centuries through the British Empire, it has been widely propagated around the world.[6][7][8][9] Through the spread of American-dominated media and technology,[10] English has become the leading language of international discourse and the lingua franca in many regions.[11][12]
Historically, English originated from the fusion of closely related dialects, now collectively termed Old English, which were brought to the eastern coast of Great Britain by Germanic settlers (Anglo-Saxons) by the 5th century; the word English is derived from the name of the Angles,[13] and ultimately from their ancestral region of Angeln (in what is now Schleswig-Holstein). The language was also influenced early on by the Old Norse language through Viking invasions in the 9th and 10th centuries."""

french_text="""Le français est une langue indo-européenne de la famille des langues romanes. Le français s'est formé en France (variété de la « langue d’oïl ») et est aujourd'hui parlé sur tous les continents par environ 220 millions de personnes dont 115 millions de locuteurs natifs1, auxquels s'ajoutent 72 millions de locuteurs partiels (évaluation Organisation internationale de la francophonie : 2010). Elle est une des six langues officielles et une des deux langues de travail (avec l’anglais) de l’Organisation des Nations unies, et langue officielle ou de travail de plusieurs organisations internationales ou régionales, dont l’Union européenne. Après avoir été à l’époque de l’Ancien Régime français la langue des cours royales et princières, des tsars de Russie aux rois d’Espagne et d'Angleterre en passant par les princes de l’Allemagne, elle demeure une langue importante de la diplomatie internationale aux côtés de l’anglais, de l'allemand et de l’espagnol.
La langue française est un attribut de souveraineté en France, depuis 1992 « la langue de la République est le français » (article 2 de la Constitution de la Cinquième République française). Elle est également le principal véhicule de la pensée et de la culture française dans le monde. La langue française fait l’objet d’un dispositif public d’enrichissement de la langue, avec le décret du 3 juillet 1996 relatif à l'enrichissement de la langue française.
La langue française a cette particularité que son développement et sa codification ont été en partie l’œuvre de groupes intellectuels, comme la Pléiade, ou d’institutions, comme l’Académie française. C’est une langue dite « académique ». Toutefois, l’usage garde ses droits et nombreux sont ceux qui malaxèrent cette langue vivante, au premier rang desquels Rabelais et Molière : il est d’ailleurs question de la « langue de Molière »4."""

german_text="""Unter dem Begriff „deutsche Sprache“ wird heute die auf der Grundlage von mitteldeutschen und oberdeutschen Mundarten entstandene deutsche Standardsprache (Standard-Hochdeutsch) verstanden sowie diejenigen Mundarten des kontinentalwestgermanischen Dialektkontinuums, die ganz oder teilweise von dieser überdacht werden.
Zum Deutschen werden darüber hinaus die historischen Vorgängersprachen Althochdeutsch (Sprachcodes nach ISO 639-2 & 639-3: goh) und Mittelhochdeutsch (Sprachcodes nach ISO 639-2 & 639-3: gmh) gezählt sowie neuere umgangssprachliche Varietäten oder Mischsprachen (z. B. Missingsch) innerhalb des Geltungsbereiches der deutschen Standardsprache.
Das Luxemburgische sowie manche Auswandererdialekte (z. B. Pennsylvania Dutch) oder Übergangsdialekte (z. B. Kollumerpompsters), die zwar auf Varietäten innerhalb des Dialektkontinuums der deutschen Mundarten zurückgehen, jedoch heute nicht oder nur in eingeschränktem Maße von der deutschen Standardsprache überdacht werden, können hingegen auf synchroner Ebene nicht zum „Deutschen“ im engeren Sinne des Wortes gerechnet werden.
Das Jiddische, das ursprünglich auf das Mittelhochdeutsche zurückgeht, sich jedoch vor allem unter slawischen und hebräischen Einflüssen eigenständig weiterentwickelt und eine eigene Schriftsprache ausgebildet hat, und die lexikalisch auf dem Deutschen basierende Kreolsprache Unserdeutsch werden hingegen heute in der Sprachwissenschaft im Allgemeinen nicht zum Deutschen gerechnet, sondern als eigenständige Sprachen betrachtet"""


class LanguageModel():
    """ Creates a trigram language model """
    LM = {}

    def __init__(self, train={'fr': french_text, 'en': english_text,
                              'de': german_text}):
        for language, text in train.items():
            # count occurence of tokens
            lm = Counter()
            for token in self.tokenizer(text):
                lm[token] += 1
            self.LM[language] = lm

            # normalize language model
            N_entries = len(lm)
            for entry, count in lm.items():
                lm[entry] = math.log10(lm[entry] / float(N_entries))

    def tokenizer(self, text):
        history = ['<s>', '<s>']
        for character in text:
            if character in ['\\', '!', ',', ';', '.', '/', ']', '[', '?']:
                continue
            else:
                yield (history[0], history[1], character.lower())
                history.pop(0)
                history.append(character)

    def probability(self, text):
        score = {}
        for language, lm in self.LM.items():
            prob = math.log(1e-88)
            for token in self.tokenizer(text):
                if token in lm:
                    prob += lm[token]
                else:
                    prob += math.log(1e-88)     # OOV prob to be set
            score[language] = prob
        return text, score

    def detect(self, text, trace=True):
        text, score = self.probability(text)
        if trace: print text, score
        return max(score.items(), key=lambda x: x[1])

