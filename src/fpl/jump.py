import fpl.operator

def __jump(program):
    address = program.stack.pop().value
    program.goto(address.value)
    
def __jump_if(program):
    address = program.stack.pop().value
    check = program.stack.pop().value
    if check.is_true():
        program.goto(address.value)

fpl.operator.Operator.add_operator('jmp', __jump)
fpl.operator.Operator.add_operator('jmpif', __jump_if)
