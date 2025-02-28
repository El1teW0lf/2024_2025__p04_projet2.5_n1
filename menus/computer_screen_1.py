from ursina import *

class ComputerScreen1:
    def __init__(self, plane):
        self.parent = plane
        self.close = False
        self.started = False

        self.log = Text(y=0.38,x=-0.4,z=-0.001,scale = 2)
        self.log.parent = self.parent
        self.log.text = """
DEBUG1
DEBUG2
DEBUG3
DEBUG4
DEBUG5
DEBUG6
DEBUG7"""

        self.parent.texture = "textures/computer/bad_terminal.png"
        self.log.disable()

    def update(self):
        if self.close:
            self.log.enable()
        else:
            self.log.disable()