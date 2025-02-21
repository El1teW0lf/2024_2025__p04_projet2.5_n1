from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from modules.CustomFPC import CustomFirstPersonController
from menus.main_menu import MainMenu  # Import menu class
from menus.splash_screen import SplashMenu
from menus.ingame_gui import IGGUI
from nights.night1 import Night1

app = Ursina(development_mode=True,show_ursina_splash=False,icon="textures/icon.ico",title="Five Night At Pichon (BETA)")

tick_events = []
all_ticks_events = []

def setup_map():
    print("Map Setup")
    load_model("models/plane")
    load_model("models/office_cylinder")
    player = CustomFirstPersonController(model='cube', z=-10, origin_y=-.5, speed=8, collider='box', enabled=True)
    player.fade_out(0, 0)
    player.set_position(Vec3(0, 0, 0))
    player.speed = 0
    player.gravity = 0

    editor_camera = EditorCamera(enabled=False, ignore_paused=True)

    def pause_input(key):
        if key == 'escape':   
            editor_camera.enabled = not editor_camera.enabled

            player.visible_self = editor_camera.enabled
            editor_camera.position = player.position
            player.rotation_y = 0
            player.center_pointer()

            application.paused = editor_camera.enabled

    pause_handler = Entity(ignore_paused=True, input=pause_input)
    print("Map Done")
    print("Launching Night 1")

    night = Night1(player)

    add_all_ticks_event("night_tick",night.count_tick,())
    print("Launched Night 1")

    ingame_gui = IGGUI(True,night)

    def update_debug_text(current):
        ingame_gui.debug_info = [
            f"Time Tick: {night.time}",
            f"Current Tick: {current}",
            f"Cpe's Position: {night.positions['CPE']}"
        ]
        ingame_gui.update()

    add_all_ticks_event("debug_info_tick",update_debug_text,())

def quit():
    application.quit()

def setup_main_menu():
    splash = SplashMenu()
    add_tick_event(200,splash.hide,())
    menu = MainMenu(setup_map,quit)
    menu.hide()
    add_tick_event(300,menu.show,())
    add_all_ticks_event("main_menu_logo_animation",menu.tick,())
    

def start():
    Sky(texture="textures/black.jpg")
    setup_main_menu()

def check_tick_events(current):
    for i in tick_events:
        if i["count"] == current:
            i["callback"](*i["args"])
            del i

def run_tick_events(current):
    for i in all_ticks_events:
        i["callback"](current, *i["args"])
        del i

def add_tick_event(tick_count, callback, args):
    tick_events.append({"count" : tick_count,"callback": callback, "args": args})

def add_all_ticks_event(name,callback, args):
    all_ticks_events.append({"callback": callback,"name": name, "args": args})

def run(count):
    check_tick_events(count)
    run_tick_events(count)
    app.step()
    

if __name__ == "__main__":
    start()
    count = 0
    while True:
        count += 1 
        run(count)