from ai.cpe import CPE
from ursina import * 
from menus.computer_screen_1 import ComputerScreen1
from menus.computer_screen_2 import ComputerScreen2
from menus.hour_screen import HourScreen
from modules.code_editor import CodeEditor
from modules.code_executor import CodeExecutor

class Night1():

    def __init__(self,player, shader):

        self.night_started = False

        self.previously_pressed = False
        self.player = player
        self.time = 0 #based on tick count: 0 to 300, 12h to 6 am, 50 per hour for first night, add 1 every 60 tick count
        self.door_status = False #false = open, true = closed

        self.current_scene = 0 #0: Office, 1: Aisle right, 2: Aisle Left
        self.current_scene_type = False #false = cylinder, true = plane
        self.in_computer = False
        self.computer_collide = False
        self.shader = shader

        self.office_cylinder = Entity(model='office_cylinder',shader=self.shader, position=(0,1,0), scale=5, rotation=(0,90,0), texture='textures/cylinder/Desk/desk_light.png')
        self.office_cylinder.model.setTwoSided(True)

        self.office_plane = Entity(model="plane", shader = self.shader, position=(0,1,4), scale=5, rotation=(0,90,0), texture='textures/plane/Door/door_empty.png')
        self.office_plane.model.setTwoSided(True)
        self.office_plane.disable()

        self.computer_screen_1_plane = Entity(model="quad",position=(-0.55,0.8,3),scale = (0.94,0.84), rotation = (0,-6,0),collider="box")
        self.computer_screen_2_plane = Entity(model="quad",position=(0.55,0.8,3),scale = (0.94,0.84), rotation = (0,4,0),collider="box")
        self.hour_plane = Entity(model="quad",position=(0,1.2,3),scale = (0.2,0.2), rotation = (0,0,0),collider="box")
        
        self.computer_screen_1_plane.model.setTwoSided(True)
        self.computer_screen_2_plane.model.setTwoSided(True)
        self.hour_plane.model.setTwoSided(True)

        self.computer_1_gui = ComputerScreen1(self.computer_screen_1_plane)
        self.computer_2_gui = ComputerScreen2(self.computer_screen_2_plane)
        self.hour_gui = HourScreen(self.hour_plane)

        self.code_entity = Entity()
        self.code_editor = CodeEditor(self.code_entity,self.computer_2_gui.update_code)

        self.run_button_plane = Entity(model="quad",position=(0,0.4,3),scale = (0.28,0.1), rotation = (0,0,0),collider="box", texture = "textures/computer/code_run.png")
        self.run_button_plane.disable()

        self.code_executor = CodeExecutor()

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
            if self.night_started:
                self.time_tick()

        if mouse.left:
            if not self.previously_pressed:
                self.previously_pressed = True
                self.is_colliding_with_computers()
                self.click()
        else: 
            self.previously_pressed = False

    def is_colliding_with_computers(self):
        collided = False
        for i in mouse.collisions:
            if i.entity == self.computer_screen_1_plane or i.entity == self.computer_screen_2_plane:
                collided = True

        if mouse.collision == None:
            collided = False 

        self.computer_collide = collided

    def is_colliding_with_run_button(self):
        collided = False
        for i in mouse.collisions:
            if i.entity == self.run_button_plane:
                collided = True

        if mouse.collision == None:
            collided = False 

        return collided

    def click(self):
        if self.computer_collide:
            self.computer_toggle()
            return

        if self.is_colliding_with_run_button():
            self.run_code()
            self.computer_toggle()
            return

    def run_code(self):
        self.night_started = True
        self.code_editor.can_code = False
        self.computer_1_gui.started = True
        self.computer_2_gui.started = True
        print("Night Started")

        self.code_executor.code = self.code_editor.get_code()
        self.code_executor.run()


    def trigger_detector(self,position):
        print(f"Something moved and triggered the detector in room {position}")

    def kill(self,who):
        print(f"Player got killed by {who}")

    def computer_toggle(self):
        self.in_computer = not self.in_computer

        if self.in_computer:
            self.player.position = (0,-0.2,2)
            self.player.rotation_y = 0
            self.player.can_rotate = False
            self.office_cylinder.texture = "textures/black.jpg"
            self.set_button_status(False,False,False,False)

            self.computer_1_gui.close = True
            self.computer_2_gui.close = True
            self.hour_gui.close = True
            self.code_editor.close = True

            self.computer_1_gui.update()
            self.computer_2_gui.update()
            self.hour_gui.update()
            
            self.computer_2_gui.code.enable()

            if not self.night_started:
                self.run_button_plane.enable()
        else:
            self.player.position = (0,0,0)
            self.player.can_rotate = True
            self.update_scene()

            self.computer_1_gui.close = False
            self.computer_2_gui.close = False
            self.hour_gui.close = False
            self.code_editor.close = False

            self.computer_1_gui.update()
            self.computer_2_gui.update()
            self.hour_gui.update()

            self.computer_2_gui.code.disable()
            self.run_button_plane.disable()

    def set_button_status(self,down,left,right,up):
        if self.igg != None:
            self.igg.down_button.enabled = down
            self.igg.left_button.enabled = left
            self.igg.right_button.enabled = right
            self.igg.up_button.enabled = up

    def update_scene(self):

        if self.igg != None:
            self.igg.blink_opacity = 1

        if self.current_scene_type:
            self.office_plane.enable()
            self.office_cylinder.disable()
            self.player.block_rotation()
            self.computer_screen_1_plane.disable()
            self.computer_screen_2_plane.disable()
        else:
            self.office_plane.disable()
            self.office_cylinder.enable()
            self.computer_screen_1_plane.enable()
            self.computer_screen_2_plane.enable()
            self.player.can_rotate = True


        match self.current_scene:
                case 0:
                    self.set_button_status(True,True,True,False)
                    self.office_cylinder.texture = 'textures/cylinder/Desk/desk_light.png'
                case 1:
                    self.set_button_status(False,False,False,True)
                    self.office_plane.texture='textures/plane/Door/door_empty.png'

                case 10:
                    self.set_button_status(True,True,True,False)
                    self.office_plane.texture = "textures/plane/Left_aisle/left.png"
                case 11:
                    self.set_button_status(True,False,False,False)
                    self.office_plane.texture = "textures/plane/Left_aisle/Left_Left_Side/left_left.png"
                case 12:
                    self.set_button_status(True,False,False,False)
                    self.office_plane.texture = "textures/plane/Left_aisle/Left_Right_Side/left_right.png"

                case 20:
                    self.set_button_status(True,True,True,False)
                    self.office_plane.texture = "textures/plane/Right_aisle/right.png"
                case 21:
                    self.set_button_status(True,False,False,False)
                    self.office_plane.texture = "textures/plane/Right_aisle/Right_Left_Side/right_left.png"
                case 22:
                    self.set_button_status(True,False,False,False)
                    self.office_plane.texture = "textures/plane/Right_aisle/Right_Right_Side/right_right.png"

                case _:
                    self.office_cylinder.texture = "textures/uv-grid.png"
                    self.office_plane.texture = "textures/uv-grid.png"
                    self.set_button_status(True,True,True,True)

    def switch_plane(self):
        self.current_scene_type = True
        self.update_scene()  

    def switch_cylinder(self):
        self.current_scene_type = False
        self.update_scene()          

    def check_door(self):
        self.current_scene = 1
        self.current_scene_type = True
        self.update_scene()

    def office(self):
        self.current_scene = 0
        self.current_scene_type = False
        self.update_scene()

    def down_press(self):
        if self.current_scene == 0 :
            self.check_door()
            return

        if self.current_scene == 10 or  self.current_scene == 20 :
            self.office()
            return
        
        if self.current_scene == 11 or self.current_scene == 12:
            self.current_scene = 10
            self.switch_plane()
            return
        
        if self.current_scene == 21 or self.current_scene == 22:
            self.current_scene = 20
            self.switch_plane()
            return

    def up_press(self):
        if self.current_scene == 1:
            self.office()
            return


    def left_press(self):
        if self.current_scene == 0:
            self.current_scene = 10
            self.switch_plane()
            return

        if self.current_scene == 10:
            self.current_scene = 11
            self.switch_plane()
            return

        if self.current_scene == 20:
            self.current_scene = 21
            self.switch_plane()
            return

    def right_press(self):
        if self.current_scene == 0:
            self.current_scene = 20
            self.switch_plane()
            return

        if self.current_scene == 10:
            self.current_scene = 12
            self.switch_plane()
            return

        if self.current_scene == 20:
            self.current_scene = 22
            self.switch_plane()
            return
