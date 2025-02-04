from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from modules.CustomFPC import CustomFirstPersonController


app = Ursina(development_mode=False,title="Five Night at Pichon (BETA)")


editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = CustomFirstPersonController(model='cube', z=-10, origin_y=0, speed=8, collider='box')
player.set_position(Vec3(0,0,0))
player.speed = 0
player.gravity = 0

load_model("models/untitled")
e = Entity(model='untitled', position=(0,1,0), scale=5, rotation=(0,90,0), texture='textures/output.jpg')
e.model.setTwoSided(True)

def pause_input(key):
    if key == 'escape':    

        player.visible_self = editor_camera.enabled
        editor_camera.position = player.position
        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)



app.run()

