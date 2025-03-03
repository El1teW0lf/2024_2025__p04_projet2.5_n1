from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from modules.CustomFPC import CustomFirstPersonController
from menus.main_menu import MainMenu  # Import menu class
from menus.splash_screen import SplashMenu
from menus.ingame_gui import IGGUI
from nights.night1 import Night1
from shaders.psx_shader import psx_shader
from panda3d.core import loadPrcFileData
from modules.save import Save
from modules.sfx import Sound
import traceback

def get_max_window_size(aspect_ratio):
    screen_width, screen_height = window.fullscreen_size
    target_width = screen_width
    target_height = int(screen_width / aspect_ratio)

    if target_height > screen_height:
        target_height = screen_height
        target_width = int(screen_height * aspect_ratio)

    return target_width, target_height

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
            save.save()
            quit()

    pause_handler = Entity(ignore_paused=True, input=pause_input)
    print("Map Done")
    print("Launching Night 1")


    night = Night1(player,save,sound)

    add_all_ticks_event("night_tick",night.count_tick,())
    print("Launched Night 1")

    ingame_gui = IGGUI(True,night)
    night.igg = ingame_gui

    ingame_gui.blink_opacity = 1

    def update_debug_text(current):
        ingame_gui.debug_info = f"""
            time_tick: {night.time}
            current_tick: {current}
            position_cpe: {night.positions['CPE']}
            position_directeur: {night.positions['directeur']}
            current_scene: {night.current_scene}
            current_scene_type: {night.current_scene_type}
            current_rotation: {player.rotation_y}
            in_computer: {night.in_computer}
            door_status: {night.door.status}
            door_temps: {night.door.temp}
            door_broken: {night.door.broken}
        """
        ingame_gui.update()

    add_all_ticks_event("debug_info_tick",update_debug_text,())
    add_tick_event(count + 10,window.center_on_screen,())

def quit():
    application.quit()

def setup_main_menu():
    splash = SplashMenu()
    add_tick_event(10,window.center_on_screen,())
    add_tick_event(50,splash.hide,())
    menu = MainMenu(setup_map,quit)
    menu.hide()
    add_tick_event(150,menu.show,())
    add_all_ticks_event("main_menu_logo_animation",menu.tick,())
    

def setup():
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
    try:
        app = Ursina(development_mode=False,show_ursina_splash=False,icon="textures/icon.ico",title="Five Night At Pichon (BETA)")
        save = Save()
        sound = Sound()
        window.forced_aspect_ratio = 1.777
        window.borderless = True
        max_width, max_height = get_max_window_size(window.forced_aspect_ratio)
        window.fullscreen = True
        window.always_on_top = True


        loadPrcFileData("", "gl-version 3 2")

        count = 0
        tick_events = []
        all_ticks_events = []

        setup()
        while True:
            count += 1 
            run(count)
    except Exception as e:
        print("!!!CRITICAL ERROR!!!")
        print("GAME CRASHED")
        print("CRASH REPORT:")
        traceback.print_exc()
        save.save()
        quit()