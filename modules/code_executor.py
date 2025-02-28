from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

import time

class SafePrint:
    def __init__(self,*args, **kwargs):
        self._call_print(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self._call_print(*args, **kwargs)
    
    def _call_print(self, *args, **kwargs):
        print(*args, **kwargs)

class CodeExecutor():
    def __init__(self):
        self.code = None


    def run(self):
        if self.code == None:
            raise ValueError("No code provided, no code executed.")
    
        compiled_code = compile_restricted(self.code, filename='<inline>', mode='exec')
        
        restricted_globals = {
            '__builtins__': safe_builtins,
            '_getattr_': getattr,
            '_setattr_': setattr,
            '_print_': SafePrint,
            '_getitem_': lambda obj, index: obj[index],
        }
        restricted_locals = {}
        
        exec(compiled_code, restricted_globals, restricted_locals)
        
        start_func = restricted_locals.get('start', restricted_globals.get('start'))
        update_func = restricted_locals.get('update', restricted_globals.get('update'))
        
        if start_func is None or update_func is None:
            raise ValueError("Both 'start' and 'update' functions must be defined in the code.")
        
        start_func()

        try:
            while True:
                update_func()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Execution interrupted by user.")