from modules.parser import parse, format

class CodeEditor():

    def __init__(self,parent,update_screen,key_sfx):

        self.parent = parent
        self.refresh = update_screen
        self.close = False
        self.sfx = key_sfx

        self.can_code = True

        self.input = ["def start():",
                      "",
                      "",
                      "def update():",
                      "",
                      "",]
        self.cursor = [0,0]
        self.active = True
        self.is_shift_pressed = False

        self.parent.input = self.on_key

    def insert_char(self,original: str, char: str, position: int) -> str:
        return original[:position] + char + original[position:]

    def remove_char(self, original: str, position: int) -> str:
        return original[:position] + original[position+1:]
    
    def split_string(self,s: str, index: int):
        return [s[:index], s[index:]] if 0 <= index <= len(s) else ["",""]

    def on_key(self,key):

        if not self.close:
            return
        
        if not self.can_code:
            parsed = parse(self.input,[0,0])
            self.refresh(format(parsed))
            return

        big_keys=["tab","space"]
        big_chars=[""," "]

        shift_keys = ["&","é",'"',"'","(","§","è","!","ç","à",")","-",";"]
        shift_chars = ["1","2","3","4","5","6","7","8","9","0","°","_","."]

        if len(key) == 1:

            to_add = ""

            if key.isdigit():
                return
            
            if key in shift_keys:
                if self.is_shift_pressed :
                    to_add = shift_chars[shift_keys.index(key)]
                else:
                    to_add = key
            else:
                if self.is_shift_pressed :
                    to_add = key.upper()
                else:
                    to_add = key

            self.input[self.cursor[0]] = self.insert_char(self.input[self.cursor[0]],to_add,self.cursor[1])
            self.cursor[1] += 1
            self.sfx()

        elif key in big_keys:
            to_add = big_chars[big_keys.index(key)]

            self.input[self.cursor[0]] = self.insert_char(self.input[self.cursor[0]],to_add,self.cursor[1])
            self.cursor[1] += 1
            self.sfx()

        elif key == "enter":

            divided = self.split_string(self.input[self.cursor[0]],self.cursor[1])

            self.input[self.cursor[0]] = divided[0]

            self.cursor[0] += 1
            self.cursor[1] = 0
            self.input.insert(self.cursor[0],divided[1])
            self.sfx()
        elif key == "backspace":
            if len(self.input[self.cursor[0]]) > 0 and self.cursor[1] > 0:
                self.cursor[1] -= 1
                self.input[self.cursor[0]] = self.remove_char(self.input[self.cursor[0]],self.cursor[1])

            else:
                if len(self.input) > 1 and self.cursor[0]>0:
                    saved = self.input[self.cursor[0]]
                    self.input.pop(self.cursor[0])
                    self.cursor[0] -= 1
                    self.cursor[1] = len(self.input[self.cursor[0]])
                    self.input[self.cursor[0]] += saved
            self.sfx()
        elif key == "shift" or key == "left shift":
            self.is_shift_pressed = True

        elif key == "shift up" or key == "left shift up":
            self.is_shift_pressed = False

        elif key == "up arrow":
            if self.cursor[0] > 0:
                self.cursor[0] -= 1
                if self.cursor[1] > len(self.input[self.cursor[0]+1]):
                    self.cursor[1] = len(self.input[self.cursor[0]])
            self.sfx()
        elif key == "down arrow":
            if self.cursor[0] < len(self.input)-1:
                self.cursor[0] += 1
                if self.cursor[1] > len(self.input[self.cursor[0]]):
                    self.cursor[1] = len(self.input[self.cursor[0]])
            self.sfx()           
        elif key == "right arrow":
            if self.cursor[1] < len(self.input[self.cursor[0]]):
                self.cursor[1] += 1
            self.sfx()
        elif key == "left arrow":
            if self.cursor[1] > 0:
                self.cursor[1] -= 1
            self.sfx()

        added_cursor = self.input.copy()
        added_cursor[self.cursor[0]] = self.insert_char(self.input[self.cursor[0]],"|",max(self.cursor[1],0))

        parsed = parse(added_cursor,[max(0,self.cursor[0]-27),max(0,self.cursor[1]-53)])
        self.refresh(format(parsed))

    def get_code(self):
        result = ""

        for i in self.input:
            result += i + "\n"

        result = result.replace("","\t")
        result = result.replace("","\n")

        return result