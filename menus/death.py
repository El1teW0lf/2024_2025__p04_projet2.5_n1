from ursina import *
from __main__ import setup_map

class DeathMenu(Entity):
    def __init__(self, quit_callback, death_message):
        self.quit_callback = quit_callback

        self.title = Sprite(
            parent = camera.ui,
            texture = "menus/assets/death/title.png",
            origin = (0, 0),
            position = (0.3, 0.3),
            scale = (),
            z=-1,
        )

        self.death_message_label = Text(
            parent = camera.ui,
            text = death_message,
            position = (0, 0.3),
            scale=(),
            z=-1

        )
