import re
import unidecode

"""
Trida predstavuje priznakovou metodu N-Gram. Predanou mnozinu trenovacich dat rozdeli na slovniky s cetnostmi pro jednotlive 
klasifikacni tridy nactene z predaneho souboru.
"""


class NGram():

    def __init__(self):
        self.name = "ngram"
        self.words = {}
        self.klas_tridy = {}
        self.prior = {}

    def load_words(self, filenameklas, filenametrain):
        """
        Metoda naplni jednotlive slovniky tridy potrebnymi daty. Vytvori slovnik pro celou trenovaci mnozinu a pro jednotlive
        klasifikacni tridy. Tyto slovniky se pak dale predavaji do metody tokenize, kde se vytvori dvojice.
        Dale spocita priority pro klasifikacni tridy ( pouzivane v Naivnim Bayesove klasifikatoru).
        :param filenameklas: parametr urcuje soubor ve kterem jsou zapsany vsechny klasifikacni tridy
        :param filenametest: soubor s cestami k jednotlivym trenovacim dokumentum
        """
        fklas = open(filenameklas, encoding='utf8')
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

    def tokenize(self, content):
        """
        Metoda rozdeli text na jednotliva slova a pomoci regularnich vyrazu je zbavi nezadoucich znacek. Pote slova spoji do dvojic.
        :param content: Text ktery se ma rozdelit
        :return: Rozdeleny text
        """
        filtered_content = []
        content = content.lower()
        content = content.strip()
        content = re.findall(r'\w+', content)
        #content = self.words_filter(content)
        bigram = []
        for word in content:
            # regex = re.compile('[^ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮa-zA-Z„,."]')
            word = unidecode.unidecode(word)
            word = word.lower()
            word = re.sub('[(^,„"!?.“/:;%$£@{}¨´ˇ<>_]', '', word)
            filtered_content.append(word)

        for i in range(len(filtered_content) - 1):
            sent = filtered_content[i] + " " + filtered_content[i + 1]
            bigram.append(sent)

        return bigram

    def words_filter(self, line):
        """
        Metoda vyfiltruje nezadouci slova.
        :param line: Text pripraveny k filtraci
        :return: vyfiltrovany text
        """
        filtered_line = []
        filter = ["nam", "pod", "vzdy", "velmi", "ta", "nas", "tomu", "ten",
                  "vse", "jsem", "zde", "tu", "kde", "ani", "jenz", "byl", "ktery",
                  "si", "tyto", "teto", "bylo", "jen", "byly", "take", "jez", "dne",
                  "tim", "jeho", "mu", "toho", "ten", "tez", "jako", "maji", "sice", "pred",
                  "proto", "ktera", "ani", "ji", "kdo", "dale", "vice", "tom", "budou", "co", "ku",
                  "byti", "bude", "bez", "vsech", "vsak", "dle", "az", "ktere", "pak", "ale", "po",
                  "jak", "jiz", "byla", "by", "jsou", "kdyz", "ze", "sve", "te", "nez", "tak", "je",
                  "tento", "od", "ma", "neb", "jeste", "na", "ve", "pro", "za", "ze", "jest", "by",
                  "aby", "do", "po", "to", "pri", "pro", "byt", "se", "a", "z", "o", "v", "k", "m", "t", "p"]

        for word in line:
            if word not in filter:
                filtered_line.append(word)

        return filtered_line
