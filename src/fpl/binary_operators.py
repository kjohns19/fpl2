import fpl.operator
import fpl.utils
import operator

def __operator(op):
    def __func(a, b):
        result = op(a.value, b.value)
        return type(a)(result)
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


def __assign(program):
    stack = program.stack
    value = stack.pop()
    dest = stack.pop(do_load=False)
    dest.value = value.value
    dest.save()
fpl.operator.Operator.add_operator('=', __assign)
