import math
import unidecode
import re

"""
Trida predstavuje klasifikacni algoritmus Bag of words. Tride je predan objekt predstavujici priznakovou metodu s natrenovanymi
klasifikacnimi tridami a mnozina dokumentu pro testovani.
"""


class NaiveBayes:

    def __init__(self, pritnakova_metoda):
        self.prizn = pritnakova_metoda

    def classify(self, test_file):
        """
        Metoda vezme jednotlive dokumenty a postupne je klasifikuje do klasifikacnich trid.
        :param test_file: Mnozina testovanych dokumentu
        """
        testf = open(test_file, encoding='utf8')
        tag_count = 0
        accurancy = 0
        for file in testf:
            file = file.strip()
            probabilities = {}
            testing_file = open(file, encoding='utf8')
            right_tags = testing_file.readline().strip().split()
            tag_count += len(right_tags)
            testing_file.__next__()
            content = testing_file.readline()
            content = self.prizn.tokenize(content)
            total_features = len(self.prizn.words)
            for kla in self.prizn.klas_tridy:
                prob_kla = []
                klas_counts = 0
                for word, value in self.prizn.klas_tridy[kla].items():
                    klas_counts += value

                for word in content:
                    if word in self.prizn.klas_tridy[kla]:
                        count = self.prizn.klas_tridy[kla][word]
                    else:
                        count = 0
                    prob_kla.append(float((count + 1.0)) / float((klas_counts + total_features)))

                probabylity = 0
                for number in prob_kla:
                    probabylity += math.log(number)

                probabilities[kla] = probabylity + math.log(self.prizn.prior[kla])
            # Vypis nejpravdepodobnejsich klasifikacnich trid.
            max_class = ""
            for i in range(len(right_tags)):
                klas = max(probabilities, key=lambda k: probabilities[k])
                max_class = max_class + " " + klas
                if klas in right_tags:
                    accurancy += 1
                del probabilities[klas]

            print("%s: %s\n" % (file, max_class))
        accurancy = (accurancy / tag_count) * 100
        print(accurancy)

    def classif(self, text):
        """
        Metoda je velmi podobna metoda classify, ale je pouzivana pro klasifikaci jen jedne vety. Pouziva se ve spusteni s GUI
        :param text: text ktery ma byt klasifikovan.
        """
        probabilities = {}
        total_features = len(self.prizn.words)
        for kla in self.prizn.klas_tridy:
            prob_kla = []
            klas_counts = 0
            for word, value in self.prizn.klas_tridy[kla].items():
                klas_counts += value

            for word in text:
                if word in self.prizn.klas_tridy[kla]:
                    count = self.prizn.klas_tridy[kla][word]
                else:
                    count = 0
                prob_kla.append(float((count + 1.0)) / float((klas_counts + total_features)))

            probabylity = 0
            for number in prob_kla:
                probabylity += math.log(number)

            probabilities[kla] = probabylity + math.log(self.prizn.prior[kla])
        max_class = ""
        for i in range(0, 3):
            klas = max(probabilities, key=lambda k: probabilities[k])
            max_class = max_class + " ," + klas
            del probabilities[klas]

        return max_class
