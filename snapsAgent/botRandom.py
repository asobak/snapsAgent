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



def odigrajRandomKartu(snapsRunda):   
	        
	if(snapsRunda.p2.naRedu):
		if unesiAkcijuPrvi(snapsRunda)=="D":
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
								brojOdabraneKarte = unesiAkcijuDrugi(snapsRunda)  
					else:
					    brojOdabraneKarte = unesiAkcijuDrugi(snapsRunda)  

def unesiAkcijuPrvi(snapsRunda):
        while 1:
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
                        else: 
                             print("Zovem 40")
                        bonusBodovi+=40                      
                    else:
                        if (snapsRunda.p2.rezultatRunde+20)>65:
                             print("Zovem 20 i dosta")
                        else:
                             print("Zovem 20")
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
                        else: 
                             print("Zovem 40")
                        bonusBodovi+=40                      
                    else:
                        if (snapsRunda.p2.rezultatRunde+20)>65:
                             print("Zovem 20 i dosta")
                        else:
                             print("Zovem 20")
                        bonusBodovi+=20
                    snapsRunda.p2.rezultatRunde+=bonusBodovi
                    return "dosta"
    
            
