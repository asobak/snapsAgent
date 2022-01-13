from spade.agent import Agent
from spade import quit_spade
from spade.behaviour import OneShotBehaviour, State
from snapsAgent import Snaps
import snaps
import karte
import dek
import igrac
import os
import asyncio
import time
	
class AgentOdabira(Agent):	
		
	async def on_end(self):
		print("ZAVRSAVAM AGENTA ODABIRA")
		
		        
class Ponasanje(OneShotBehaviour):
                async def run(self):
                        print("POKREČEM AGENTA DOABIRA")
                        print("Želite li igrati protiv lošeg bota[1] ili boljeg bota[2]?")
                        odabir=""
                        while odabir not in ("1","2") :
                                odabir=input()
                        snaps=Snaps("agent@rec.foi.hr", "tajna",odabir)
                        await snaps.start()
                        while snaps.is_alive():
                                await asyncio.sleep(1)
                        await self.agent.stop()
			

        
if __name__ == '__main__':
    a = AgentOdabira("agent@rec.foi.hr", "tajna")
    behav=Ponasanje()
    a.add_behaviour(behav)
    future=a.start()
    future.result()
    while a.is_alive():
          try:	
             time.sleep(1)
          except KeyboardInterrupt:
             a.stop()
             break
    quit_spade()
    time.sleep(2)
    


