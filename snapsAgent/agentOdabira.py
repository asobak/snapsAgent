from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, State
from snapsAgent import Snaps
import snaps
import karte
import dek
import igrac
import os
import asyncio
import time
import bot
			
class AgentOdabira(Agent):	
		
	async def on_end(self):
		print("ZAVRSAVAM AGENTA ODABIRA")
		
		
	def __init__(self, jid, password,bot):
		super().__init__(jid, password)
		self.bot=bot	
        
class Ponasanje(OneShotBehaviour):
		async def run(self):
			print("POKRECEM AGENTA DOABIRA")
			snaps=Snaps("agent@rec.foi.hr", "tajna",self.agent.bot)
			print(snaps)
			fut = (await snaps.start())
			print(fut)
			await fut.result()
			while snaps.is_alive():
				time.sleep(1)
				await print("ziv")		
			await self.agent.stop()
			

        
if __name__ == '__main__':
    print("Želite li igrati protiv lošeg bota[1] ili boljeg bota[2]?")
    odabir=""
    while odabir not in ("1","2") :
    	odabir=input()
    a = AgentOdabira("agent@rec.foi.hr", "tajna",odabir)
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


