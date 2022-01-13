from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
import snaps
import karte
import dek
import igrac
import os
import asyncio
import time
import random
from operator import attrgetter




def odigrajRandomKartu(snapsRunda):           
	if(snapsRunda.p2.naRedu):
		if unesiAkcijuPrvi(snapsRunda)=="D":
			return "dosta"
	    #provjera zamjene karte aduta
		if snapsRunda.p2OdabranaKarta.adut and snapsRunda.p2OdabranaKarta.vrijednost==10 and len(snapsRunda.dek.karte)>1 and not snapsRunda.mus:
			snapsRunda.p2.karte.append(snapsRunda.zamijeniAdutKartu(snapsRunda.p2OdabranaKarta))
			snapsRunda.nacrtajStol(None,None)
			if unesiAkcijuPrvi(snapsRunda)=="D":
				return "dosta"
	    #provjera zvanja
		if snapsRunda.p2OdabranaKarta.vrijednost==11 or snapsRunda.p2OdabranaKarta.vrijednost==12:
			odgovorZvanja=provijeriZvanje(snapsRunda,snapsRunda.p2OdabranaKarta)
			if odgovorZvanja=="dosta":
				snapsRunda.bodovi=snapsRunda.provjeriDosta(False)
				if snapsRunda.bodovi !=0:
					print("Dosta")
					time.sleep(2)
					snapsRunda.nacrtajStol(None,snapsRunda.p2OdabranaKarta)
					return "dosta"	
		snapsRunda.p2OdabranaKarta.prvi=True
		snapsRunda.nacrtajStol(None,snapsRunda.p2OdabranaKarta)
	else:  
		brojOdabraneKarte = unesiAkcijuDrugi(snapsRunda)       
		if not snapsRunda.mus:
			snapsRunda.p2OdabranaKarta=snapsRunda.p2.karte.pop(brojOdabraneKarte-1)
			snapsRunda.nacrtajStol(snapsRunda.p1OdabranaKarta,snapsRunda.p2OdabranaKarta)
		else:
			while 1:
				if snapsRunda.p1OdabranaKarta.boja == snapsRunda.p2.karte[brojOdabraneKarte-1].boja:
					snapsRunda.p2OdabranaKarta=snapsRunda.p2.karte.pop(brojOdabraneKarte-1)
					snapsRunda.nacrtajStol(snapsRunda.p1OdabranaKarta,snapsRunda.p2OdabranaKarta)
					break
				else:
					postiva=True
					for karta in snapsRunda.p2.karte:
						if snapsRunda.p1OdabranaKarta.boja==karta.boja:        
							postiva=False
					if postiva:
						if snapsRunda.p2.karte[brojOdabraneKarte-1].adut:
							snapsRunda.p2OdabranaKarta=snapsRunda.p2.karte.pop(brojOdabraneKarte-1)
							snapsRunda.nacrtajStol(snapsRunda.p1OdabranaKarta,snapsRunda.p2OdabranaKarta)
							break
						else:
							postiva=True
							for karta in snapsRunda.p2.karte:
								if karta.adut:        
									postiva=False
									break
							if postiva:
								snapsRunda.p2OdabranaKarta=snapsRunda.p2.karte.pop(brojOdabraneKarte-1)
								snapsRunda.nacrtajStol(snapsRunda.p1OdabranaKarta,snapsRunda.p2OdabranaKarta)
								break
							else:
								print("Morate poštivati boju!")
								brojOdabraneKarte = unesiAkcijuDrugi(snapsRunda)  
					else:
					    print("Morate poštivati boju!")
					    brojOdabraneKarte = unesiAkcijuDrugi(snapsRunda)  

def unesiAkcijuPrvi(snapsRunda):
        while 1:
            akcija=pronadjiZamjenu(snapsRunda)    
            if akcija == "0":
                akcija=pronadjiZvanje(snapsRunda)
                if akcija == "0":
                             akcija= odigrajNajboljuKartuPrvi(snapsRunda)
                             if akcija is None:
                                     akcija = str(random.randint(1, 5))  
            snapsRunda.bodovi = snapsRunda.provjeriDosta(False)           
            if snapsRunda.bodovi > 0:
                return "D"            
            elif akcija in ("1","2","3","4","5") and int(akcija)<=len(snapsRunda.p2.karte) and int(akcija)>0:
                break                
        brojOdabraneKarte = int(akcija)
        snapsRunda.p2OdabranaKarta=snapsRunda.p2.karte.pop(brojOdabraneKarte-1)

def unesiAkcijuDrugi(snapsRunda):
        while 1:
                akcija = odigrajNajboljuKartuDrugi(snapsRunda)
                if akcija is None:   
                        akcija = str(random.randint(1, 5))
                if akcija in ("1","2","3","4","5") and int(akcija)<=len(snapsRunda.p2.karte) and int(akcija)>0:                 
                        break
        return int(akcija)        

