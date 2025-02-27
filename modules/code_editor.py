from modules.parser import parse, format

class CodeEditor():
    def __init__(self,parent,update_screen):

        self.parent = parent
        self.refresh = update_screen
        self.input = [""]
        self.cursor = [0,0]
        self.active = True
        self.is_shift_pressed = False

        self.parent.input = self.on_key

    def insert_char(self,original: str, char: str, position: int) -> str:
        return original[:position] + char + original[position:]

    def remove_char(self, original: str, position: int) -> str:
        return original[:position] + original[position+1:]

    def on_key(self,key):
        big_keys=["tab","space"]
        big_chars=[""," "]

        if len(key) == 1:

            to_add = ""

            if self.is_shift_pressed :
                to_add = key.upper()
            else:
                to_add = key

            self.cursor[1] += 1
            self.input[self.cursor[0]] = self.insert_char(self.input[self.cursor[0]],to_add,self.cursor[1])


        elif key in big_keys:
            to_add = big_chars[big_keys.index(key)]

            self.cursor[1] += 1
            self.input[self.cursor[0]] = self.insert_char(self.input[self.cursor[0]],to_add,self.cursor[1])

        elif key == "enter":
            self.cursor[0] += 1
            self.cursor[1] = 0
            self.input.insert(self.cursor[0],"")
        
        elif key == "backspace":
            if len(self.input[self.cursor[0]]) > 0:
                self.cursor[1] -= 1
                self.input[self.cursor[0]] = self.remove_char(self.input[self.cursor[0]],self.cursor[1])

            else:
                if len(self.input) > 1:
                    self.input.pop(self.cursor[0])
                    self.cursor[0] -= 1
                    self.cursor[1] = len(self.input[self.cursor[0]])


        parsed = parse(self.input)
        print(format(parsed))
        self.refresh(format(parsed))