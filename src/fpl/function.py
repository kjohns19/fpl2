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
        return Function(args, code_start)

    def __init__(self, args, code_start):
        self.args = args
        self.code_start = code_start

    def call(self, program):
        stack = program.stack
        arguments = [stack.pop().value for i in range(len(self.args))]
        program.jump_change_dir('_', self.code_start)
        for arg, name in zip(arguments, self.args):
            var = fpl.variable.Variable(name, arg)
            var.save()

    def print(self):
        print('<function>')

    def __str__(self):
        return ' '.join(reversed(self.args)) + '\n' + str(self.code_start)

fpl.value.Value.register_type('Function', Function)
