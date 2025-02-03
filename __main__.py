from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from modules.CustomFPC import CustomFirstPersonController


app = Ursina(development_mode=False)


editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = CustomFirstPersonController(model='cube', z=-10, origin_y=0, speed=8, collider='box')
player.set_position(Vec3(0,0,0))
player.speed = 0
player.gravity = 0

e = Entity(model='cube', color=color.orange, position=(0,1,5), scale=5, rotation=(0,0,0), texture='fnaf_office.jpg')

def pause_input(key):
    if key == 'escape':    

        editor_camera.enabled = not editor_camera.enabled
        player.visible_self = editor_camera.enabled
        editor_camera.position = player.position
        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)

test = Text("not_found")

def display_camera_position():
    test.text = str(editor_camera.position)  
    print(editor_camera.position) 

position_display_updater = Entity(ignore_paused=True, update=display_camera_position)


Sky()

app.run()

