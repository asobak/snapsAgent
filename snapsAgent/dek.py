from random import shuffle
import karte
class Dek:
    def __init__(self):
        self.karte = []
        for j in range(4):
            for i in range(10, 15):
                self.karte\
                    .append(karte.Karta(i,
                                 j))
        shuffle(self.karte)

    def vuciKartu(self):
        if len(self.karte) == 0:
            return
        return self.karte.pop()

