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

        self.right_button = Entity(
            model="quad",
            parent=camera.ui,  
            texture="assets/in_game_gui/button_down.png",
            scale=(1, 0.1),
            origin=(0, 0),  
            color=color.white,  
            collider="box", 
            position=(0.8, 0),  
            
        )

        self.left_button = Entity(
            model="quad",
            parent=camera.ui,  
            texture="assets/in_game_gui/button_down.png",
            scale=(1, 0.1),
            origin=(0, 0),  
            color=color.white,  
            collider="box", 
            position=(-0.8, 0),  
            
        )
        self.up_button = Entity(
            model="quad",
            parent=camera.ui,  
            texture="assets/in_game_gui/button_down.png",
            scale=(1, 0.1),
            origin=(0, 0),  
            color=color.white,  
            collider="box", 
            position=(0, 0.45),  
            
        )

        self.left_button.rotation_z_setter(90)
        self.right_button.rotation_z_setter(-90)
        self.up_button.rotation_z_setter(180)

    def set_opacity(self,button):

        mouse_pos = mouse.position
        button_pos = button.position
        distance = ((mouse_pos[0] - button_pos[0])**2 + (mouse_pos[1] - button_pos[1])**2) ** 0.5
        button.alpha_setter((1 - min(distance * 2, 1)) *  0.34) 

    def update(self):
        self.debug_label.text = "\n".join(self.debug_info)
        self.debug_label.position = window.top_left

        self.set_opacity(self.down_button)
        self.set_opacity(self.left_button)
        self.set_opacity(self.right_button)
        self.set_opacity(self.up_button)

        if mouse.hovered_entity == self.down_button:
            if mouse.left:
                self.night.down_press()

        if mouse.hovered_entity == self.left_button:
            if mouse.left:
                self.night.left_press()


        if mouse.hovered_entity == self.right_button:
            if mouse.left:
                self.night.right_press()


        if mouse.hovered_entity == self.up_button:
            if mouse.left:
                self.night.up_press()

