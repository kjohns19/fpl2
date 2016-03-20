import fpl.tokenizer

class Program:
    def __init__(self):
        pass

    def run_file(self, filename):
        with open(filename, 'r') as f:
            code = f.read()
        return self.run_code(code)

    def run_code(self, code):
        tokenizer = fpl.tokenizer.Tokenizer()
        tokens = tokenizer.tokenize(code)
        for token in tokens:
            print(type(token).__name__ + ': ' + str(token))
