from ursina import *

class ComputerScreen2:
    def __init__(self, plane):
        self.parent = plane
        self.close = False
        self.started = False

        self.parent.texture = "textures/computer/code_edit.png"

        self.code = Text(y=0.33,x=-0.4,z=-0.001,scale = 2,color=color.red)
        self.code.parent = self.parent
        self.code.disable()


    def update_code(self,code):
        self.code.text = code

    def update(self):
        if self.close:
            self.code.enable()
            self.parent.texture = "textures/computer/code_blank.png"
        else:
            self.code.disable
            if self.started:
                self.parent.texture = "textures/computer/code_running.png"
            else:
                self.parent.texture = "textures/computer/code_edit.png"