def provijeriZvanje(snapsRunda,odabranaKarta):
        bonusBodovi=0
        if odabranaKarta.vrijednost==11:
                postojiKralj=False
                for karta in snapsRunda.p2.karte:
                    if karta.vrijednost==12 and karta.boja==odabranaKarta.boja:
                        postojiKralj=True
                if postojiKralj:
                    if odabranaKarta.boja == snapsRunda.kartaAduta.boja:
                        if (snapsRunda.p2.rezultatRunde+40)>65:
                             print("Zovem 40 i dosta")
                             time.sleep(2)
                        else: 
                             print("Zovem 40")
                             time.sleep(2)
                        bonusBodovi+=40                      
                    else:
                        if (snapsRunda.p2.rezultatRunde+20)>65:
                             print("Zovem 20 i dosta")
                             time.sleep(2)
                        else:
                             print("Zovem 20")
                             time.sleep(2)
                        bonusBodovi+=20
                    snapsRunda.p2.rezultatRunde+=bonusBodovi
                    return "dosta"                 
        if odabranaKarta.vrijednost==12:
                postojiBaba=False
                for karta in snapsRunda.p2.karte:
                    if karta.vrijednost==11 and karta.boja==odabranaKarta.boja:
                        postojiBaba=True
                if postojiBaba:
                    if odabranaKarta.boja == snapsRunda.kartaAduta.boja:
                        if (snapsRunda.p2.rezultatRunde+40)>65:
                             print("Zovem 40 i dosta")
                             time.sleep(2)
                        else: 
                             print("Zovem 40")
                             time.sleep(2)
                        bonusBodovi+=40                      
                    else:
                        if (snapsRunda.p2.rezultatRunde+20)>65:
                             print("Zovem 20 i dosta")
                             time.sleep(2)
                        else:
                             print("Zovem 20")
                             time.sleep(2)
                        bonusBodovi+=20
                    snapsRunda.p2.rezultatRunde+=bonusBodovi
                    return "dosta"
    
def pronadjiZvanje(snapsRunda):
        babe=[]
        for karta in snapsRunda.p2.karte:
                if karta.vrijednost==11:
                        babe.append(karta)
        for kartaBabe in babe:
                for kartaIgraca in snapsRunda.p2.karte:
                        if kartaIgraca.boja == kartaBabe.boja and kartaIgraca.vrijednost == 12:
                                time.sleep(2)
                                return str(snapsRunda.p2.karte.index(kartaIgraca)+1)                

        return "0"

def pronadjiZamjenu(snapsRunda):
        for karta in snapsRunda.p2.karte:
                if karta.vrijednost==10 and karta.boja==snapsRunda.kartaAduta.boja and len(snapsRunda.dek.karte)>1 and not snapsRunda.mus:
                        return str(snapsRunda.p2.karte.index(karta)+1)
        return "0"

def odigrajNajboljuKartuPrvi(snapsRunda):
        if snapsRunda.mus:
                najaca = max(snapsRunda.p2.karte,key=attrgetter('vrijednost'),default=None)  
                return str(snapsRunda.p2.karte.index(najaca)+1)
        else:
                neaduti=dohvatiNeadute(snapsRunda)
                if neaduti is None:
                        najslabija = min(snapsRunda.p2.karte,key=attrgetter('vrijednost'),default=None)
                else:
                        najslabija = min(neaduti,key=attrgetter('vrijednost'),default=None)
                return str(snapsRunda.p2.karte.index(najslabija)+1)
                
        
        
def odigrajNajboljuKartuDrugi(snapsRunda):
        jaceKarte=[]
        baba=False
        kralj=False
        #Gleda ima li koja jaca karta iste boje
        for karta in snapsRunda.p2.karte:
                if karta.vrijednost>snapsRunda.p1OdabranaKarta.vrijednost and karta.boja==snapsRunda.p1OdabranaKarta.boja:
                        jaceKarte.append(karta)
        #Ako ima  kartu babe i kralja zajedno s asom ili cenarom baca asa ili cenara
        if any(x.vrijednost == 11 for x in jaceKarte) and any(x.vrijednost == 12 for x in jaceKarte) and (any(x.vrijednost == 13 for x in jaceKarte) or any(x.vrijednost == 14 for x in jaceKarte)):
                for karta in jaceKarte:
                        if karta.vrijednost == 13 or karta.vrijednost == 14:
                                return str(snapsRunda.p2.karte.index(karta)+1)
        #inace baci samo najjacu
        najmanjaNajaca = min(jaceKarte,key=attrgetter('vrijednost'),default=None)
       
        
        #Nema jacu koja nije adut onda idemo a je karta cenar il jaca i nije adut
        if najmanjaNajaca==None and not snapsRunda.mus:              
                if snapsRunda.p1OdabranaKarta.vrijednost>12 and not snapsRunda.kartaAduta.boja==snapsRunda.p1OdabranaKarta.boja:
                        for karta in snapsRunda.p2.karte:
                                #a imamo adut i a je on jaci od dececa
                                if karta.boja == snapsRunda.kartaAduta.boja and karta.vrijednost > 10:                              
                                        #a je taj adut baba il kralj
                                        if karta.vrijednost == 11:
                                                baba=True
                                        if karta.vrijednost == 12:
                                                kralj=True                                      
                                        jaceKarte.append(karta)
                        #ak ima adut onda gledaj a su solo baba i deda ili nisu
                        if len(jaceKarte)>0:
                                if baba and kralj and len(jaceKarte)>2:
                                        najmanjaNajaca = max(jaceKarte,key=attrgetter('vrijednost'),default=None)
                                elif baba and kralj:
                                        najmanjaNajaca = min(dohvatiNeadute(snapsRunda),key=attrgetter('vrijednost'),default=None)                                           
                                else:
                                        najmanjaNajaca = min(jaceKarte,key=attrgetter('vrijednost'),default=None)
                        else:
                                najmanjaNajaca = min(dohvatiNeadute(snapsRunda),key=attrgetter('vrijednost'),default=None)                               
        if najmanjaNajaca is None:
                return None
        else:
                return str(snapsRunda.p2.karte.index(najmanjaNajaca)+1)
        

def dohvatiNeadute(snapsRunda):
        neaduti=[]
        for karta in snapsRunda.p2.karte:
                if karta.boja != snapsRunda.kartaAduta.boja:
                        neaduti.append(karta)
        return neaduti
        
                        
