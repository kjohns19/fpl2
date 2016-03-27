import fpl.operator
import fpl.utils
import fpl.pointer
import fpl.symbol

def __print(value):
    print(value.value)
fpl.operator.Operator.add_operator('print', fpl.utils.create_operator(__print))

def __ref(program):
    value = program.stack.pop(do_load=False)
    fpl.pointer.Pointer(value.path).apply(program)
fpl.operator.Operator.add_operator('ref', __ref)

def __deref(value):
    return fpl.symbol.Symbol(value.value)
fpl.operator.Operator.add_operator('deref', fpl.utils.create_operator(__deref))
