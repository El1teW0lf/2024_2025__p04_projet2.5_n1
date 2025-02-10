from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from modules.CustomFPC import CustomFirstPersonController
from menus.main_menu import MainMenu  # Import menu class

app = Ursina(development_mode=True,show_ursina_splash=True,icon="textures/icon.ico",title="Five Night At Pichon (BETA)")



def setup_map():
    player = CustomFirstPersonController(model='cube', z=-10, origin_y=-.5, speed=8, collider='box', enabled=True)
    player.fade_out(0, 0)
    player.set_position(Vec3(0, 0, 0))
    player.speed = 0
    player.gravity = 0

    editor_camera = EditorCamera(enabled=False, ignore_paused=True)

    load_model("models/untitled")
    office = Entity(model='untitled', position=(0,1,0), scale=5, rotation=(0,90,0), texture='textures/office.png')
    office.model.setTwoSided(True)

    
    def pause_input(key):
        if key == 'escape':   
            editor_camera.enabled = not editor_camera.enabled

            player.visible_self = editor_camera.enabled
            editor_camera.position = player.position
            player.rotation_y = 0
            player.center_pointer()

            application.paused = editor_camera.enabled

    pause_handler = Entity(ignore_paused=True, input=pause_input)

def quit():
    application.quit()

def setup_main_menu():
    menu = MainMenu(setup_map,quit)

setup_main_menu()


Sky(texture="textures/black.jpg")

app.run()


