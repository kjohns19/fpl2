import fpl.operator
import fpl.number
import fpl.symbol
import fpl.none
import fpl.object
import os.path

class Tokenizer:
    def __init__(self):
        pass

    __constants = {
        'none':  fpl.none.NoneType.singleton(),
        'true':  fpl.number.Number(1),
        'false': fpl.number.Number(0),
        'obj':   fpl.object.Object()
    }
    def tokenize_one(self, token):
        constant = Tokenizer.__constants.get(token)
        if constant:
            return constant

        operator = fpl.operator.Operator.get_operator(token)
        if operator:
            return operator

        try:
            val = int(token)
            return fpl.number.Number(val)
        except ValueError:
            path = os.path.join(*token.split('.'))
            return fpl.symbol.Symbol(path)

    def tokenize(self, code):
        return [ self.tokenize_one(token) for token in code.split() ]
