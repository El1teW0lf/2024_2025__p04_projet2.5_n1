import multiprocess as mp  
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from ctypes import c_bool

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

class CodeExecutor():
    def __init__(self,log_gui):
        self.code = None
        self.output = []
        self.timeout = 0.05
        self.log_gui = log_gui

        self.crashed = False

        self.manager = mp.Manager()  # use multiprocess Manager
        self.output_queue = self.manager.Queue()
        self.namespace_queue = self.manager.Queue()
        self.error_queue = self.manager.Value(c_bool, False)
        self.custom_print = CustomPrintFactory(self.output_queue)
        self.namespace =  {
            '__builtins__': safe_builtins,
            '_getattr_': getattr,
            '_setattr_': setattr,
            '_inplacevar_': _inplacevar_,
            '_print_':  self.custom_print,
            '_getitem_': lambda obj, index: obj[index],
        }


    def setup(self):
        self.setup_code()
        self.run_process_safe(self.namespace.get('start'))

    def setup_code(self):
        if self.code is None:
            self.output.append("Error: No code provided, no code executed.")
            self.crashed = True


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

    def run_func_process(self,func):
        try:
            func()
        except Exception as e:
            self.output_queue.put("Error: "+str(e))
            self.error_queue.value = True
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
        else:
            temp_list = []
            while not self.output_queue.empty():
                temp_list.append(self.output_queue.get())

            self.output.extend(temp_list)
            self.namespace = self.namespace_queue.get()

            if self.error_queue.value:
                self.crashed = True
        self.log_gui.update_log(self.output)

    def run_update(self):
        self.run_process_safe(self.namespace.get('update'))