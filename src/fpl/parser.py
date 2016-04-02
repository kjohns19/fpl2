import fpl.syntax
import fpl.symbol
import sys

class Parser:
    def __init__(self, debug):
        self.debug = debug

    def parse(self, tokenization):
        parsed, index = self.__parse(tokenization)
        expanded = parsed.expand()
        if self.debug:
            print(expanded)
        return expanded

    def __parse_if(self, tokenization, index):
        condition, index = self.__parse(tokenization, index=index, stop=['then'])
        ifnode, index = self.__parse(tokenization, index=index+1, stop=['else', 'end'])
        elsenode = None
        if tokenization[index].value == 'else':
            elsenode, index = self.__parse(tokenization, index=index+1, stop=['end'])
        return fpl.syntax.NodeThen(condition, ifnode, elsenode), index

    def __parse_while(self, tokenization, index):
        print('Parsing while')
        condition, index = self.__parse(tokenization, index=index, stop=['do'])
        whilenode, index = self.__parse(tokenization, index=index+1, stop=['end'])
        print('Done parsing while')
        return fpl.syntax.NodeWhile(condition, whilenode), index
        
    def __parse(self, tokenization, index=0, stop=[]):
        block = fpl.syntax.Block()
        while index < len(tokenization):
            token = tokenization[index]
            node = None

            if type(token) is fpl.symbol.Symbol:
                if token.value in stop:
                    return block, index
                if token.value in ['then', 'do', 'else', 'end']: #TODO don't hardcode this?
                    #TODO throw something here
                    print('ERROR: Unexpected \'' + token.value + '\'', file=sys.stderr)
                    print('Stop=' + str(stop))
                    sys.exit(1)
                if token.value == 'if':
                    node, index = self.__parse_if(tokenization, index=index+1)
                elif token.value == 'while':
                    node, index = self.__parse_while(tokenization, index=index+1)

            if not node:
                node = fpl.syntax.Node(token)
            block.add(node)
            index += 1

        if stop:
            #TODO throw something here
            if len(stop) == 1:
                msg = '\'' + stop[0] + '\''
            else:
                msg = 'one of (\'' + '\', \''.join(stop) + '\')'
            print('ERROR: Expected ' + msg, file=sys.stderr)
            sys.exit(1)
        return block, index
