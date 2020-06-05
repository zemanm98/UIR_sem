import re
import unidecode

klas_tridy = "klas_tridy"

"""
Trida predstavuje priznakovou metodu Bag of words. Predanou mnozinu trenovacich dat rozdeli na slovniky s cetnostmi pro jednotlive 
klasifikacni tridy nactene z predaneho souboru.
"""


class BagOfWords:

    def __init__(self):
        self.name = "bow"
        self.words = {}
        self.klas_tridy = {}
        self.prior = {}

    def load_words(self, filenameklas, filenametest):
        """
        Metoda naplni jednotlive slovniky tridy potrebnymi daty. Vytvori slovnik pro celou trenovaci mnozinu a pro jednotlive
        klasifikacni tridy. Dale spocita priority pro klasifikacni tridy ( pouzivane v Naivnim Bayesove klasifikatoru).
        :param filenameklas: parametr urcuje soubor ve kterem jsou zapsany vsechny klasifikacni tridy
        :param filenametest: soubor s cestami k jednotlivym trenovacim dokumentum
        """
        fklas = open(filenameklas, encoding='utf8')
        file_count = 0
        for line in fklas:
            self.klas_tridy[line.strip()] = {}
            self.prior[line.strip()] = 0

        f = open(filenametest, encoding='utf8')
        for line in f:
            file_count += 1
            path = line.strip()
            fil = open(path, encoding='utf8')
            first_line = fil.readline().strip().split()
            fil.__next__()
            content = fil.readline().strip().split()
            content = self.words_filter(content)
            for word in content:  # Pro kazde slovo v trenovacim dokumentu se zjisti jeho pritomnost v celkovem slovniku a slovniku klasifikacnich trid
                regex = re.compile('[^ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮa-zA-Z]')
                word = regex.sub('', word)
                word = unidecode.unidecode(word)
                word = word.lower()
                if word in self.words:
                    self.words[word] = self.words[word] + 1
                else:
                    self.words[word] = 1

                for name in first_line:

                    if word in self.klas_tridy[name]:
                        self.klas_tridy[name][word] = self.klas_tridy[name][word] + 1

                    else:
                        self.klas_tridy[name][word] = 1
            for kl in first_line:
                if kl in self.prior:
                    self.prior[kl] += 1
                else:
                    self.prior[kl] = 1

            fil.close()
        # Vypocet priorit jednotlivych klasifikacnich trid
        for n in self.prior:
            self.prior[n] = (self.prior[n] / file_count)

        f.close()

    def tokenize(self, content):
        """
        Metoda rozdeli text na jednotliva slova, ktera pote vyfiltruje a zbavi nezadoucich znaku.
        :param content: Text se slovy, ktere se maji rozdelit
        :return: rozdeleny text
        """
        parsedtxt = []
        content = content.strip().split()
        content = self.words_filter(content)
        for word in content:
            word = re.sub('[(^,„"!?.“/:;%$£@{}¨´ˇ<>_]', '', word)
            word = unidecode.unidecode(word)
            word = word.lower()
            parsedtxt.append(word)

        return parsedtxt

    def words_filter(self, line):
        """
        Metoda filtruje slova v zavislosti na jejich pritomnosti v poli filter.
        :param line: Pole se slovy ktera se maji profiltrovat
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
