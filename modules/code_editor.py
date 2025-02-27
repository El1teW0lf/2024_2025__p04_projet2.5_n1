

class CodeEditor():
    def __init__(self,parent):

        self.parent = parent
        self.input = [[]]
        self.cursor = (0,0)

        self.parent.input = self.on_key

    def on_key(self,key):
        big_keys=["enter","tab","space"]
        big_chars=["\n","\t"," "]
        print(key)
        if self.visible:
            if self.is_shift_pressed and len(key) == 1:
                self.content.append(key.upper())
            if len(key) == 1:
                self.content.append(key)
            elif key in big_keys:
                self.content.append(big_chars[big_keys.index(key)])
            elif key == "backspace":
                self.content.pop()
