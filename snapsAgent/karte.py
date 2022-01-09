class Karta:
    prvi=False
    adut=False
    boje = ["\u2665",
             "\u2666",
             "\u2660",
             "\u2663"]
    
    vrijednosti = ["Dečko", "Baba",
              "Kralj","10", "As"]

    def __init__(self, v, s):
        """INTEGERI"""
        self.vrijednost = v
        self.boja = s
        if self.vrijednost==10:
            self.vrijednostIzracuna=2
        elif self.vrijednost==11:
            self.vrijednostIzracuna=3
        elif self.vrijednost==12:
            self.vrijednostIzracuna=4
        elif self.vrijednost==13:
            self.vrijednostIzracuna=10
        elif self.vrijednost==14:
            self.vrijednostIzracuna=11

    def __lt__(self, c2):
        if self.adut and c2.adut:
            if self.vrijednost < c2.vrijednost:
                return True
            else:
                return False
        elif self.adut and not c2.adut:
            return False
        elif not self.adut and c2.adut:
            return True
        elif self.prvi:
            if self.boja==c2.boja:
                if self.vrijednost<c2.vrijednost:       
                    return True
                else:
                    return False
            return False
        return True;


    def __gt__(self, c2):
        if self.adut and c2.adut:
            if self.vrijednost < c2.vrijednost:
                return False
            else:
                return True
        elif self.adut and not c2.adut:
            return True
        elif not self.adut and c2.adut:
            return False
        elif self.boja == c2.boja:
            if self.vrijednost < c2.vrijednost:
                return False
            else:
                return True
        else:
            if self.prvi:
                return True
            else:
                return False
            
            
        
  

    def __repr__(self):
        if self.vrijednost==None:
            v=self.boje[self.boja] 
        else:
            v=self.boje[self.boja] +" "+ self.vrijednosti[self.vrijednost-10]
        return v

