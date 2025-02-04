from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from menus.main_menu import MainMenu  # Import menu class

app = Ursina(development_mode=False)



# Setup Player (Initially Disabled)
player = FirstPersonController(model='cube', z=-10, origin_y=-.5, speed=8, collider='box', enabled=False)
player.fade_out(0, 0)
player.set_position(Vec3(10.76, 3.6, 9.55))
player.speed = 0
player.gravity = 0

# Editor Camera (Initially Disabled)
editor_camera = EditorCamera(enabled=False, ignore_paused=True)

# Skybox (Initially Disabled)
sky = Sky(enabled=False)

# Function to toggle the editor camera
def pause_input(key):
    if key == 'tab':    
        editor_camera.enabled = not editor_camera.enabled
        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position
        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)

# Debugging text for position display (Initially Disabled)
position_text = Text("Position: ", position=(-0.5, 0.4), scale=1.5, color=color.white, enabled=False)

def display_camera_position():
    position_text.text = f"Position: {editor_camera.position}"

position_display_updater = Entity(ignore_paused=True, update=display_camera_position, enabled=False)

# --- MENU SYSTEM ---
def start_game():
    print("Starting game...")
    main_menu.hide()

    # Enable game elements
    player.enabled = True  # Enable player movement
    sky.enabled = True  # Enable skybox
    position_text.enabled = True  # Show position text
    position_display_updater.enabled = True  # Enable position updates

    # Set correct physics values
    player.speed = 8
    player.gravity = 9.8
    window.color = color.black  # Change background color

def quit_game():
    print("Quitting game...")
    application.quit()

# --- INITIAL SETUP ---
# Create the Main Menu
main_menu = MainMenu(start_game, quit_game)

# Set menu background color
window.color = color.dark_gray

app.run()
