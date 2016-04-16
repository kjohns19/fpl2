import fpl.utils
import fpl.error
import fpl.variable
import fpl.value
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
    int:   fpl.value.Number,
    float: fpl.value.Number,
    bool:  fpl.value.Number,
    str:   fpl.value.String
}
def __operator(opname, op):
    def __func(a, b):
        for val in (a, b):
            __expect_type(opname, val, (fpl.value.Number, fpl.value.String))
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
    fpl.value.Operator.add_operator(op, __operator(op, func))

def __eq(a, b):
    return fpl.value.Number(a.value == b.value)
fpl.value.Operator.add_operator('==', fpl.utils.create_operator(__eq))
def __ne(a, b):
    return fpl.value.Number(a.value != b.value)
fpl.value.Operator.add_operator('!=', fpl.utils.create_operator(__ne))


# Input/Output
def __get():
    return fpl.value.String(input())
fpl.value.Operator.add_operator('get', fpl.utils.create_operator(__get))

def __print(value):
    value.print()
fpl.value.Operator.add_operator('print', fpl.utils.create_operator(__print))



# Jump operators
def __jump(program):
    amount = program.stack.pop().value
    __expect_type('jmp', amount, fpl.value.Number)
    program.jump(amount.value)
fpl.value.Operator.add_operator('jmp', __jump)
    
def __jump_if(program):
    amount = program.stack.pop().value
    __expect_type('jmpif', amount, fpl.value.Number)
    check = program.stack.pop().value
    if check.is_true():
        program.jump(amount.value)
fpl.value.Operator.add_operator('jmpif', __jump_if)

def __jump_not_if(program):
    amount = program.stack.pop().value
    __expect_type('jmpnif', amount, fpl.value.Number)
    check = program.stack.pop().value
    if not check.is_true():
        program.jump(amount.value)
fpl.value.Operator.add_operator('jmpnif', __jump_not_if)



# Pointer
def __ref(program):
    value = program.stack.pop(do_load=False)
    fpl.value.Pointer(value.path).apply(program)
fpl.value.Operator.add_operator('ref', __ref)

def __deref(value):
    __expect_type('deref', value, fpl.value.Pointer)
    return fpl.value.Symbol(value.value)
fpl.value.Operator.add_operator('deref', fpl.utils.create_operator(__deref))

def __heap(program):
    path = program.heap.get_new().path
    fpl.value.Pointer(path).apply(program)
fpl.value.Operator.add_operator('heap', __heap)



# Function
def __fun(program):
    stack = program.stack
    count = stack.pop().value
    __expect_type('fun', count, fpl.value.Number)
    args = [ os.path.basename(stack.pop(do_load=False).path) for i in range(count.value) ]
    code_start = program.counter()+2
    func = fpl.value.Function(args, code_start)
    func.apply(program)
fpl.value.Operator.add_operator('fun', __fun)

def __call(program):
    func = program.stack.pop().value
    __expect_type('call', func, fpl.value.Function)
    func.call(program)
fpl.value.Operator.add_operator('call', __call)

def __return(program):
    program.exit_function()
fpl.value.Operator.add_operator('return', __return)



# Conversions

def __num(value):
    __expect_type('num', value, fpl.value.String)
    return fpl.value.Number(int(value.value))
fpl.value.Operator.add_operator('num', fpl.utils.create_operator(__num))

def __str(value):
    return fpl.value.String(str(value))
fpl.value.Operator.add_operator('str', fpl.utils.create_operator(__str))

# Other
def __assign(program):
    stack = program.stack
    value = stack.pop()
    dest = stack.pop(do_load=False)
    if dest.is_tmp():
        raise fpl.error.Error('Cannot assign to temporary')
    dest.value = value.value
    dest.save()
fpl.value.Operator.add_operator('=', __assign)

def __at(program):
    stack = program.stack
    value = stack.pop().value
    __expect_type('at', value, (fpl.value.Number, fpl.value.String))
    obj = stack.pop(do_load=False)
    if not os.path.isdir(obj.path):
        obj.load()
        __expect_type('at', obj.value, fpl.value.Object)
    var = fpl.variable.Variable(os.path.join(obj.path, str(value)))
    stack.push(var)
fpl.value.Operator.add_operator('at', __at)

def __delete(program):
    value = program.stack.pop(do_load=False)
    if value.is_tmp():
        raise fpl.error.Error('Cannot delete temporary')
    fpl.utils.clear_path(value.path)
fpl.value.Operator.add_operator('delete', __delete)

def __rand(min, max):
    for val in (min, max):
        __expect_type('rand', val, fpl.value.Number)
    return fpl.value.Number(random.randint(min.value, max.value))
fpl.value.Operator.add_operator('rand', fpl.utils.create_operator(__rand))

def __seed(value):
    __expect_type('seed', value, fpl.value.Number)
    random.seed(value.value)
fpl.value.Operator.add_operator('seed', fpl.utils.create_operator(__seed))
