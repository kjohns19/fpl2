import fpl.operator
import fpl.number
import fpl.symbol
import fpl.none
import fpl.bool

class Tokenizer:
    def __init__(self):
        pass

    __constants = {
        'none':  fpl.none.NoneType.value(),
        'true':  fpl.bool.Bool.true_value(),
        'false': fpl.bool.Bool.false_value()
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
            return fpl.symbol.Symbol(token)

    def tokenize(self, code):
        return [ self.tokenize_one(token) for token in code.split() ]
