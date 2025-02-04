from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from menus.main_menu import MainMenu  # Import menu class


app = Ursina(development_mode=False,title="Five Night at Pichon (BETA)")

# Setup Player (Initially Disabled)
player = FirstPersonController(model='cube', z=-10, origin_y=-.5, speed=8, collider='box', enabled=False)
player.fade_out(0, 0)
player.set_position(Vec3(10.76, 3.6, 9.55))
player.speed = 0
player.gravity = 0

load_model("models/untitled")
e = Entity(model='untitled', position=(0,1,0), scale=5, rotation=(0,90,0), texture='textures/output.jpg')
e.model.setTwoSided(True)


app.run()
