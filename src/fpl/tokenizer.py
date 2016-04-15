import fpl.operator
import fpl.number
import fpl.symbol
import fpl.string
import fpl.none
import fpl.object
import os.path
import re

class Tokenizer:
    def __init__(self):
        pass

    __str_rep = {
        '\\n': '\n',
        '\\t': '\t',
        '\\\'': '\'',
        '\\"': '"',
    }
    __str_rep_pattern = re.compile('|'.join(re.escape(k) for k in __str_rep.keys()))

    __constants = {
        'none':  fpl.none.NoneType.singleton(),
        'true':  fpl.number.Number(1),
        'false': fpl.number.Number(0),
        'obj':   fpl.object.Object()
    }
    def tokenize_one(self, token):
        if token[0] == '"' and token[-1] == '"':
            return fpl.string.String(token[1:-1])

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

    def tokenize_string(self, token):
        subfunc = lambda m: Tokenizer.__str_rep[m.group(0)]
        text = Tokenizer.__str_rep_pattern.sub(subfunc, token)
        return fpl.string.String(text)


    def tokenize(self, code):
        result = []
        for line in code.splitlines():
            inquote = False
            for part in re.split(r'(?<!\\)"', line):
                skiprest = False
                if inquote:
                    result.append(self.tokenize_string(part))
                else:
                    if '#' in part:
                        part = part[0:part.index('#')]
                        skiprest = True
                    result += [ self.tokenize_one(token) for token in part.split() ]
                inquote = not inquote
                if skiprest:
                    break
            if not inquote:
                raise fpl.error.Error('Expected "')
        return result
