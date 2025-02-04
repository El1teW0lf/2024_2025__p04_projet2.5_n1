from ursina import *


class SettingsMenu(Entity):
    def __init__(self):
        super().__init__()
        self.title = Text("Hello", color=color.white, scale=1.5, origin=(0, 0))

        self.elements = [self.title]
    
    def show(self):
        for item in self.elements:
            item.enable()


def go_to_settings(previous_menu):
    previous_menu.hide()
    settings_menu = SettingsMenu()
    settings_menu.show()