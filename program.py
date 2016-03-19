import tokenizer

class Program:
    def __init__(self):
        pass

    def run_file(self, filename):
        with open(filename, 'r') as f:
            code = f.read()
        return run_code(code)

    def run_code(self, code):
        tokens = tokenizer.tokenize(code)
        for token in tokens:
            print(token)
