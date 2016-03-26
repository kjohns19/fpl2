import fpl.tokenizer
import fpl.stack
import fpl.storage
import fpl.utils
import os
import os.path

class Program:
    def __init__(self):
        self.path = '_fpl_runtime'
        fpl.utils.clear_path(self.path)
        os.makedirs(self.path)
        self.tmpdir = fpl.storage.Storage(os.path.join(self.path, '_tmp'))
        self.stack = fpl.stack.Stack(os.path.join(self.path, '_stack'), self.tmpdir)

    def run_file(self, filename):
        with open(filename, 'r') as f:
            code = f.read()
        return self.run_code(code)

    def run_code(self, code):
        tokenizer = fpl.tokenizer.Tokenizer()
        tokens = tokenizer.tokenize(code)
        for token in tokens:
            print(type(token).__name__ + ': ' + str(token))
            token.apply(self)
        self.stack.debug()
