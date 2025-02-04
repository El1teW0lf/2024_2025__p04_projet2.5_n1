from ursina import *

class MainMenu(Entity):
    def __init__(self, start_callback, quit_callback):
        super().__init__()

        self.start_callback = start_callback

        # Create a background entity with a quad model
        self.bg = Entity(
            model="quad",
            origin=(0, -0.50),  # Center the background
            texture="assets/green_bg.png",
            scale=(window.aspect_ratio * 9.5, 9.5),  # Correct scaling
            z=0  # Keep it in the background
        )

        # Title Text
        self.title = Text("Learn Python with Pichon", scale=2, origin=(0, 0), y=0.4, color=color.white)

        # Buttons
        self.start_button = Button(text="Start", scale=(0.2, 0.1), position=(0, 0.1), color=color.green, on_click=self.launch)
        self.quit_button = Button(text="Quit", scale=(0.2, 0.1), position=(0, -0.1), color=color.red, on_click=quit_callback)

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