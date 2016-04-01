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
    def __init__(self, condition, ifnode, elsenode=None):
        self.condition = condition
        self.ifnode = ifnode
        self.elsenode = elsenode

    def expand(self):
        condition = self.condition.expand()
        ifcode = self.ifnode.expand()
        elsecode = self.elsenode.expand() if self.elsenode else []
        jmpamount = len(ifcode) + (2 if elsecode else 0)
        jmpnif = [
            fpl.number.Number(jmpamount),
            fpl.operator.Operator.get_operator('jmpnif')
        ]
        code = condition + jmpnif + ifcode
        if elsecode:
            jmp = [
                fpl.number.Number(len(elsecode)),
                fpl.operator.Operator.get_operator('jmp')
            ]
            code += jmp + elsecode
        return code

class NodeWhile(Node):
    def __init__(self, condition, whilenode):
        self.condition = condition
        self.whilenode = whilenode

    def expand(self):
        condition = self.condition.expand()
        whilenode = self.whilenode.expand()
        jmpnif = [
            fpl.number.Number(len(whilenode)+2),
            fpl.operator.Operator.get_operator('jmpnif')
        ]
        jmp = [
            fpl.number.Number(-(len(condition) + len(whilenode) + 4)),
            fpl.operator.Operator.get_operator('jmp')
        ]
        return condition + jmpnif + whilenode + jmp

