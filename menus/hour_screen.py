from ursina import *

class HourScreen:
    def __init__(self, plane):
        self.parent = plane
        self.close = False

        self.parent.texture = "textures/black.jpg"

        self.hour = Text(
            "12 AM",
            color=color.hex("149414"),
            parent=self.parent,
            origin = (0,0),
            scale=15,
            z=-0.001) 
        
        self.hour.position = Vec2(self.hour.width,0.3)
        self.hour.font = "fonts/JBMONO.ttf"
        self.hour.position = (0+(self.hour.width/2),0 + (self.hour.height/2))

        self.parent.disable()


    def update(self):
        if self.close:
            self.parent.enable()
        else:
            self.parent.disable()