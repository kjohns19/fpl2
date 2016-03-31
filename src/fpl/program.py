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
        self.stack = fpl.stack.Stack(os.path.join(self.path, '_stack'))
        self.code = fpl.storage.Storage(os.path.join(self.path, '_code'))

    def run_file(self, filename):
        with open(filename, 'r') as f:
            code = f.read()
        return self.run_code(code)

    def run_code(self, code):
        tokenizer = fpl.tokenizer.Tokenizer()
        tokens = tokenizer.tokenize(code)
        savecounter = self.code.counter()
        for token in tokens:
            var = self.code.get_new()
            var.value = token
            var.save()
        savecounter.save()
        self.run_program()

    def run_program(self):
        while True:
            counter = self.code.counter()
            current = self.code.get_at(counter.value.value)
            if os.path.isfile(current.path):
                current.load()
            else:
                break
            counter.value.value += 1
            counter.save()

            print(type(current.value).__name__ + ': ' + str(current.value))
            current.value.apply(self)
        self.stack.debug()

    def jump(self, amount):
        counter = self.code.counter()
        counter.value.value += amount
        counter.save()
