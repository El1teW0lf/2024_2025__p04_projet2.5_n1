from ai.cpe import CPE

class Night1():
    def __init__(self):
        self.time = 0 #based on tick count: 0 to 300, 12h to 6 am, 50 per hour for first night, add 1 every 60 tick count
        self.door_status = False #false = open, true = closed

        self.positions = {
            "Pichon": 0,
            "Surveillant": 0,
            "CPE":0,
        }

        self.agresivite = {
            "Pichon": 1,
            "Surveillant": 0,
            "CPE": 1,
        }

        self.parameters = {
            "hour_duration": 50, #based in time ticks (1 / sec ~~)
            "random_pc": False,
            "python_errors": 5, #alowed number of python errors
            "python_duration": 10,  #alowed time to solver in time ticks
        }

        self.cpe = CPE(self.agresivite["CPE"],self)

    def time_tick(self):
        self.positions["CPE"] = self.cpe.on_time_tick(self.time)

    def count_tick(self,tick):
        if tick % 60 == 0:
            self.time += 1
            self.time_tick()

    def trigger_detector(self,position):
        print(f"Something moved and triggered the detector in room {position}")

    def kill(self,who):
        print(f"Player got killed by {who}")