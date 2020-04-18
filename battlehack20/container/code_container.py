import os
import builtins

def deepcopy(item):
    if isinstance(item, dict):
        return {key: deepcopy(val) for key, val in item.items()}
    elif isinstance(item, list):
        return [deepcopy(val) for val in item]
    elif isinstance(item, tuple):
        return tuple(deepcopy(val) for val in item)
    else:
        return item

class CodeContainer:
    def __init__(self, code):
        self.code = code

    def do_turn(self, methods):
        globals = {}
        locals = {}
        for key, method in methods.items():
            globals[key] = method
        exec(self.code, globals, locals)
        globals.update(locals)
        if 'turn' in locals and isinstance(locals['turn'], type(lambda: 1)):
            exec(locals['turn'].__code__, globals, locals)
        else:
            raise Exception("File does not have a 'turn' method.")
                
    @classmethod
    def from_directory(cls, dirname):
        file = os.path.join(dirname, "bot.py")
        with open(file) as f:
            code = f.read()
        return cls(code)
