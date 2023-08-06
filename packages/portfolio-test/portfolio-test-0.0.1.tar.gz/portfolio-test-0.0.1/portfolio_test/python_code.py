class airport1:
   def __init__(self,takeoff,landing):
        self.takeoff = takeoff
        self.landing = landing
        
    def change_takeoff(self,new_airport):
        self.takeoff = new_airport
    
    def change_landing(self,new_airport):
        self.landing = new_airport

    