from ursina import *

class IGGUI () :
    def __init__(self,debug = False,night = None):
        self.night = night
        self.debug = debug

        self.blink_opacity = 0

        self.debug_info = [
            "FPS: calculating...",
            "Delta time: 0.0",
            "Extra debug info: (example data)"
        ]

        self.startup_value = Text(y=.5,x=.3)

        self.blink = Entity(
            model="quad",
            parent=camera.ui,
            scale=(10,10),
            origin =(0,0),
            color = color.black,
            position = (0.5,0.5)
        )

        self.button_list = ButtonList(
            {
            'widow.position = Vec2(0,0)': Func(setattr, window, 'position', Vec2(0,0)),
            'widow.size = Vec2(768,768)': Func(setattr, window, 'size', Vec2(768,768)),
            'widow.center_on_screen()': window.center_on_screen,
            'window.forced_aspect_ration = 1.77': Func(setattr, window, "forced_aspect_ratio", 1.777),

            'widow.borderless = True': Func(setattr, window, 'borderless', True),
            'widow.borderless = False': Func(setattr, window, 'borderless', False),

            'widow.fullscreen = True': Func(setattr, window, 'fullscreen', True),
            'widow.fullscreen = False': Func(setattr, window, 'fullscreen', False),

            }, y=0.5, x = -.9
        )

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
            scale=(0.8, 0.1),
            origin=(0, 0),  
            color=color.white,  
            collider="box", 
            position=(0.8, 0),  
            
        )

        self.left_button = Entity(
            model="quad",
            parent=camera.ui,  
            texture="assets/in_game_gui/button_down.png",
            scale=(0.8, 0.1),
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

        self.up_button.enabled = False
        self.blink.enable = True
        self.blink.fade_out(self.blink_opacity,0)

        self.left_button.rotation_z_setter(90)
        self.right_button.rotation_z_setter(-90)
        self.up_button.rotation_z_setter(180)

        self.previously_pressed = False

        if self.debug == False:
            self.button_list.disable()
            self.startup_value.disable()

    def set_opacity(self,button):

        mouse_pos = mouse.position
        button_pos = button.position
        distance = ((mouse_pos[0] - button_pos[0])**2 + (mouse_pos[1] - button_pos[1])**2) ** 0.5
        button.alpha_setter(max((1 - min(distance * 2, 1)) *  0.34, 0.1)) 

    def update(self):
        self.blink.fade_out(self.blink_opacity,0)
        self.blink_opacity = max(self.blink_opacity - 0.01, 0)

        self.startup_value.text = \
f'''            position: {window.position}
            size: {window.size}
            aspect_ratio: {window.aspect_ratio}
            window.main_monitor.width: {window.main_monitor.width}
            window.main_monitor.height: {window.main_monitor.height}'''

        self.startup_value.text = self.startup_value.text + self.debug_info

        self.set_opacity(self.down_button)
        self.set_opacity(self.left_button)
        self.set_opacity(self.right_button)
        self.set_opacity(self.up_button)


        if mouse.left:
            if not self.previously_pressed:
                self.previously_pressed = True
                if mouse.hovered_entity == self.down_button:
                    self.night.down_press()
                if mouse.hovered_entity == self.right_button:
                    self.night.right_press()
                if mouse.hovered_entity == self.left_button:
                    self.night.left_press()
                if mouse.hovered_entity == self.up_button:
                    self.night.up_press()
        else:
            self.previously_pressed = False

