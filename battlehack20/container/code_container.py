import os

class CodeContainer:
    def __init__(self, code):
        self.code = code
        self.code = compile(code, "<string>", "exec")
                
    @classmethod
    def from_directory(cls, dirname):
        file = os.path.join(dirname, "bot.py")
        with open(file) as f:
            code = f.read()
        return cls(code)
