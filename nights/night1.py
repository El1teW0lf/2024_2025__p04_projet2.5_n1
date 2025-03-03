from ai.cpe import CPE
from ai.directeur import directeur
from ursina import * 
from menus.computer_screen_1 import ComputerScreen1
from menus.computer_screen_2 import ComputerScreen2
from menus.hour_screen import HourScreen
from modules.code_editor import CodeEditor
from modules.code_executor import CodeExecutor
from modules.door import Door
import time
import asyncio
import threading
from menus.death import DeathMenu
from modules.eventbus import EventBus


def send_message(event_name, message):
    print(f"Sent {event_name} message {message} to all subscribers")
    EventBus.send(event_name, message)

class Night1():

    def __init__(self,player, save, sound):

        self.night_started = False
        self.save = save
        self.sound = sound
        self.fps = int(1/time.dt)
        self.won = False

        self.previously_pressed = False
        self.player = player
        self.hour = 0
        self.time = 0 #based on tick count: 0 to 300, 12h to 6 am, 50 per hour for first night, add 1 every 60 tick count
        self.door = Door(self.sound.play_door)
        self.alive = True

        self.current_scene = 0 #0: Office, 1: Aisle right, 2: Aisle Left
        self.current_scene_type = False #false = cylinder, true = plane
        self.in_computer = False
        self.computer_collide = False
        self.last_move = []

        self.office_cylinder = Entity(model='office_cylinder', position=(0,1,0), scale=5, rotation=(0,90,0), texture='textures/cylinder/Desk/desk_light.png')
        self.office_cylinder.model.setTwoSided(True)

        self.office_plane = Entity(model="plane", position=(0,1,4), scale=5, rotation=(0,90,0), texture='textures/plane/Door/door_empty.png')
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
        self.code_editor = CodeEditor(self.code_entity,self.computer_2_gui.update_code,self.sound.play_key)

        self.run_button_plane = Entity(model="quad",position=(0,0.4,3),scale = (0.28,0.1), rotation = (0,0,0),collider="box", texture = "textures/computer/code_run.png")
        self.run_button_plane.disable()

        self.code_executor = CodeExecutor(self.computer_1_gui,self.door,self.sound.play_door)

        self.positions = {
            "pichon": 0,
            "surveillant": 0,
            "directeur":0,
            "CPE":0,
        }

        self.agresivite = {
            "pichon": 1,
            "surveillant": 0,
            "directeur":10,
            "CPE": 1,
        }

        self.parameters = {
            "hour_duration": 45, #based in time ticks (1 / sec ~~)
            "random_pc": False,
        }

        self.cpe = CPE(self.agresivite["CPE"],self)
        self.directeur = directeur(self.agresivite["directeur"],self)

        self.save_data = self.save.load()

        if self.save_data != None:
            self.code_editor.input = self.save_data["code"]
            print("Found save data, loaded.")
        else:
            print("No Save Data found.")

        print(window.monitors)

    def time_tick(self):

        self.positions["CPE"] = self.cpe.on_time_tick(self.time)
        self.positions["directeur"] = self.directeur.on_time_tick(self.time)
        self.door.update()
        self.door.force_change_status(self.time % 2 == 0)
        self.code_executor.run_update(self.last_move)
        self.last_move = []

        if self.time % self.parameters["hour_duration"] == 0:
            self.hour += 1
            self.hour_gui.update_hour(self.hour)

        if self.time >= self.parameters["hour_duration"]*7:
            self.won = True
            self.alive = False
            self.win()

        if self.code_executor.crashed:
            self.alive = False
            self.sync_pichon_kill()

        if self.current_scene == 1:
            self.office_plane.texture=self.get_current_door_path()

    def count_tick(self,tick):
        if tick % self.fps == 0:
            self.time += 1
            if self.night_started and self.alive:
                self.time_tick()

        if mouse.left and self.alive:
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

        self.save.code = self.code_editor.input
        self.hour_gui.update_hour(self.hour)

        self.code_executor.code = self.code_editor.get_code()
        self.code_executor.setup()
        if self.code_executor.crashed:
            self.alive = False
            self.sync_pichon_kill()


    def trigger_detector(self,position):
        self.last_move.append(position)
        print(f"Something moved and triggered the detector in room {position}")

    def kill(self,who):
        if who == "cpe":
            self.alive = False
            self.sync_cpe_kill()

        if who == "directeur":
            self.alive = False
            self.sync_directeur_kill()

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
                    self.office_plane.texture=self.get_current_door_path()

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

    def sync_pichon_kill(self):
        def run_async():
            asyncio.run(self.pichon_kill())

        thread = threading.Thread(target=run_async)
        thread.start()

    def sync_cpe_kill(self):
        def run_async():
            asyncio.run(self.cpe_kill())

        thread = threading.Thread(target=run_async)
        thread.start()

    def sync_directeur_kill(self):
        def run_async():
            asyncio.run(self.directeur_kill())

        thread = threading.Thread(target=run_async)
        thread.start()
        
    async def pichon_kill(self):

        print("Pichon Kill")

        self.office()
        if self.in_computer : 
            self.computer_toggle()

        self.set_button_status(False,False,False,False)

        for _ in range(4):
            self.computer_screen_2_plane.texture = "textures/computer/code_error.png"
            time.sleep(1)
            self.computer_screen_2_plane.texture = "textures/computer/code_blank.png"
            time.sleep(1)

        self.office_plane.texture = "textures/black.jpg"
        self.switch_plane()
        self.set_button_status(False,False,False,False)
        video = Texture("screamers/plane/screamer_pichon/screamer_pichon.mp4")
        video.repeat = False
        self.office_plane.texture = video
        self.sound.play_jumpscare()
        time.sleep(1.25)
        
        message = "\n".join(map(str, self.code_executor.output[-2:]))
        send_message("death", message)
        
        self.office_plane.texture = "textures/black.jpg"
        
        
        

    def close(self):
        self.save.save()
        quit()

    def get_current_door_path(self):
        close_npc = []
        for i in self.positions:
            if self.positions[i] == 7:
                close_npc.append(i)

        door_status = "off" if self.door.broken else ("closed" if self.door.status else "open")

        if len(close_npc) > 0:
            return f"textures/plane/Doors/door_{close_npc[0]}_{door_status}.png"
        return f"textures/plane/Doors/door_{door_status}.png"

    def win(self):
        if self.in_computer : 
            self.computer_toggle()
        self.office_plane.texture = "textures/black.jpg"
        self.switch_plane()
        self.set_button_status(False,False,False,False)

    async def cpe_kill(self):

        print("CPE Kill")

        self.check_door()
        if self.in_computer : 
            self.computer_toggle()

        self.set_button_status(False,False,False,False)

        self.office_plane.texture = "textures/plane/Doors/door_CPE_closed.png"
        time.sleep(2)
        self.sound.play_door()
        self.office_plane.texture = "textures/plane/Doors/door_CPE_open.png"
        time.sleep(1)
        if self.igg != None:
            self.igg.blink_opacity = 1
        
        self.office_plane.texture = "textures/black.jpg"
        self.switch_plane()
        self.set_button_status(False,False,False,False)
        video = Texture("screamers/plane/screamer_CPE/screamer_CPE.mp4")
        video.repeat = False
        self.office_plane.texture = video
        self.sound.play_jumpscare()
        time.sleep(1.25)
        self.office_plane.texture = "textures/black.jpg"

    async def directeur_kill(self):

        print("Directeur Kill")

        self.check_door()
        if self.in_computer : 
            self.computer_toggle()

        self.set_button_status(False,False,False,False)

        self.office_plane.texture = "textures/plane/Doors/door_directeur_closed.png"
        time.sleep(2)
        self.sound.play_door()
        self.office_plane.texture = "textures/plane/Doors/door_directeur_open.png"
        time.sleep(1)
        if self.igg != None:
            self.igg.blink_opacity = 1
        
        self.office_plane.texture = "textures/black.jpg"
        self.switch_plane()
        self.set_button_status(False,False,False,False)
        video = Texture("screamers/plane/screamer_directeur/screamer_directeur.mp4")
        self.sound.play_jumpscare()
        video.repeat = False
        self.office_plane.texture = video
        time.sleep(1.25)
        self.office_plane.texture = "textures/black.jpg"