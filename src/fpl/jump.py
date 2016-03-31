import fpl.operator

def __jump(program):
    amount = program.stack.pop().value
    program.jump(amount.value)
    
def __jump_if(program):
    amount = program.stack.pop().value
    check = program.stack.pop().value
    if check.is_true():
        program.jump(amount.value)

def __jump_not_if(program):
    amount = program.stack.pop().value
    check = program.stack.pop().value
    if not check.is_true():
        program.jump(amount.value)

fpl.operator.Operator.add_operator('jmp', __jump)
fpl.operator.Operator.add_operator('jmpif', __jump_if)
fpl.operator.Operator.add_operator('jmpnif', __jump_not_if)
