from ursina import *


class SettingsMenu(Entity):
    def __init__(self, previous_menu, state):
        super().__init__()
        self.previous_menu = previous_menu
        self.state = state
        self.bg = Entity(
            model="quad",
            origin=(0, 0),  # Center the background
            texture="green_bg.png",
            scale=(window.aspect_ratio * 8.25, 8.25),  # Correct scaling
            z=0  # Keep it in the background
        )

        self.title = Sprite(
            parent = camera.ui,
            texture = "settings.png",
            color = color.white, 
            scale = (0.514, 0.1), 
            origin = (0, 0), 
            z=-1,
            position = (0, 0.3)
        )
        
        self.audio_btn = Entity(
            model = "quad",
            parent = camera.ui,
            texture = "audio_btn.png",
            scale = (0.358, 0.1),
            origin = (0, 0),
            color = color.white,
            collider = "box",
            position = (-0.08, 0.0125),
            z=-1
        )

        self.back_btn = Entity(
            model = "quad",
            parent = camera.ui,
            texture = "back_btn.png",
            scale = (0.341, 0.1),
            origin = (0, 0),
            color = color.white,
            collider = "box",
            position = (-0.086, -0.1125),
            z=-1
        )

        self.elements = [self.title, self.bg, self.back_btn, self.audio_btn]

    def get_textures(self):
        if self.state == "green":
            for element in self.elements:
                element.texture = f"assets/settings/green/{element.texture}"
        elif self.state == "dark":
            for element in self.elements:
                element.texture = f"assets/settings/dark/{element.texture}"
        
    
    def back(self):
        self.hide()
        self.previous_menu.show()

    def show(self):
        for item in self.elements:
            item.enable()

    def hide(self):
        for item in self.elements:
            item.disable()
            
    def on_hover_green(self, button, scale):
        button.scale = scale[1] * 1.05, scale[0] * 1.05

    def on_hover_dark(self, button, position):
        pass

    def on_hover(self):
        buttons = {
            self.back_btn : {
                "position" : (-0.107, -0.1),
                "scale" : (0.341, 0.1),
                "function" : self.back()
            },
            self.audio_btn : {
                "position" : (-0.1, -0.1),
                "scale" : (0.358, 0.1)
            }
        }
        for button, info in buttons.items():
            if button.hovered:
                if self.state == "green":
                    self.on_hover_green(button, info["scale"])
                    
                elif self.state == "dark":
                    self.on_hover_dark(button, info["position"])

                if mouse.left:
                    info["function"]
            else:
                button.scale = info["scale"]
                button.position = info["position"]



    def update(self):
        default_scales = {
            self.back_btn: (0.341, 0.1),
            self.audio_btn : (0.358, 0.1)
        }
        for button, default_scale in default_scales.items():
            if button.hovered:
                button.scale = (default_scale[0] * 1.05, default_scale[1] * 1.05)
                if mouse.left:
                    if button == self.back_btn:
                        self.back()
            else:
                button.scale = default_scale


def go_to_settings(previous_menu, state):
    previous_menu.hide()
    settings_menu = SettingsMenu(previous_menu, state)
    settings_menu.show()