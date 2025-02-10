from ursina import *

class IGGUI () :
    def __init__(self,debug = False):
        self.debug = debug

        self.debug_info = [
            "FPS: calculating...",
            "Delta time: 0.0",
            "Extra debug info: (example data)"
        ]

        self.debug_label = Text(
            text="\n".join(self.debug_info),
            origin=(-1, 1),
            position=window.top_left,
            scale=1,
            background=True  # optional: adds a background for better readability
        )

    def update(self):
        self.debug_label.text = "\n".join(self.debug_info)
        self.debug_label.position = window.top_left
