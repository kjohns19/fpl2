import fpl.operator
import os.path

def __fun(program):
    stack = program.stack
    count = stack.pop().value.value
    args = [ os.path.basename(stack.pop(do_load=False).path) for i in range(count) ]
    code_start = program.counter()+2
    func = fpl.function.Function(args, code_start)
    func.apply(program)
fpl.operator.Operator.add_operator('fun', __fun)

def __call(program):
    func = program.stack.pop()
    func.value.call(program)
fpl.operator.Operator.add_operator('call', __call)

def __return(program):
    program.exit_function()
fpl.operator.Operator.add_operator('return', __return)
