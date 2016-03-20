import fpl.operator
import fpl.number
import fpl.symbol

class Tokenizer:
    def __init__(self):
        pass

    def tokenize_one(self, token):
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
