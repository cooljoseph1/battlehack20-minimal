import os
import builtins

class CodeContainer:
    def __init__(self, directory):
        file = os.path.join(directory, "bot.py")
        with open(file) as f:
            self.code = f.read()
        
        self.globals["__builtins__"] = builtins.__dict__.copy()
        self.locals = {}
        
        exec(self.code, globals=self.globals, locals=self.locals)
        self.globals.update(self.locals)

    def do_turn(self, methods):
        globals = {key: val.copy() for key, val in self.globals.items()}
        locals = {key: val.copy() for key, val in self.locals.items()}
        for key, method in methods.items():
            globals["__builtins__"][key] = method
        if 'turn' in self.locals and isinstance(self.locals['turn'], type(lambda: 1)):
            exec(self.locals['turn'].__code__, globals, locals)
        else:
            raise Exception("File does not have a 'turn' method.")
                
