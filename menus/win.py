from ursina import *
from modules.eventbus import send_message

class WinMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.quit_callback = quit_callback

        # Background
        self.bg = Entity(
            parent=self,
            model="quad",
            texture="menus/assets/win/bg.png",
            scale=(window.aspect_ratio, 1),
            z=0
        )

        # Title
        self.title = Sprite(
            parent=self,
            texture="menus/assets/win/title.png",
            position=(0, 0.3),
            scale=(0.492, 0.1),
            z=-1
        )

        # Determine text scale based on length
        text_length = len(death_message)
        base_scale = 1.0  # Default scale
        scale_factor = max(0.3, min(1.0, 20 / text_length))  # Adjust dynamically

        # Congrats title
        self.congrats_title = Sprite(
            parent=self,
            texture="menus/assets/win/congrats_title.png",
            position=(0, 0),
            scale=(0.594, 0.1),
            z=-1
        )

        self.main_menu_btn = Entity(
            model="quad",
            parent=camera.ui,  # Attach to UI for proper rendering
            texture="assets/win/main_menu_btn.png",
            scale=(0.276, 0.1),
            origin=(0, 0),  # Align the left side of the button
            color=color.white,  # Prevents darkening effect
            collider="box",  # Adding a collider for the button
            position=(-0.55, -0.2),  # Place it below the settings button
        )
        
        self.quit_btn = Entity(
            model="quad",
            parent=camera.ui,  # Attach to UI for proper rendering
            texture="assets/win/quit_btn.png",
            scale=(0.252, 0.1),
            origin=(0, 0),  # Align the left side of the button
            color=color.white,  # Prevents darkening effect
            collider="box",  # Adding a collider for the button
            position=(0.55, -0.2),  # Place it below the settings button
        )

        self.menu_items = [self.bg, self.title, self.death_message_label, self.main_menu_btn, self.quit_btn]

    def show(self):
        for item in self.menu_items:
            item.enable()

    def hide(self):
        for item in self.menu_items:
            item.disable()

    def is_enabled(self):
        return self.bg.enabled

    def update(self):
        if (not hasattr(self, "main_menu_btn") or self.main_menu_btn is None) or (not hasattr(self, "quit_btn") or self.quit_btn is None):
            return  

        buttons = {
            self.main_menu_btn: {
                "scale": (0.341, 0.1),
                "function": lambda: send_message("main_menu", "activate")
            },
            self.quit_btn: {
                "scale": (0.269, 0.1),
                "function": application.quit
            }
        }

        for button, info in buttons.items():
            if button.hovered:
                button.scale = (info["scale"][0] * 1.05, info["scale"][1] * 1.05)

                if mouse.left:
                    if button == self.main_menu_btn:
                        invoke(info["function"], delay=0.1)
                    elif button == self.quit_btn:
                        invoke(info["function"], delay=0.1)
                    self.hide()
            else:
                button.scale = info["scale"]