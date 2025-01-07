from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

office_texture = load_model("office_texture.glb",application.asset_folder.parent)
office_collider =  load_model('office_collider.obj',application.asset_folder.parent)

office = Entity(model="office_texture",scale=1)
office.set_position(Vec3(0,0,0))

office_hitbox = Entity(model="office_collider",scale=1,collider="mesh")
office_hitbox.set_position(Vec3(0,0,0))
office_hitbox.world_rotation_setter(Vec3(0,180,0))
office_hitbox.fade_out(duration=0)

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, origin_y=-.5, speed=8, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,1,1))


def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)


Sky()

app.run()

