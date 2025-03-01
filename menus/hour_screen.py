from ursina import *

class HourScreen:
    def __init__(self, plane):
        self.parent = plane
        self.close = False
        self.display = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM"]

        self.parent.texture = "textures/black.jpg"

        self.hour = Text(
            "",
            color=color.hex("149414"),
            parent=self.parent,
            origin = (0,0),
            scale=15,
            z=-0.001) 
        
        self.hour.position = Vec2(self.hour.width,0.3)
        self.hour.font = "fonts/JBMONO.ttf"
        self.hour.position = (0+(self.hour.width/2),0 + (self.hour.height/2))

        self.parent.disable()

    def update_hour(self,new):
        self.hour.text = self.display[new]

    def update(self):
        if self.close:
            self.parent.enable()
        else:
            self.parent.disable()