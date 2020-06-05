import sys
import os.path
from tkinter import *
import json

from NGram import NGram
from NaiveBayes import NaiveBayes
from BagOfWords import BagOfWords
from TfIdf import TfIdf
from NN import NN

"""
Hlavni trida programu. Kontroluje vstupni argumenty a vola jednotlive metody pro tvorbu priznaku a klasifikaci.
"""


class Main:

    def __init__(self):
        self.version = "1.0.0"
        self.tran_file = ""
        self.test_file = ""
        self.classif = ""
        self.modelname = ""
        self.top = Tk()
        self.text1 = Text(self.top, height=15, width=60)
        self.label = Label(self.top, text="")
        self.priz_metoda = None
        self.klasifikator = None
        pass

    def check_arguments(self):
        """
        Metoda zkontroluje delku vstupnich argumentu a na jejich zaklade spusti GUI s modelem, nebo normalni beh programu.
        """
        if sys.argv.__len__() > 3:
            self.load_from_parametres()
            self.priz_metoda.load_words(self.classif, self.tran_file)
            self.klasifikator.classify(self.test_file)
            self.zapis_model(self.modelname)

        else:
            if os.path.isfile(sys.argv[1]):
                self.load_from_model(sys.argv[1])
            else:
                print("Model neexistuje")
                sys.exit(-1)

    def load_from_parametres(self):
        """
        Metoda kontroluje vstupni parametry a prirazuje je do patricnych promennych.
        """
        if os.path.isfile(sys.argv[1]):
            self.classif = sys.argv[1]
        else:
            print("Zadany parametr pro klasifikacni tridy neni souborem")
            sys.exit(-1)

        if os.path.isfile(sys.argv[2]):
            self.tran_file = sys.argv[2]
        else:
            print("Zadany parametr pro trenovaci mnozinu neni souborem")
            sys.exit(-1)

        if os.path.isfile(sys.argv[3]):
            self.test_file = sys.argv[3]
        else:
            print("Zadany parametr pro testovaci mnozinu neni souborem")
            sys.exit(-1)

        if sys.argv[4] == "bow":
            self.priz_metoda = BagOfWords()
        elif sys.argv[4] == "tfidf":
            self.priz_metoda = TfIdf()
        elif sys.argv[4] == "ngram":
            self.priz_metoda = NGram()
        else:
            print("Neznama priznakova metoda")
            sys.exit(-1)

        if sys.argv[5] == "bayes":
            self.klasifikator = NaiveBayes(self.priz_metoda)
        elif sys.argv[5] == "nn":
            self.klasifikator = NN(self.priz_metoda)
        else:
            print("Neznamy klasifikator")
            sys.exit(-1)

        self.modelname = sys.argv[6]

    def load_from_model(self, model_name):
        """
        Metoda nacita z predaneho modelu jednotlive slovniky klasifikacnich trid a spoustí GUI, ceka na stisk tlacitka a pote klasifikuje zadanou vetu.
        :param model_name: model ze ktereho se maji nacist jednotliva data.
        """

        with open(model_name, "r") as read_file:
            json_load = json.load(read_file)
            if json_load["namepriz"] == "BagOfWords":
                self.priz_metoda = BagOfWords()
            elif json_load["namepriz"] == "TfIdf":
                self.priz_metoda = TfIdf()
            elif json_load["namepriz"] == "NGram":
                self.priz_metoda = NGram()

            self.priz_metoda.words = json_load["words"]
            self.priz_metoda.klas_tridy = json_load["klas_tridy"]
            self.priz_metoda.prior = json_load["prior"]

            if json_load["nameklas"] == "NaiveBayes":
                self.klasifikator = NaiveBayes(self.priz_metoda)
            elif json_load["nameklas"] == "NN":
                self.klasifikator = NN(self.priz_metoda)

        self.top.title("Classify")
        self.top.geometry('400x300')
        buttonCommit = Button(self.top, height=1, width=10, text="Commit",
                              command=lambda: self.retrieve_input())
        self.text1.pack()
        buttonCommit.pack()
        self.label.pack()
        self.top.mainloop()

    def zapis_model(self, model_file):
        """
        Metoda zapisuje data z pripraveneho modelu do .json souboru pro dalsi spusteni.
        :param model_file: nazev souboru do ktereho se ma model ulozit
        """
        with open(model_file, "w") as write_file:
            json.dump(
                {"namepriz": self.priz_metoda.__class__.__name__, "nameklas": self.klasifikator.__class__.__name__,
                 "words": self.priz_metoda.words, "klas_tridy": self.priz_metoda.klas_tridy,
                 "prior": self.priz_metoda.prior}, write_file)
            write_file.close()

    def retrieve_input(self):
        """
        Metoda obstarava stisk tlacitka Classify z GUI aplikace.
        """
        inputValue = self.text1.get("1.0", "end-1c")
        if inputValue == '':
            self.text1.insert(INSERT, "Zadejte text pro klasifikaci\n")
        else:
            vysl = self.klasifikator.classif(inputValue)
            self.label['text'] = vysl

    def run(self):
        self.check_arguments()


def main():
    main = Main()
    main.run()


if __name__ == "__main__":
    main()
