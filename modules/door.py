
class Door():
    def __init__(self,sfx = None):
        self.status = False
        self.broken = False
        self.sfx = sfx
        self.temp = 0
        self.max_temp = 10 #max temp avant que ca casse
    
    def update(self):
        if self.status:
            self.temp += 1
        else: 
            self.temp -= 0.25

        self.temp = max(self.temp, 0) #On evite que la temp parte trop dans le negatif

        if self.temp >= self.max_temp:
            self.status = False
            self.broken = True

    def force_change_status(self,status):
        self.status = status

    def safe_get_status(self):
        return self.status
    
    def attempt_status_change(self,status):
        if self.broken:
            self.status = False
            return False
        else:
            if status == True or status == False: #on verifie bien que l'input du user est un bool, sinon explosion
                self.status = status
                return True
            else:
                raise ValueError("status should be a bool.")