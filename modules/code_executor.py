import multiprocess as mp  
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from ursina import *
from ctypes import c_bool
from line_profiler import profile
import time
import threading
import asyncio

class CustomPrintFactory:
    def __init__(self, output):
        self.output = output

    def _call_print(self,*args):
        self.output.put(*args)

    def __call__(self,*args):
        return CustomPrintFactory(self.output)

def _inplacevar_(operator, old_value, new_value):
    if operator == '+=':
        return old_value + new_value
    elif operator == '-=':
        return old_value - new_value
    elif operator == '*=':
        return old_value * new_value
    elif operator == '/=':
        return old_value / new_value
    else:
        raise ValueError(f"Unsupported operator: {operator}")

_SAFE_MODULES = frozenset(("math",))

def _safe_import(name, *args, **kwargs):
    if name not in _SAFE_MODULES:
        raise Exception(f"Don't you even think about {name!r}")
    return __import__(name, *args, **kwargs)

class SafeDoor():
    def __init__(self,status,desired,broken):
        self._status = status
        self._desired = desired
        self._broken = broken

    @property
    def status(self):
        return self._status.value
    
    @status.setter
    def status(self,status):
        self._desired.value = status
        return self._broken

class SafeDetector():
    def __init__(self,last):
        self._last = last

    @property
    def last_moved(self):
        return self._last.value
    
class CodeExecutor():
    def __init__(self,log_gui,door,sfx):
        self.code = None
        self.output = []
        self.timeout = 3
        self.log_gui = log_gui
        self.door = door
        self.sfx = sfx

        self.crashed = False

        self.manager = mp.Manager()  
        self.output_queue = self.manager.Queue()
        self.namespace_queue = self.manager.Queue()
        self.error_queue = self.manager.Value(c_bool, False)
        self.door_status_queue = self.manager.Value(c_bool,False)
        self.door_broken_queue = self.manager.Value(c_bool,False)
        self.door_desired_queue = self.manager.Value(c_bool,False)
        self.last_move_queue = self.manager.Value(int,None)

        self.custom_print = CustomPrintFactory(self.output_queue)
        self.safe_door = SafeDoor(self.door_status_queue,self.door_desired_queue,self.door_broken_queue)
        self.safe_detector = SafeDetector(self.last_move_queue)

        self.namespace =  {
            '__builtins__': safe_builtins,
            '_getattr_': getattr,
            '_setattr_': setattr,
            '_inplacevar_': _inplacevar_,
            '_print_':  self.custom_print,
            '_getitem_': lambda obj, index: obj[index],
            'door': self.safe_door,
            "__import__": _safe_import,
            "detector": self.safe_detector,
            '_write_': lambda *args: args[0]
        }


    def setup(self):
        self.setup_code()
        self.run_process_safe(self.namespace.get('start'))

    def setup_code(self):
        if self.code is None:
            self.output.append("Error: No code provided, no code executed.")
            self.crashed = True
            print(self.output)


        try: 
            compiled_code = compile_restricted(self.code, filename='<inline>', mode='exec')
        except Exception as e:
            self.output.append("Error: Failed to compile code:")
            self.output.append(e)
            self.crashed = True
            return
        
        exec(compiled_code, self.namespace, self.namespace)

        start_func = self.namespace.get('start')
        update_func = self.namespace.get('update')

        if start_func is None or update_func is None:
            self.output.append("Error: Both 'start' and 'update' functions must be defined in the code.")
            self.crashed = True
            print(self.output)

    def run_func_process(self,func):
        try:
            func()
        except Exception as e:
            self.output_queue.put("Error: "+str(e))
            self.error_queue.value = True
            print(self.output)
        self.namespace_queue.put(self.namespace)

    def run_process_safe(self, func):
        process = mp.Process(target=self.run_func_process, args=(func,))
        process.start()
        process.join(self.timeout)
        if process.is_alive():
            print("Process is still alive, timeout occurred.")
            process.terminate()
            process.join()
            self.output.append("Error: Execution timed out!")
            self.crashed = True
            print(self.output)
        else:
            temp_list = []
            while not self.output_queue.empty():
                temp_list.append(self.output_queue.get())

            self.output.extend(temp_list)
            self.namespace = self.namespace_queue.get()

            if self.error_queue.value:
                self.crashed = True
                print(self.output)
        self.log_gui.update_log(self.output)

    async def run_update_async(self):

        start = time.time()

        self.door_status_queue.value = self.door.status
        self.door_broken_queue.value = self.door.broken
        
        self.run_process_safe(self.namespace.get('update'))

        if self.door_desired_queue.value != self.door.status:
            try:
                result = self.door.attempt_status_change(self.door_desired_queue.value)
                if result:
                    if self.door_desired_queue.value != self.door_status_queue.value:
                        self.sfx()
            except Exception as e:
                self.crashed =True
                self.output.append("Error: "+str(e))

        end = time.time()

    def run_update(self,last_move):
        self.last_move_queue.value = last_move
        def run_async():
            asyncio.run(self.run_update_async())

        thread = threading.Thread(target=run_async)
        thread.start()