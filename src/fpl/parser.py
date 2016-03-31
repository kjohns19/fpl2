import fpl.syntax
import fpl.symbol
import sys

class Parser:
    def __init__(self):
        pass

    def parse(self, tokenization):
        parsed, index = self.__parse(tokenization)
        expanded = parsed.expand()
        print(expanded)
        return expanded

    def __parsethen(self, tokenization, index):
        ifnode, index = self.__parse(tokenization, index=index, allowelse=True, allowend=True)
        elsenode = None
        if tokenization[index].value == 'else':
            elsenode, index = self.__parse(tokenization, index=index+1, allowelse=False, allowend=True)
        if tokenization[index].value != 'end':
            #TODO throw something here
            print('ERROR: Expected \'end\'', file=sys.stderr)
            sys.exit(1)
        return fpl.syntax.NodeThen(ifnode, elsenode), index
        
    def __parse(self, tokenization, index=0, allowelse=False, allowend=False):
        block = fpl.syntax.Block()
        while index < len(tokenization):
            token = tokenization[index]
            node = None

            if type(token) is fpl.symbol.Symbol:
                for value, allowed in [('else', allowelse), ('end', allowend)]:
                    if token.value == value:
                        if allowed:
                            return block, index
                        #TODO throw something here
                        print('ERROR: Unexpected \'' + value + '\'', file=sys.stderr)
                        sys.exit(1)
                if token.value == 'then':
                    node, index = self.__parsethen(tokenization, index=index+1)

            if not node:
                node = fpl.syntax.Node(token)

            block.add(node)
            index += 1
        return block, index
