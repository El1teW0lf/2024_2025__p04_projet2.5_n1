from ursina import *

class DeathMenu(Entity):
    def __init__(self, quit_callback, death_message):
        super().__init__(parent=camera.ui)
        self.quit_callback = quit_callback

        # Background
        self.bg = Entity(
            parent=self,
            model="quad",
            texture="menus/assets/death/bg.png",
            scale=(window.aspect_ratio, 1),
            z=0
        )

        # Title
        self.title = Sprite(
            parent=self,
            texture="menus/assets/death/title.png",
            position=(0, 0.3),
            scale=(0.5, 0.1),
            z=-1
        )

        # Determine text scale based on length
        text_length = len(death_message)
        base_scale = 1.0  # Default scale
        scale_factor = max(0.3, min(1.0, 20 / text_length))  # Adjust dynamically

        # Death message label
        self.death_message_label = Text(
            parent=self,
            text=death_message,
            position=(0, 0),
            scale=scale_factor,
            z=-1,
            origin=(0, 0),
            color=color.white
        )


        self.menu_items = [self.bg, self.title, self.death_message_label]

    def show(self):
        for item in self.menu_items:
            item.enable()

    def is_enabled(self):
        return self.bg.enabled