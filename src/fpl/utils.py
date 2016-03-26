import os.path
import shutil
import inspect

def clear_path(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

def create_operator(func):
    num_args = len(inspect.getargspec(func).args)
    def __func(program):
        stack = program.stack
        args = [ stack.pop() for i in range(num_args) ]
        result = func(*args)
        if result:
            stack.push(result)
    return __func
