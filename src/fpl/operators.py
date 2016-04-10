import fpl.operator
import fpl.utils
import fpl.error
import fpl.variable
import fpl.number
import fpl.pointer
import fpl.string
import fpl.symbol
import operator
import os.path
import random
import sys

def __expect_type(op, value, expected):
    if not isinstance(expected, (list, tuple)):
        expected = [expected]
    if type(value) not in expected:
        if len(expected) == 1:
            expectstr = expected[0].__name__
        else:
            expectstr = 'one of (' + ', '.join(t.__name__ for t in expected) + ')'
        raise fpl.error.Error('Invalid type for ' + op + ': Expected ' + expectstr + ', got ' + type(value).__name__)

# Basic binary (arithmetic, boolean, etc)
__result_types = {
    int:   fpl.number.Number,
    float: fpl.number.Number,
    bool:  fpl.number.Number,
    str:   fpl.string.String
}
def __operator(opname, op):
    def __func(a, b):
        for val in (a, b):
            __expect_type(opname, val, (fpl.number.Number, fpl.string.String))
        result = op(a.value, b.value)
        result_type = __result_types.get(type(result))
        if not result_type:
            err = 'Invalid result type ' + str(type(result)) + ' from operator ' + str(op)
            raise fpl.error.Error(err)
        return result_type(result)
    return fpl.utils.create_operator(__func)

__operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
}
for op, func in __operators.items():
    fpl.operator.Operator.add_operator(op, __operator(op, func))

def __eq(a, b):
    return fpl.number.Number(a.value == b.value)
fpl.operator.Operator.add_operator('==', fpl.utils.create_operator(__eq))
def __ne(a, b):
    return fpl.number.Number(a.value != b.value)
fpl.operator.Operator.add_operator('!=', fpl.utils.create_operator(__ne))


# Input/Output
def __get():
    return fpl.string.String(input())
fpl.operator.Operator.add_operator('get', fpl.utils.create_operator(__get))

def __print(value):
    value.print()
fpl.operator.Operator.add_operator('print', fpl.utils.create_operator(__print))



# Jump operators
def __jump(program):
    amount = program.stack.pop().value
    __expect_type('jmp', amount, fpl.number.Number)
    program.jump(amount.value)
fpl.operator.Operator.add_operator('jmp', __jump)
    
def __jump_if(program):
    amount = program.stack.pop().value
    __expect_type('jmpif', amount, fpl.number.Number)
    check = program.stack.pop().value
    if check.is_true():
        program.jump(amount.value)
fpl.operator.Operator.add_operator('jmpif', __jump_if)

def __jump_not_if(program):
    amount = program.stack.pop().value
    __expect_type('jmpnif', amount, fpl.number.Number)
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
    __expect_type('deref', value, fpl.pointer.Pointer)
    return fpl.symbol.Symbol(value.value)
fpl.operator.Operator.add_operator('deref', fpl.utils.create_operator(__deref))

def __heap(program):
    path = program.heap.get_new().path
    fpl.pointer.Pointer(path).apply(program)
fpl.operator.Operator.add_operator('heap', __heap)



# Function
def __fun(program):
    stack = program.stack
    count = stack.pop().value
    __expect_type('fun', count, fpl.number.Number)
    args = [ os.path.basename(stack.pop(do_load=False).path) for i in range(count.value) ]
    code_start = program.counter()+2
    func = fpl.function.Function(args, code_start)
    func.apply(program)
fpl.operator.Operator.add_operator('fun', __fun)

def __call(program):
    func = program.stack.pop().value
    __expect_type('call', func, fpl.function.Function)
    func.call(program)
fpl.operator.Operator.add_operator('call', __call)

def __return(program):
    program.exit_function()
fpl.operator.Operator.add_operator('return', __return)



# Conversions

def __num(value):
    __expect_type('num', value, fpl.string.String)
    return fpl.number.Number(int(value.value))
fpl.operator.Operator.add_operator('num', fpl.utils.create_operator(__num))

def __str(value):
    return fpl.string.String(str(value))
fpl.operator.Operator.add_operator('str', fpl.utils.create_operator(__str))

# Other
def __assign(program):
    stack = program.stack
    value = stack.pop()
    dest = stack.pop(do_load=False)
    if dest.is_tmp():
        raise fpl.error.Error('Cannot assign to temporary')
    dest.value = value.value
    dest.save()
fpl.operator.Operator.add_operator('=', __assign)

def __at(program):
    stack = program.stack
    value = stack.pop().value
    __expect_type('at', value, (fpl.number.Number, fpl.string.String))
    obj = stack.pop(do_load=False)
    if not os.path.isdir(obj.path):
        obj.load()
        __expect_type('at', obj.value, fpl.object.Object)
    var = fpl.variable.Variable(os.path.join(obj.path, str(value)))
    stack.push(var)
fpl.operator.Operator.add_operator('at', __at)

def __delete(program):
    value = program.stack.pop(do_load=False)
    if value.is_tmp():
        raise fpl.error.Error('Cannot delete temporary')
    fpl.utils.clear_path(value.path)
fpl.operator.Operator.add_operator('delete', __delete)

def __rand(min, max):
    for val in (min, max):
        __expect_type('rand', val, fpl.number.Number)
    return fpl.number.Number(random.randint(min.value, max.value))
fpl.operator.Operator.add_operator('rand', fpl.utils.create_operator(__rand))
