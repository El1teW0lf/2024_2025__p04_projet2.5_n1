from ursina import *

class ComputerScreen1:
    def __init__(self, plane):
        self.parent = plane
        self.close = False
        self.started = False

        self.log = Text(y=0.36,x=-0.41,z=-0.001,scale = 1,color=color.hex("149414"),)
        self.log.parent = self.parent
        self.log.text = ""
        self.parent.texture = "textures/computer/bad_terminal.png"
        self.log.disable()

    def update_log(self,new_log):
        trimmed = new_log[-25:]
        result = "\n"
        for i in trimmed:
            new_i = (str(i)[:60] + '..') if len(str(i)) > 60 else str(i)
            result +=  new_i + "\n"

        self.log.text = result

    def update(self):
        if self.close:
            self.log.enable()
        else:
            self.log.disable()