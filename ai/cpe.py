

class CPE():
    def __init__(self,agressivite, main):
        self.main = main
        self.agressivite = agressivite
        self.delay = int(15 / agressivite) # time between moves, in time tick diveded by aggresivity level
        self.path = [0,3,2,4,5,6,7]
        self.internal_tick = 0
        self.position_index = 0

    def jumpscare(self):
        self.main.kill("cpe")

    def move(self):
        self.main.trigger_detector(self.path[self.position_index])

    def on_time_tick(self,time_tick):
        self.internal_tick += 1
        if self.internal_tick >= self.delay:

            if self.path[self.position_index] == 7 and not self.main.door_status:
                self.jumpscare()

            self.internal_tick = 0
            if self.position_index >= len(self.path)-1:
                self.position_index = 0
            else:
                self.position_index += 1
            
            self.move()
        return self.path[self.position_index]
