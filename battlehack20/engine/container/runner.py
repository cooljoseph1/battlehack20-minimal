class Runner:
    def __init__(self, code_container, methods):
        self.code = code_container.code
        self.globals = {}
        self.locals = {}
        for key, method in methods.items():
            self.globals[key] = method
        
        exec(self.code, self.globals, self.locals)
        self.globals.update(self.locals)

    def do_turn(self):
        if 'turn' in self.locals and isinstance(self.locals['turn'], type(lambda: 1)):
            exec(self.locals['turn'].__code__, self.globals, self.locals)
        else:
            raise Exception("File does not have a 'turn' method.")
