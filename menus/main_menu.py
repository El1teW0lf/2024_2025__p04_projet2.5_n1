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
            origin=(0, -0.175),  # Center the background
            texture="assets/main_menu/green_bg.png",
            scale=(window.aspect_ratio * 11.25, 11.25),  # Correct scaling
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
            position=(-0.41, -0.075),  # Place it below the start button
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
            scale = (0.8, 10),
            origin=(0, 0),  # Align the left side of the sprite
            position = (0.5, -0.2),  # Place it at the top-left side of
        )
        self.start_button.texture.filtering = None
        # Store menu items in a list for easy hiding/showing
        self.menu_items = [self.bg, self.title, self.start_button, self.settings_button, self.quit_button, self.pichon]

    def show(self):
        for item in self.menu_items:
            item.enable()

    def hide(self):
        for item in self.menu_items:
            item.disable()

    def update(self):
        # Check if the mouse is over the start button
        if mouse.hovered_entity == self.start_button:
            # Check if the left mouse button is pressed
            if mouse.left:
                self.start_callback()  # Trigger the start callback when clicked
        elif mouse.hovered_entity == self.settings_button:
            if mouse.left:
                go_to_settings(self)
        elif mouse.hovered_entity == self.quit_button:
            if mouse.left:
                self.quit_callback()
