import time
import json
import base64
import os

class Save():
    def __init__(self):
        self.launch_timestamp = time.time()
        self.code = None
        self.night = 1

    def load(self):

        save_data = None

        if os.path.isfile("saves/last.pichon") :
            last_save = None
            with open(f"saves/last.pichon","r") as file:
                last_save = str(file.read())
            
            if os.path.isfile(f"saves/{last_save}"):
                with open(f"saves/{last_save}","r") as file:
                    save_data = json.loads(base64.a85decode(file.read()))

        return save_data

    def save(self):
        if self.code != None:
            self.save_timestamp = time.time()
            with open(f"saves/save_{self.save_timestamp}.pichon","wb") as file:
                data = {'code': self.code,'night': self.night, 'launch_timestamp': self.launch_timestamp, 'save_timestamp': self.save_timestamp}
                file.write(base64.a85encode(json.dumps(data).encode("utf-8")))

            with open(f"saves/last.pichon","wb") as file:
                file.write((f"save_{self.save_timestamp}.pichon").encode("utf-8"))