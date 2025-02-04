from ursina import *

class MainMenu(Entity):
    def __init__(self, start_callback, quit_callback):
        super().__init__()

        self.start_callback = start_callback

        # Create a background entity with a quad model
        self.bg = Entity(
            model="quad",
            origin=(0, -0.2),  # Center the background
            texture="assets/main_menu/green_bg.png",
            scale=(window.aspect_ratio * 11.25, 11.25),  # Correct scaling
            z=0  # Keep it in the background
        )

        # Title Text
        self.title = Sprite(
            parent=camera.ui,
            texture="assets/main_menu/main_menu_title.png",
            origin=(0.5, -0.7),
            scale=(0.1, 0.1),
            z=-1
        )

        # Start Button
        self.start_button = Entity(
            model="quad",
            parent=camera.ui,  # Attach to UI for proper rendering
            texture="assets/main_menu/play_btn.png",
            scale=(0.337, 0.1),
            origin=(1, -0.3),
            color=color.white,  # Prevents darkening effect
            collider="box"  # Adding a collider for the button
        )

        # Quit Button (Using default Button widget here)
        self.quit_button = Entity(
            model="quad",
            parent=camera.ui,  # Attach to UI for proper rendering
            texture="assets/main_menu/quit_btn.png",
            scale=(0.337, 0.1),
            origin=(1, -0.1),
            color=color.white,  # Prevents darkening effect
            collider="box"  # Adding a collider for the button
        )

        self.start_button.texture.filtering = None
        # Store menu items in a list for easy hiding/showing
        self.menu_items = [self.bg, self.title, self.start_button, self.quit_button]

    def show(self):
        for item in self.menu_items:
            item.enable()

    def hide(self):
        for item in self.menu_items:
            item.disable()

    def launch(self):
        self.hide()
        self.start_callback()
        
    def update(self):
        # Check if the mouse is over the start button
        if mouse.hovered_entity == self.start_button:
            # Check if the left mouse button is pressed
            if mouse.left:
                self.launch()  # Trigger the start callback when clicked
