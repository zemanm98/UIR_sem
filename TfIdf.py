import math
import re
import unidecode

"""
Trida predstavuje priznakovou metodu TF-IDF. Predanou mnozinu trenovacich dat rozdeli na slovniky s cetnostmi pro jednotlive 
klasifikacni tridy nactene z predaneho souboru.
"""


class TfIdf:

    def __init__(self):
        self.name = "tfidf"
        self.words = {}
        self.klas_tridy = {}
        self.prior = {}

    def load_words(self, filenameklas, filenametrain):
        """
        Metoda naplni jednotlive slovniky tridy potrebnymi daty. Vytvori slovnik pro celou trenovaci mnozinu a pro jednotlive
        klasifikacni tridy. Hodnoty v techto slovnícíh pote nadhodnoti a podhodnoti v zavislosti na jejich vyskytu.
        Dale spocita priority pro klasifikacni tridy ( pouzivane v Naivnim Bayesove klasifikatoru).
        :param filenameklas: parametr urcuje soubor ve kterem jsou zapsany vsechny klasifikacni tridy
        :param filenametest: soubor s cestami k jednotlivym trenovacim dokumentum
        """
        fklas = open(filenameklas, encoding='utf8')
        count_dict = 0
        for line in fklas:
            self.klas_tridy[line.strip()] = {}
            self.prior[line.strip()] = 0

        file_count = 0
        f = open(filenametrain, encoding='utf8')
        for line in f:
            file_count += 1
            path = line.strip()
            fil = open(path, encoding='utf8')
            first_line = fil.readline().strip().split()
            fil.__next__()
            content = fil.readline()
            sentences = self.tokenize(content)
            for words in sentences:
                if words in self.words:
                    self.words[words] = self.words[words] + 1
                else:
                    self.words[words] = 1

                for name in first_line:
                    if words in self.klas_tridy[name]:
                        self.klas_tridy[name][words] = self.klas_tridy[name][words] + 1

                    else:
                        self.klas_tridy[name][words] = 1
            fil.close()
            for kl in first_line:
                if kl in self.prior:
                    self.prior[kl] += 1
                else:
                    self.prior[kl] = 1

        f.close()

        for n in self.prior:
            self.prior[n] = (self.prior[n] / file_count)
        # V techto for cyklech se urcuje nova hodnota pro kazde slovo ve slovnicich klasifikacnich trid
        for kla in self.klas_tridy:
            klas_count = 0
            for word in self.klas_tridy[kla]:
                klas_count += self.klas_tridy[kla][word]
            for word in self.klas_tridy[kla]:
                wordc = 0
                for k in self.klas_tridy:
                    if word in self.klas_tridy[k]:
                        wordc += 1

                tf = self.klas_tridy[kla][word] / len(self.klas_tridy[kla])
                idf = math.log(len(self.klas_tridy) / wordc)
                if idf == 0.0:
                    idf = 1.0
                self.klas_tridy[kla][word] = tf * idf

    def tokenize(self, content):
        """
        Metoda prevezme text a rozdeli ho na jednotliva slova
        :param content: Text ktery se ma rozdelit
        :return: rozdeleny text
        """
        parsedtxt = []
        content = content.strip().split()
        for word in content:
            word = unidecode.unidecode(word)
            word = word.lower()
            parsedtxt.append(word)

        return parsedtxt
