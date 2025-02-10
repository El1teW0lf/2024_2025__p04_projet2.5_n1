from ursina import *


class SettingsMenu(Entity):
    def __init__(self, previous_menu):
        super().__init__()
        self.previous_menu = previous_menu
        self.bg = Entity(
            model="quad",
            origin=(0, 0),  # Center the background
            texture="assets/main_menu/green_bg.png",
            scale=(window.aspect_ratio * 8.25, 8.25),  # Correct scaling
            z=0  # Keep it in the background
        )

        self.title = Sprite(
            parent = camera.ui,
            texture = "assets/settings/settings.png",
            color = color.white, 
            scale = (0.514, 0.1), 
            origin = (0, 0), 
            z=-1,
            position = (0, 0.3)
        )
        
        self.keybinds_button = Entity(
            model = "quad",
            parent = camera.ui,
            texture = "assets/settings/keybinds_btn.png",
            scale = (0.516, 0.1),
            origin = (0, 0),
            color = color.white,
            collider = "box",
            position = (0, -0.075),
            z=-1
        )

        self.back_btn = Entity(
            model = "quad",
            parent = camera.ui,
            texture = "assets/settings/back_btn.png",
            scale = (0.302, 0.1),
            origin = (0, 0),
            color = color.white,
            collider = "box",
            position = (0, -0.2),
            z=-1
        )

        self.elements = [self.title, self.bg, self.back_btn, self.keybinds_button]
    
    def back(self):
        self.hide()
        self.previous_menu.show()

    def show(self):
        for item in self.elements:
            item.enable()

    def hide(self):
        for item in self.elements:
            item.disable()

    def update(self):
        default_scales = {
            self.back_btn: (0.302, 0.1)
        }
        for button, default_scale in default_scales.items():
            if button.hovered:
                button.scale = (default_scale[0] * 1.05, default_scale[1] * 1.05)
                if mouse.left:
                    if button == self.back_btn:
                        self.back()
            else:
                button.scale = default_scale


def go_to_settings(previous_menu):
    previous_menu.hide()
    settings_menu = SettingsMenu(previous_menu)
    settings_menu.show()