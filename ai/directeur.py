import random

class directeur():
    def __init__(self,agressivite, main):
        self.main = main
        self.agressivite = agressivite
        self.delay = random.randint(int( 30/ self.agressivite),int( 60/ self.agressivite)) # time between moves, in time tick diveded by aggresivity level
        self.internal_tick = 0
        self.comming = False
        self.comming_countdown = 3


    def jumpscare(self):
        self.main.kill("directeur")

    def on_time_tick(self,time_tick):
        self.internal_tick += 1
        if self.comming:
            if self.comming_countdown > 0:
                self.comming_countdown -= 1
                return 7
            else:
                if self.main.door.status:
                    self.main.trigger_detector(8)
                    self.comming_countdown = 3
                    self.comming = False
                    self.delay = random.randint(int( 30/ self.agressivite),int( 60/ self.agressivite))+self.internal_tick
                    return 8
                else:
                    self.jumpscare()
                    return 7
        else:
            if self.internal_tick == self.delay:
                self.comming = True
                self.comming_countdown = 3
                self.main.trigger_detector(8)
                return 7
            return 8
