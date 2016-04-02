import fpl.tokenizer
import fpl.parser
import fpl.stack
import fpl.storage
import fpl.utils
import os
import os.path

class Program:
    def __init__(self, path, debug):
        self.path = path
        fpl.utils.clear_path(self.path)
        os.makedirs(self.path)
        self.tmpdir = fpl.storage.Storage(os.path.join(self.path, '_tmp'))
        self.stack = fpl.stack.Stack(os.path.join(self.path, '_stack'))
        self.code = fpl.storage.Storage(os.path.join(self.path, '_code'))
        self.debug = debug

    def run_file(self, filename):
        with open(filename, 'r') as f:
            code = f.read()
        return self.run_code(code)

    def run_code(self, code):
        tokenizer = fpl.tokenizer.Tokenizer()
        tokens = tokenizer.tokenize(code)
        parsed = fpl.parser.Parser(self.debug).parse(tokens)
        savecounter = self.code.counter()
        for token in parsed:
            var = self.code.get_new()
            var.value = token
            var.save()
        savecounter.save()
        self.run_program()

    def run_program(self):
        total = 0
        limit = 1000
        while total < limit:
            counter = self.code.counter()
            current = self.code.get_at(counter.value.value)
            if os.path.isfile(current.path):
                current.load()
            else:
                break
            counter.value.value += 1
            counter.save()

            if self.debug:
                print(type(current.value).__name__ + ': ' + str(current.value))
            current.value.apply(self)
            total += 1
        if total == limit:
            print('Possible infinite loop!')
        if self.debug:
            self.stack.debug()

    def jump(self, amount):
        counter = self.code.counter()
        counter.value.value += amount
        counter.save()
