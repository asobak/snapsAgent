import karte
import dek
import igrac
import os
import time



class Snaps:
    
    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')


    def __init__(self):
        ime1 = input("p1 ime ")
        ime2 = input("p2 ime ")
        self.dek = dek.Dek()
        self.p1 = igrac.Igrac(ime1)
        self.p2 = igrac.Igrac(ime2)

    def igraj(self):
        while self.p1.bodovi>0 or self.p2.bodovi>0:
            self.resetirajRundu()
            while(len(self.p1.karte)!=0 and len(self.p2.karte)!=0):
                    self.nacrtajStol(None,None)               
                    if(self.odigrajKarte()!="dosta"):
                        self.izracunajRezultatKarti(self.p1OdabranaKarta,self.p2OdabranaKarta)
                       # time.sleep(3)
                        if not self.mus:
                            self.vuciJednuKartu()
                    else:              
                        break
            if self.p1.naRedu:
                if len(self.p1.karte)==0 and len(self.p2.karte)==0:
                    self.bodovi=self.provjeriRezultatKraja(True)
                self.p1.bodovi-=self.bodovi
                self.p1.dobioZadnju=True
                self.p2.dobioZadnju=False
            else:
                if len(self.p1.karte)==0 and len(self.p2.karte)==0:
                    self.bodovi=self.provjeriRezultatKraja(False)
                self.p2.bodovi-=self.bodovi
                self.p2.dobioZadnju=True
                self.p1.dobioZadnju=False
        

    def odrediPrvogIgraca(self):
        if not self.p1.dobioZadnju and not self.p2.dobioZadnju:
            self.p1.naRedu=True
        elif self.p1.dobioZadnju:
            self.p1.naRedu=True
        else:
            self.p2.naRedu=True
                
    def odigrajKarte(self):
        if(self.p1.naRedu):             
            if self.unesiAkcijuPrvi(True)=="D":
                return "dosta"
            #provjera zamjene karte aduta
            if self.p1OdabranaKarta.adut and self.p1OdabranaKarta.vrijednost==10 and len(self.dek.karte)>1 and not self.mus:
                odgovor = input("Želite li zamijeniti kartu ?(Y/N): ")
                if odgovor=="Y":                   
                    self.p1.karte.append(self.zamijeniAdutKartu(self.p1OdabranaKarta))
                    self.nacrtajStol(None,None)
                    if self.unesiAkcijuPrvi(True)=="D":
                        return "dosta"
            #provjera zvanja
            if self.p1OdabranaKarta.vrijednost==11 or self.p1OdabranaKarta.vrijednost==12:
                odgovorZvanja=self.provijeriZvanje(self.p1OdabranaKarta,True)
                if odgovorZvanja=="dosta":
                    self.bodovi=self.provjeriDosta(True)
                    if self.bodovi !=0:
                        self.nacrtajStol(self.p1OdabranaKarta,None)
                        print("Dosta")
                        time.sleep(2)
                        return "dosta"
                
            self.p1OdabranaKarta.prvi=True
            self.nacrtajStol(self.p1OdabranaKarta,None)
            
            brojOdabraneKarte = self.unesiAkcijuDrugi(True)       
            if not self.mus:
                self.p2OdabranaKarta=self.p2.karte.pop(brojOdabraneKarte-1)
                self.nacrtajStol(self.p1OdabranaKarta,self.p2OdabranaKarta)
            else:
                while 1:
                    if self.p1OdabranaKarta.boja == self.p2.karte[brojOdabraneKarte-1].boja:
                        self.p2OdabranaKarta=self.p2.karte.pop(brojOdabraneKarte-1)
                        self.nacrtajStol(self.p1OdabranaKarta,self.p2OdabranaKarta)
                        break
                    else:
                        postiva=True
                        for karta in self.p2.karte:
                            if self.p1OdabranaKarta.boja==karta.boja:        
                                postiva=False
                        if postiva:
                            if self.p2.karte[brojOdabraneKarte-1].adut:
                                self.p2OdabranaKarta=self.p2.karte.pop(brojOdabraneKarte-1)
                                self.nacrtajStol(self.p1OdabranaKarta,self.p2OdabranaKarta)
                                break
                            else:
                                postiva=True
                                for karta in self.p2.karte:
                                    if karta.adut:        
                                        postiva=False
                                        break
                                if postiva:
                                    self.p2OdabranaKarta=self.p2.karte.pop(brojOdabraneKarte-1)
                                    self.nacrtajStol(self.p1OdabranaKarta,self.p2OdabranaKarta)
                                    break
                                else:
                                    print("Morate poštivati boju!")
                                    brojOdabraneKarte = self.unesiAkcijuDrugi(False)  
                        else:
                            print("Morate poštivati boju!")
                            brojOdabraneKarte = self.unesiAkcijuDrugi(True)   
                        
                
        if(self.p2.naRedu):
            if self.unesiAkcijuPrvi(False)=="D":
                return "dosta"
            #provjera zamjene karte aduta
            if self.p2OdabranaKarta.adut and self.p2OdabranaKarta.vrijednost==10 and len(self.dek.karte)>1 and not self.mus:
                odgovor = input("Želite li zamijeniti kartu ?(Y/N): ")
                if odgovor=="Y":                   
                    self.p2.karte.append(self.zamijeniAdutKartu(self.p2OdabranaKarta))
                    self.nacrtajStol(None,None)
                    if self.unesiAkcijuPrvi(False)=="D":
                        return "dosta"
            #provjera zvanja
            if self.p2OdabranaKarta.vrijednost==11 or self.p2OdabranaKarta.vrijednost==12:
                odgovorZvanja=self.provijeriZvanje(self.p2OdabranaKarta,False)
                if odgovorZvanja=="dosta":
                    self.bodovi=self.provjeriDosta(False)
                    if self.bodovi !=0:
                        print("Dosta")
                        time.sleep(2)
                        self.nacrtajStol(None,self.p2OdabranaKarta)
                        return "dosta"
                
            self.p2OdabranaKarta.prvi=True
            self.nacrtajStol(None,self.p2OdabranaKarta)
            
            brojOdabraneKarte = self.unesiAkcijuDrugi(False)  
            if not self.mus:
                self.p1OdabranaKarta=self.p1.karte.pop(brojOdabraneKarte-1)
                self.nacrtajStol(self.p1OdabranaKarta,self.p2OdabranaKarta)
            else:
                while 1:
                    if self.p2OdabranaKarta.boja == self.p1.karte[brojOdabraneKarte-1].boja:
                        self.p1OdabranaKarta=self.p1.karte.pop(brojOdabraneKarte-1)
                        self.nacrtajStol(self.p1OdabranaKarta,self.p2OdabranaKarta)
                        break
                    else:
                        postiva=True
                        for karta in self.p1.karte:
                            if self.p2OdabranaKarta.boja==karta.boja:
                                postiva=False
                        if postiva:
                            if self.p1.karte[brojOdabraneKarte-1].adut:
                                self.p1OdabranaKarta=self.p1.karte.pop(brojOdabraneKarte-1)
                                self.nacrtajStol(self.p1OdabranaKarta,self.p2OdabranaKarta)
                                break
                            else:
                                postiva=True
                                for karta in self.p1.karte:
                                    if karta.adut:        
                                        postiva=False
                                        break
                                if postiva:
                                    self.p1OdabranaKarta=self.p1.karte.pop(brojOdabraneKarte-1)
                                    self.nacrtajStol(self.p1OdabranaKarta,self.p2OdabranaKarta)
                                    break
                                else:
                                    print("Morate poštivati boju!")
                                    brojOdabraneKarte = self.unesiAkcijuDrugi(False)  
                        else:
                            print("Morate poštivati boju!")
                            brojOdabraneKarte = self.unesiAkcijuDrugi(False)  
                            
        
    def postaviAdut(self):
        self.kartaAduta.adut=True;
        for karta in self.dek.karte:
            if karta.boja==self.kartaAduta.boja:
                karta.adut=True

    def vuciKarte(self):
        for i in range(5):
            self.p1.karte.append(self.dek.vuciKartu())
            self.p2.karte.append(self.dek.vuciKartu())

    def vuciJednuKartu(self):
        if len(self.dek.karte)>0:
            if len(self.dek.karte)==1:          
                if self.p1.naRedu:
                    self.p1.karte.append(self.dek.vuciKartu())
                    self.p2.karte.append(self.kartaAduta)
                    bojaPrijasnjegAduta=self.kartaAduta.boja
                    self.kartaAduta=karte.Karta(None, bojaPrijasnjegAduta)
                    self.mus=True
                else:
                    self.p2.karte.append(self.dek.vuciKartu())
                    self.p1.karte.append(self.kartaAduta)
                    bojaPrijasnjegAduta=self.kartaAduta.boja
                    self.kartaAduta=karte.Karta(None, bojaPrijasnjegAduta)
                    self.mus=True
            else:
                if self.p1.naRedu:
                    self.p1.karte.append(self.dek.vuciKartu())
                    self.p2.karte.append(self.dek.vuciKartu())
                else:
                    self.p2.karte.append(self.dek.vuciKartu())
                    self.p1.karte.append(self.dek.vuciKartu())

    def zamijeniAdutKartu(self, decko):
        karta=self.kartaAduta
        self.kartaAduta=decko
        return karta

    def unesiAkcijuPrvi(self,prviIgrac):
        while 1:               
            akcija = input("Odaberi kartu "+(self.p1.ime if prviIgrac else self.p2.ime)+": ")
            if akcija == "D":
                self.bodovi=self.provjeriDosta(True)
                if self.bodovi !=0:
                    print("Dosta")
                    time.sleep(2)
                    return "D"
                else:
                    print("Nema dovoljno bodova za izlaz!")
            elif akcija=="Z":
                print("Zatvorena igra")
                time.sleep(2)
                self.mus=True                 
            elif akcija in ("1","2","3","4","5") and int(akcija)<=(len(self.p1.karte) if prviIgrac else len(self.p2.karte)) and int(akcija)>0:
                break
        brojOdabraneKarte = int(akcija)
        if prviIgrac:
            self.p1OdabranaKarta=self.p1.karte.pop(brojOdabraneKarte-1)
        else:
            self.p2OdabranaKarta=self.p2.karte.pop(brojOdabraneKarte-1)

    def unesiAkcijuDrugi(self,prviIgrac):
        while 1:               
                akcija = input("Odaberi kartu "+(self.p2.ime if prviIgrac else self.p1.ime)+": ")
                if akcija in ("1","2","3","4","5")  and int(akcija)<=(len(self.p1.karte) if not prviIgrac else len(self.p2.karte)) and int(akcija)>0:                 
                    break
        return int(akcija)        
    

    def izracunajRezultatKarti(self,k1,k2): 
        if(k1>k2):
            self.p1.rezultatRunde+=k1.vrijednostIzracuna
            self.p1.rezultatRunde+=k2.vrijednostIzracuna
            self.p1.naRedu=True
            self.p2.naRedu=False
        else:
            self.p2.rezultatRunde+=k1.vrijednostIzracuna
            self.p2.rezultatRunde+=k2.vrijednostIzracuna
            self.p1.naRedu=False
            self.p2.naRedu=True
                
    def provijeriZvanje(self,odabranaKarta,prviIgrac):
        bonusBodovi=0
        odgovor=""
        if prviIgrac:
            if odabranaKarta.vrijednost==11:
                postojiKralj=False
                for karta in self.p1.karte:
                    if karta.vrijednost==12 and karta.boja==odabranaKarta.boja:
                        postojiKralj=True
                if postojiKralj:
                    if odabranaKarta.boja == self.kartaAduta.boja:
                        odgovor = input("Želite li zvati 40 i dosta?(Y/N): ")
                        bonusBodovi+=40                      
                    else:
                        odgovor = input("Želite li zvati 20 i dosta?(Y/N): ")
                        bonusBodovi+=20
                    self.p1.rezultatRunde+=bonusBodovi
                    if odgovor=="Y":
                        return "dosta"             
            if odabranaKarta.vrijednost==12:
                postojiBaba=False
                for karta in self.p1.karte:
                    if karta.vrijednost==11 and karta.boja==odabranaKarta.boja:
                        postojiBaba=True
                if postojiBaba:
                    if odabranaKarta.boja == self.kartaAduta.boja:
                        odgovor = input("Želite li zvati 40 i dosta?(Y/N): ")
                        bonusBodovi+=40                      
                    else:
                        odgovor = input("Želite li zvati 20 i dosta?(Y/N): ")
                        bonusBodovi+=20
                    self.p1.rezultatRunde+=bonusBodovi
                    if odgovor=="Y":
                        return "dosta"
                    
                
        else:
            if odabranaKarta.vrijednost==11:
                postojiKralj=False
                for karta in self.p2.karte:
                    if karta.vrijednost==11 and karta.boja==odabranaKarta.boja:
                        postojiKralj=True
                if postojiKralj:
                    if odabranaKarta.boja == self.kartaAduta.boja:
                        odgovor = input("Želite li zvati 40 i dosta?(Y/N): ")
                        bonusBodovi+=40                      
                    else:
                        odgovor = input("Želite li zvati 20 i dosta?(Y/N): ")
                        bonusBodovi+=20
                    self.p2.rezultatRunde+=bonusBodovi
                    if odgovor=="Y":
                        return "dosta"                 
            if odabranaKarta.vrijednost==12:
                postojiBaba=False
                for karta in self.p2.karte:
                    if karta.vrijednost==11 and karta.boja==odabranaKarta.boja:
                        postojiBaba=True
                if postojiBaba:
                    if odabranaKarta.boja == self.kartaAduta.boja:
                        odgovor = input("Želite li zvati 40 i dosta?(Y/N): ")
                        bonusBodovi+=40                      
                    else:
                        odgovor = input("Želite li zvati 20 i dosta?(Y/N): ")
                        bonusBodovi+=20
                    self.p2.rezultatRunde+=bonusBodovi
                    if odgovor=="Y":
                        return "dosta"

    def provjeriDosta(self,prviIgrac):
        if prviIgrac:
            if self.p1.rezultatRunde >=66:
                if self.p2.rezultatRunde==0:
                    return 3
                elif self.p2.rezultatRunde<33:
                    return 2
                elif self.p2.rezultatRunde>32:
                    return 1
            else:
                return 0
        else:
            if self.p2.rezultatRunde >=66:
                if self.p1.rezultatRunde==0:
                    return 3
                elif self.p1.rezultatRunde<33:
                    return 2
                elif self.p1.rezultatRunde>32:
                    return 1
            else:
                return 0

    def provjeriRezultatKraja(self,prviIgrac):
        if prviIgrac:
                if self.p2.rezultatRunde==0:
                    return 3
                elif self.p2.rezultatRunde<33:
                    return 2
                elif self.p2.rezultatRunde>32:
                    return 1
        else:
                if self.p1.rezultatRunde==0:
                    return 3
                elif self.p1.rezultatRunde<33:
                    return 2
                elif self.p1.rezultatRunde>32:
                    return 1

    def resetirajRundu(self):
        self.p1.karte.clear()
        self.p1.rezultatRunde=0
        self.p2.karte.clear()
        self.p2.rezultatRunde=0
        self.dek=dek.Dek()
        self.kartaAduta=self.dek.vuciKartu()
        self.mus=False
        self.postaviAdut()
        self.vuciKarte()
        self.odrediPrvogIgraca()
        
        
        
        
    def nacrtajStol(self,kartaIgraca1,kartaIgraca2):
        self.cls()
        print()
        print("{:>37}:{:<37}{:>10}".format(self.p2.ime,self.p2.rezultatRunde,self.p2.bodovi),end=" ")
        print()
        print("-"*85)
        for karta in self.p2.karte:
            print("{:^15}".format(repr(karta)),end=" ")
        brojac=1
        print()
        for karta in self.p2.karte:         
            print("{:^15}".format("["+str(brojac)+"]"),end=" ")
            brojac+=1
        print()
        print()
        print()
        print()
        print("Dek  :{:<10}{:>20}".format(len(self.dek.karte),repr(kartaIgraca2)))
        print("Adut :{:10}{:>20}".format(repr(self.kartaAduta),repr(kartaIgraca1)))
        print()
        print()
        print()
        print()
        for karta in self.p1.karte:
            print("{:^15}".format(repr(karta)),end=" ")
        brojac=1
        print()
        for karta in self.p1.karte:                
            print("{:^15}".format("["+str(brojac)+"]"),end=" ")
            brojac+=1
        print()
        print("-"*85)
        print("{:>37}:{:<37}{:>10}".format(self.p1.ime,self.p1.rezultatRunde,self.p1.bodovi),end=" ")
        print()

        
#snaps = Snaps()
#snaps.igraj()


