import fpl.tokenizer
import fpl.parser
import fpl.stack
import fpl.storage
import fpl.utils
import fpl.value
import os
import os.path

class Program:
    def __init__(self, path, debug, limit):
        self.path = os.path.abspath(path)
        self.debug = debug
        self.limit = limit
        fpl.utils.clear_path(self.path)
        os.makedirs(self.path)
        os.chdir(self.path)
        self.tmpdir = fpl.storage.Storage(os.path.abspath('_tmp'))
        self.heap = fpl.storage.Storage(os.path.abspath('_heap'))
        self.code = fpl.storage.Storage(os.path.abspath('_code'))
        self.goto(-1)
        self.jump_change_dir('_', 0)

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
        self.stack = fpl.stack.Stack(os.path.abspath('../_stack'))
        return_value.apply(self)
        last = fpl.variable.Variable('$', do_load=True)
        current = os.getcwd();
        os.chdir(last.value.value)
        fpl.utils.clear_path(current)

    def backtrace(self):
        trace = []
        path = os.getcwd()
        counter = self.counter()
        while counter != -1:
            trace.append(counter-1)
            varpath = os.path.join(path, '_return')
            counter = fpl.variable.Variable(varpath).load().value
            path = os.path.dirname(path)
        return trace

    def jump_change_dir(self, path, counter):
        cur = fpl.variable.Variable(os.path.join(self.path, '_current'))
        cur.value = fpl.value.Pointer(path)
        cur.save()
        last_path = os.getcwd();
        os.makedirs(path)
        os.chdir(path)
        ret = fpl.variable.Variable('_return', fpl.value.Number(self.counter()))
        ret.save()
        last = fpl.variable.Variable('$', fpl.value.Pointer(last_path))
        last.save()
        self.goto(counter)
        self.stack = fpl.stack.Stack(os.path.abspath('_stack'))
        

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
