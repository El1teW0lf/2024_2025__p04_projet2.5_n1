from ursina import *
from menus.settings import go_to_settings

class MainMenu(Entity):
    def __init__(self, start_callback, quit_callback):
        super().__init__()

        self.start_callback = start_callback
        self.quit_callback = quit_callback
        # Create a background entity with a quad model
        self.bg = Entity(
            model="quad",
            origin=(0, 0),  # Center the background
            texture="assets/main_menu/green_bg.png",
            scale=(window.aspect_ratio * 8.25, 8.25),  # Correct scaling
            z=0  # Keep it in the background
        )

        # Title Text
        self.title = Sprite(
            parent=camera.ui,
            texture="assets/main_menu/main_menu_title.png",
            origin=(0, 0),  # Align the left side of the sprite
            scale=(0.1, 0.1),
            z=-1,
            position=(-0.4, 0.3),  # Place it at the top-left side of the screen
        )

        # Start Button
        self.start_button = Entity(
            model="quad",
            parent=camera.ui,  # Attach to UI for proper rendering
            texture="assets/main_menu/play_btn.png",
            scale=(0.337, 0.1),
            origin=(0, 0),  # Align the left side of the button
            color=color.white,  # Prevents darkening effect
            collider="box",  # Adding a collider for the button
            position=(-0.5, 0.05),  # Place it below the title
        )

        # Settings Button
        self.settings_button = Entity(
            model="quad",
            parent=camera.ui,  # Attach to UI for proper rendering
            texture="assets/main_menu/settings_btn.png",
            scale=(0.537, 0.1),
            origin=(0, 0),  # Align the left side of the button
            color=color.white,  # Prevents darkening effect
            collider="box",  # Adding a collider for the button
            position=(-0.425, -0.075),  # Place it below the start button
        )

        # Quit Button
        self.quit_button = Entity(
            model="quad",
            parent=camera.ui,  # Attach to UI for proper rendering
            texture="assets/main_menu/quit_btn.png",
            scale=(0.302, 0.1),
            origin=(0, 0),  # Align the left side of the button
            color=color.white,  # Prevents darkening effect
            collider="box",  # Adding a collider for the button
            position=(-0.515, -0.2),  # Place it below the settings button
        )

        self.pichon = Entity(
            model="quad",
            parent=camera.ui,
            texture="assets/main_menu/pichon.png",
            scale = (0.8, 1),
            origin=(0, 0),  # Align the left side of the sprite
            position = (0.5, -0.05),  # Place it at the top-left side of
        )

        # Store menu items in a list for easy hiding/showing
        self.menu_items = [self.bg, self.title, self.start_button, self.settings_button, self.quit_button, self.pichon]

    def show(self):
        for item in self.menu_items:
            item.enable()

    def hide(self):
        for item in self.menu_items:
            item.disable()

    def launch(self):
        self.hide()
        self.start_callback()
        
    def tick(self,tick_count):
        self.title.rotation_z_setter(sin(tick_count/30)*15)
        self.title.rotation_y_setter(sin(tick_count/100)*15)

    def update(self):
        # Define default scales
        default_scales = {
            self.start_button: (0.337, 0.1),
            self.settings_button: (0.5, 0.1),
            self.quit_button: (0.302, 0.1)
        }

        # Loop through all buttons
        for button, default_scale in default_scales.items():
            if mouse.hovered_entity == button:
                mouse.visible = True
                mouse.texture = "assets/on_hover_cursor.png"
                button.scale = (default_scale[0] * 1.05, default_scale[1] * 1.05)  # Slightly increase size
                if mouse.left:
                    if button == self.start_button:
                        self.launch()
                    elif button == self.settings_button:
                        go_to_settings(self, "dark")
                    elif button == self.quit_button:
                        self.quit_callback()
            else:
                button.scale = default_scale 
                mouse.texture = None # Reset scale when not hovered

