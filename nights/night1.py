from ai.cpe import CPE
from ursina import * 

class Night1():

    def __init__(self,player):

        self.player = player
        self.time = 0 #based on tick count: 0 to 300, 12h to 6 am, 50 per hour for first night, add 1 every 60 tick count
        self.door_status = False #false = open, true = closed

        self.current_scene = 0 #0: Office, 1: Aisle right, 2: Aisle Left
        self.current_scene_type = False #false = cylinder, true = plane

        self.office_cylinder = Entity(model='office_cylinder', position=(0,1,0), scale=5, rotation=(0,90,0), texture='textures/cylinder/Desk/desk_light.png')
        self.office_cylinder.model.setTwoSided(True)

        self.office_plane = Entity(model="plane", position=(0,1,4), scale=5, rotation=(0,90,0), texture='textures/plane/Door/door_empty.png')
        self.office_plane.model.setTwoSided(True)
        self.office_plane.disable()
        

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

    def update_scene(self):

        if self.current_scene_type:
            self.office_plane.enable()
            self.office_cylinder.disable()
            self.player.block_rotation()
        else:
            self.office_plane.disable()
            self.office_cylinder.enable()
            self.player.can_rotate = True


        if self.igg != None:
            match self.current_scene:
                case 0:
                    self.igg.down_button.enable
        

    def check_door(self):
        self.current_scene = 1
        self.current_scene_type = True
        self.update_scene()

    def office(self):
        self.current_scene = 0
        self.current_scene_type = False
        self.update_scene()

    def down_press(self):
        if self.current_scene == 0:
            self.check_door()

    def up_press(self):
        if self.current_scene == 1:
            self.office()


    def left_press(self):
        pass

    def right_press(self):
        pass