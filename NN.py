import math

"""
Trida predstavuje klasifikator s nejblizsi vzdalenosti. Tride je predan objekt predstavujici priznakovou metodu s natrenovanymi
klasifikacnimi tridami a mnozina dokumentu pro testovani.
"""


class NN:

    def __init__(self, priznakova_metoda):
        self.prizn = priznakova_metoda

    def classify(self, test_file):
        """
        Metoda vezme jednotlive dokumenty a postupne je klasifikuje do klasifikacnich trid.
        :param test_file: Mnozina testovanych dokumentu
        """
        path = test_file.strip()
        file = open(path, encoding='utf8')
        accurancy = 0
        filecount = 0
        for line in file:
            filecount += 1
            path = line.strip()
            test_file = open(path, encoding='utf8')
            right_tags = test_file.readline().strip().split()
            test_file.__next__()
            content = test_file.readline()
            content = self.prizn.tokenize(content)
            filec = self.vectorize_content(content)
            selected = {}
            for klas in self.prizn.klas_tridy:
                distance = 0.0
                wrdc = 0.0
                for wrd in filec:
                    if wrd in self.prizn.klas_tridy[klas]:
                        wrdc += 1.0
                        distance += abs(float(filec[wrd]) - float(self.prizn.klas_tridy[klas][wrd]))
                if wrdc > 0:
                    if self.prizn.name == "tfidf":
                        selected[klas] = float(distance) * float(wrdc)
                    else:
                        selected[klas] = float(distance) / float(wrdc)

            # Vypis nejpravdepodobnejsich klasifikacnich trid.
            max_class = ""
            for i in range(len(right_tags)):
                if len(selected) == 0:
                    klas = "kul"
                else:
                    klas = max(selected, key=lambda k: selected[k])
                max_class = max_class + " " + klas
                if klas in right_tags:
                    accurancy += 1
                if len(selected) != 0:
                    del selected[klas]

            print("%s: %s\n" % (path, max_class))
        accurancy = (accurancy / filecount) * 100
        print(accurancy)

    def vectorize_content(self, content):
        """
        Metoda vytvori slovnik pro zadany text. Tedy slova vyskytujici se v textu a jejich cetnost
        :param content: Text ze ktereho se ma slovnik vytvorit
        :return: vytvoreny slovnik.
        """
        file_dict = {}
        for word in content:
            if word in file_dict:
                file_dict[word] += 1
            else:
                file_dict[word] = 1
        return file_dict

    def classif(self, text):
        """
        Metoda je velmi podobna metoda classify, ale je pouzivana pro klasifikaci jen jedne vety. Pouziva se ve spusteni s GUI
        :param text: text ktery ma byt klasifikovan.
        """
        content = self.prizn.tokenize(text)
        filec = self.vectorize_content(content)
        selected = {}
        for klas in self.prizn.klas_tridy:
            distance = 0.0
            wrdc = 0.0
            for wrd in filec:
                if wrd in self.prizn.klas_tridy[klas]:
                    wrdc += 1.0
                    distance += abs(float(filec[wrd]) - float(self.prizn.klas_tridy[klas][wrd]))
            if wrdc > 0:
                selected[klas] = float(distance) / float(wrdc)

        max_class = ""
        for i in range(0, 3):
            klas = max(selected, key=lambda k: selected[k])
            max_class = max_class + " ," + klas
            del selected[klas]

        return max_class
