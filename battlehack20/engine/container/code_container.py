import os
import re

class CodeContainer:
    def __init__(self, code):
        self.code = code
        self.code = compile(code, "<string>", "exec")
                
    @classmethod
    def from_directory(cls, dirname):
        file = os.path.join(dirname, "bot.py")
        with open(file) as f:
            code = f.read()
        code = cls.preprocess(code)
        return cls(code)

    @classmethod
    def preprocess(cls, content):
        """
        Strips battlehack20.stubs imports from the code.
        It removes lines containing one of the following imports:
        - from battlehack20.stubs import *
        - from battlehack20.stubs import a, b, c
        The regular expression that is used also supports non-standard whitespace styles like the following:
        - from battlehack20.stubs import a,b,c
        - from  battlehack20.stubs  import  a,  b,  c
        Go to https://regex101.com/r/bhAqFE/6 to test the regular expression with custom input.
        """

        pattern = r'^([ \t]*)from([ \t]+)battlehack20\.stubs([ \t]+)import([ \t]+)(\*|([a-zA-Z_]+([ \t]*),([ \t]*))*[a-zA-Z_]+)([ \t]*)$'

        # Replace all stub imports
        while True:
            match = re.search(pattern, content, re.MULTILINE)

            if match is None:
                break

            # Remove the match from the content
            start = match.start()
            end = match.end()
            content = content[0:start] + content[end:]

        return content

    @classmethod
    def preprocess(cls, content):
        """
        Strips battlehack20.stubs imports from the code.
        It removes lines containing one of the following imports:
        - from battlehack20.stubs import *
        - from battlehack20.stubs import a, b, c
        The regular expression that is used also supports non-standard whitespace styles like the following:
        - from battlehack20.stubs import a,b,c
        - from  battlehack20.stubs  import  a,  b,  c
        Go to https://regex101.com/r/bhAqFE/6 to test the regular expression with custom input.
        """
        # Code copied directly from battlehack20 engine

        pattern = r'^([ \t]*)from([ \t]+)battlehack20\.stubs([ \t]+)import([ \t]+)(\*|([a-zA-Z_]+([ \t]*),([ \t]*))*[a-zA-Z_]+)([ \t]*)$'

        # Replace all stub imports
        while True:
            match = re.search(pattern, content, re.MULTILINE)

            if match is None:
                break

            # Remove the match from the content
            start = match.start()
            end = match.end()
            content = content[0:start] + content[end:]

        return content
