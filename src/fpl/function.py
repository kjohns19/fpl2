import fpl.value
import fpl.number
import fpl.variable
import os
import os.path

class Function(fpl.value.Value):
    @staticmethod
    def deserialize(data):
        split = data.split('\n')
        args = list(reversed(split[0].split()))
        code_start = int(split[1])
        #print('Args: <' + '>, <'.join(args) + '>, code_start: ' + str(code_start))
        return Function(args, code_start)

    def __init__(self, args, code_start):
        self.args = args
        self.code_start = code_start

    def call(self, program):
        stack = program.stack
        arguments = [stack.pop().value for i in range(len(self.args))]
        os.makedirs('_')
        os.chdir('_')
        for arg, name in zip(arguments, self.args):
            var = fpl.variable.Variable(name, arg)
            var.save()
        savepos = fpl.variable.Variable('_return', fpl.number.Number(program.counter()))
        savepos.save()
        program.goto(self.code_start)

    def __str__(self):
        return ' '.join(reversed(self.args)) + '\n' + str(self.code_start)

fpl.value.Value.register_type('Function', Function)
