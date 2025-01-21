from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

nsi_room =  load_blender_scene('nsi_room_def1',application.asset_folder)

nsi_room.Plane_006.collider = 'box'
nsi_room.Plane_006.visible = True

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, origin_y=-.5, speed=8, collider='box')
player.fade_out(0,0)
player.set_position(Vec3(10.76,3.6,9.55))
player.speed = 0
player.gravity = 0

def pause_input(key):
    if key == 'tab':    

        editor_camera.enabled = not editor_camera.enabled
        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
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

