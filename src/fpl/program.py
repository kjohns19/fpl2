import fpl.tokenizer
import fpl.parser
import fpl.stack
import fpl.storage
import fpl.utils
import fpl.number
import os
import os.path

class Program:
    def __init__(self, path, debug, limit):
        self.path = path
        fpl.utils.clear_path(self.path)
        os.makedirs(self.path)
        os.chdir(self.path)
        self.tmpdir = fpl.storage.Storage(os.path.abspath('_tmp'))
        self.heap = fpl.storage.Storage(os.path.abspath('_heap'))
        self.stack = fpl.stack.Stack(os.path.abspath('_stack'))
        self.code = fpl.storage.Storage(os.path.abspath('_code'))
        self.debug = debug
        self.limit = limit
        os.makedirs('_')
        os.chdir('_')
        ret = fpl.variable.Variable('_return', fpl.number.Number(-1))
        ret.save()

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
        while self.limit <= 0 or total < self.limit:
            counter = self.code.counter()
            if counter.value.value < 0:
                break
            current = self.code.get_at(counter.value.value)
            if os.path.isfile(current.path) or os.path.isdir(current.path):
                current.load()
            else:
                break
            counter.value.value += 1
            counter.save()

            if self.debug:
                pc = counter.value.value-1
                print(str(pc) + ': ' + type(current.value).__name__ + ': ' + str(current.value))
            current.value.apply(self)
            total += 1
        if self.limit > 0 and total == self.limit:
            print('Possible infinite loop! (limit=' + str(self.limit) + ')')
        if self.debug:
            self.stack.debug()

    def exit_function(self):
        return_point = fpl.variable.Variable('_return', do_load=True)
        return_value = self.stack.pop().value
        self.goto(return_point.value.value)
        os.chdir('..')
        fpl.utils.clear_path('_')
        #print('Return value: <' + str(return_value) + '>')
        return_value.apply(self)

    def jump(self, amount):
        counter = self.code.counter()
        counter.value.value += amount
        counter.save()

    def goto(self, address):
        counter = self.code.counter()
        counter.value.value = address
        counter.save()

    def counter(self):
        counter = self.code.counter()
        return counter.value.value
