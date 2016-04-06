import fpl.operator
import fpl.utils
import fpl.variable
import fpl.number
import fpl.pointer
import fpl.symbol
import operator
import os.path
import random

# Basic binary (arithmetic, boolean, etc)
__result_types = {
    int:   fpl.number.Number,
    float: fpl.number.Number,
    bool:  fpl.number.Number
}
def __operator(op):
    def __func(a, b):
        result = op(a.value, b.value)
        result_type = __result_types.get(type(result))
        if not result_type:
            #TODO throw exception here
            print('ERROR: Invalid result type ' + str(type(result)) + ' from operator ' + str(op), file=sys.stderr)
            return fpl.number.NoneType.singleton()
        return result_type(result)
    return fpl.utils.create_operator(__func)

__operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
}
for op, func in __operators.items():
    fpl.operator.Operator.add_operator(op, __operator(func))



# Input/Output
def __get(program):
    value = fpl.number.Number(int(input()))
    value.apply(program)
fpl.operator.Operator.add_operator('get', __get)

def __print(value):
    value.print()
fpl.operator.Operator.add_operator('print', fpl.utils.create_operator(__print))



# Jump operators
def __jump(program):
    amount = program.stack.pop().value
    program.jump(amount.value)
fpl.operator.Operator.add_operator('jmp', __jump)
    
def __jump_if(program):
    amount = program.stack.pop().value
    check = program.stack.pop().value
    if check.is_true():
        program.jump(amount.value)
fpl.operator.Operator.add_operator('jmpif', __jump_if)

def __jump_not_if(program):
    amount = program.stack.pop().value
    check = program.stack.pop().value
    if not check.is_true():
        program.jump(amount.value)
fpl.operator.Operator.add_operator('jmpnif', __jump_not_if)



# Pointer
def __ref(program):
    value = program.stack.pop(do_load=False)
    fpl.pointer.Pointer(value.path).apply(program)
fpl.operator.Operator.add_operator('ref', __ref)

def __deref(value):
    return fpl.symbol.Symbol(value.value)
fpl.operator.Operator.add_operator('deref', fpl.utils.create_operator(__deref))

def __heap(program):
    path = program.heap.get_new().path
    fpl.pointer.Pointer(path).apply(program)
fpl.operator.Operator.add_operator('heap', __heap)



# Function
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



# Other
def __assign(program):
    stack = program.stack
    value = stack.pop()
    dest = stack.pop(do_load=False)
    dest.value = value.value
    dest.save()
fpl.operator.Operator.add_operator('=', __assign)

def __at(program):
    stack = program.stack
    value = stack.pop()
    obj = stack.pop(do_load=False)
    var = fpl.variable.Variable(os.path.join(obj.path, str(value.value)))
    stack.push(var)
fpl.operator.Operator.add_operator('at', __at)

def __delete(program):
    value = program.stack.pop(do_load=False)
    fpl.utils.clear_path(value.path)
fpl.operator.Operator.add_operator('delete', __delete)

def __rand(value):
    return fpl.number.Number(random.randint(0, value.value))
fpl.operator.Operator.add_operator('rand', fpl.utils.create_operator(__rand))
