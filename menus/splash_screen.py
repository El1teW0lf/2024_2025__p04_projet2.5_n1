from ursina import *
import time

class SplashMenu(Entity):
    def __init__(self):
        super().__init__()
        self.title = Sprite(
            parent=camera.ui,
            texture="assets/splash_menu/logo.png",
            origin=(0, 0), 
            scale=(0.1, 0.1),
            z=-1,
            position=(0, 0),  
        )

        

        self.elements = [self.title]
    
    def show(self):
        for item in self.elements:
            item.enable()

    def hide(self):
        for item in self.elements:
            item.fade_out(0,1)


def go_to_settings(previous_menu):
    previous_menu.hide()
    settings_menu = SplashMenu()
    settings_menu.show()