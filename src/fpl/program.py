import fpl.tokenizer
import fpl.stack

class Program:
    def __init__(self):
        self.stack = fpl.stack.Stack()

    def run_file(self, filename):
        with open(filename, 'r') as f:
            code = f.read()
        return self.run_code(code)

    def run_code(self, code):
        tokenizer = fpl.tokenizer.Tokenizer()
        tokens = tokenizer.tokenize(code)
        for token in tokens:
            token.apply(self)
        print(self.stack)
