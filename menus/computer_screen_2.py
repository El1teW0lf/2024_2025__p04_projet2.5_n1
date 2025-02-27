from ursina import *

class ComputerScreen2:
    def __init__(self, plane):
        self.parent = plane
        self.close = False
        
        self.parent.texture = "textures/computer/code_edit.png"


    def update(self):
        if self.close:
            self.parent.texture = "textures/computer/code_blank.png"
        else:
            self.parent.texture = "textures/computer/code_edit.png"