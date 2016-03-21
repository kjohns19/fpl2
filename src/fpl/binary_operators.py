import fpl.operator
import operator

def __operator(op):
    def __func(program):
        stack = program.stack
        a = stack.pop()
        b = stack.pop()
        result = type(a)(op(b.value, a.value))
        stack.push(result)
    return __func

__operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv
}
for op, func in __operators.items():
    fpl.operator.Operator.add_operator(op, __operator(func))
