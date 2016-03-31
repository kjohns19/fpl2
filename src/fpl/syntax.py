import fpl.number
import fpl.operator

class Node:
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value]


class Block(Node):
    def __init__(self, nodes=[]):
        self.nodes = nodes[:]

    def add(self, node):
        self.nodes.append(node)

    def expand(self):
        return sum([node.expand() for node in self.nodes], [])


class NodeThen(Node):
    def __init__(self, ifnode, elsenode=None):
        self.ifnode = ifnode
        self.elsenode = elsenode

    def expand(self):
        ifcode = self.ifnode.expand()
        elsecode = self.elsenode.expand() if self.elsenode else []
        jmpamount = len(ifcode) + (2 if elsecode else 0)
        jmpnif = [
            fpl.number.Number(jmpamount),
            fpl.operator.Operator.get_operator('jmpnif')
        ]
        code = jmpnif + ifcode
        if elsecode:
            jmp = [
                fpl.number.Number(len(elsecode)),
                fpl.operator.Operator.get_operator('jmp')
            ]
            code += jmp + elsecode
        return code
