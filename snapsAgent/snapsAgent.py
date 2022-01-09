from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
import snaps
import karte
import dek
import igrac
import os
import asyncio
import time
import botRandom
import botBolji



class Ponasanje(FSMBehaviour):
	async def on_start(self):
		print("Pocinjem ponasanje agenta snaps")

	async def on_end(self):
		await self.agent.stop()
		print("Zavrsavam ponasanje agenta snaps")
		
		

class Igrac(State):
	async def run(self):
		if len(self.agent.snaps.p1.karte)==0 and len(self.agent.snaps.p2.karte)==0:
			self.set_next_state("Izracun")     
			return              
		if self.agent.snaps.odigrajKartuPrvi()=="dosta":
			self.set_next_state("Izracun") 
			return         
		await asyncio.sleep(2)
		if self.agent.snaps.p1.naRedu:
			self.set_next_state("Racunalo")
		else: 
			self.agent.snaps.izracunajRezultatKarti(self.agent.snaps.p1OdabranaKarta,self.agent.snaps.p2OdabranaKarta)
			await asyncio.sleep(2)
			if not self.agent.snaps.mus:
				self.agent.snaps.vuciJednuKartu()
			self.agent.snaps.nacrtajStol(None,None) 
			if self.agent.snaps.p1.naRedu:
				self.set_next_state("Igrac")
			else:
				self.set_next_state("Racunalo")
				


class Racunalo(State):
        async def run(self):
                if len(self.agent.snaps.p1.karte)==0 and len(self.agent.snaps.p2.karte)==0:
                        self.set_next_state("Izracun")
                        return
                #await asyncio.sleep(2)
                if self.agent.mod=="1":
                        if botRandom.odigrajRandomKartu(self.agent.snaps)=="dosta":
                                self.set_next_state("Izracun")
                                return
                else:
                        if botBolji.odigrajRandomKartu(self.agent.snaps)=="dosta":
                                self.set_next_state("Izracun")
                                return 
                if self.agent.snaps.p2.naRedu:
                        self.set_next_state("Igrac")
                else: 
                        self.agent.snaps.izracunajRezultatKarti(self.agent.snaps.p1OdabranaKarta,self.agent.snaps.p2OdabranaKarta)
                        await asyncio.sleep(2)
                        if not self.agent.snaps.mus:
                                self.agent.snaps.vuciJednuKartu()
                        self.agent.snaps.nacrtajStol(None,None) 
                        if self.agent.snaps.p2.naRedu:
                                self.set_next_state("Racunalo")
                        else:
                                self.set_next_state("Igrac")
				
class Izracun(State):
	async def run(self):	
		if self.agent.snaps.p1.naRedu:
			if len(self.agent.snaps.p1.karte)==0 and len(self.agent.snaps.p2.karte)==0:
				self.agent.snaps.bodovi=self.agent.snaps.provjeriRezultatKraja(True)
			self.agent.snaps.p1.bodovi-=self.agent.snaps.bodovi
			self.agent.snaps.p1.dobioZadnju=True
			self.agent.snaps.p2.dobioZadnju=False
			self.agent.snaps.resetirajRundu()
			self.agent.snaps.nacrtajStol(None,None)  
		else:
			if len(self.agent.snaps.p1.karte)==0 and len(self.agent.snaps.p2.karte)==0:
				self.agent.snaps.bodovi=self.agent.snaps.provjeriRezultatKraja(False)
			self.agent.snaps.p2.bodovi-=self.agent.snaps.bodovi
			self.agent.snaps.p2.dobioZadnju=True
			self.agent.snaps.p1.dobioZadnju=False
			self.agent.snaps.resetirajRundu()
			self.agent.snaps.nacrtajStol(None,None) 
		if self.agent.snaps.p1.bodovi<=0 or self.agent.snaps.p2.bodovi<=0:
			print("Prijatelj "+(self.agent.snaps.p1.ime if self.agent.snaps.p1.bodovi<=0 else self.agent.snaps.p2.ime)  +" je pobijedio!!!")
		else:
			if self.agent.snaps.p1.naRedu:
				self.set_next_state("Igrac")
			else:
				self.set_next_state("Racunalo")
			
	
		
        
			
class Snaps(Agent):
	async def setup(self):
		fsm = Ponasanje()
		fsm.add_state(name="Igrac", state=Igrac())
		fsm.add_state(name="Racunalo", state=Racunalo(),initial=True)
		fsm.add_state(name="Izracun", state=Izracun())
		fsm.add_transition(source="Igrac", dest="Racunalo")
		fsm.add_transition(source="Racunalo", dest="Igrac")
		fsm.add_transition(source="Igrac", dest="Igrac")
		fsm.add_transition(source="Racunalo", dest="Racunalo")
		fsm.add_transition(source="Igrac", dest="Izracun")
		fsm.add_transition(source="Izracun", dest="Igrac")
		fsm.add_transition(source="Racunalo", dest="Izracun")
		fsm.add_transition(source="Izracun", dest="Racunalo")
		self.add_behaviour(fsm)  
		
	def __init__(self, jid, password,mod):
		super().__init__(jid, password)
		self.mod=mod
		self.snaps=snaps.Snaps()
		self.snaps.resetirajRundu()
		self.snaps.nacrtajStol(None,None)	
        

        
if __name__ == '__main__':
    print("Želite li igrati protiv lošeg bota[1] ili boljeg bota[2]?")
    odabir=""
    while odabir not in ("1","2") :
    	odabir=input()  
    a = Snaps("agent@rec.foi.hr", "tajna",odabir)
    future=a.start()
    future.result()
    while a.is_alive():
    	try:	
    		time.sleep(1)
    	except KeyboardInterrupt:
    		a.stop()
    		break


