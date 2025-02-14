from ursina import *

class IGGUI () :
    def __init__(self,debug = False,night = None):
        self.night = night
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
        
        if not self.debug:
            self.debug_label.disable()

        self.down_button = Entity(
            model="quad",
            parent=camera.ui,  
            texture="assets/in_game_gui/button_down.png",
            scale=(1, 0.1),
            origin=(0, 0),  
            color=color.white,  
            collider="box", 
            position=(0, -0.45),  
        )

    def update(self):
        self.debug_label.text = "\n".join(self.debug_info)
        self.debug_label.position = window.top_left

        mouse_pos = mouse.position
        button_pos = self.down_button.position


        distance = ((mouse_pos[0] - button_pos[0])**2 + (mouse_pos[1] - button_pos[1])**2) ** 0.5
        self.down_button.alpha_setter((1 - min(distance * 2, 1)) *  0.34) 

        if mouse.hovered_entity == self.down_button:
            if mouse.left:
                self.night.check_door()
