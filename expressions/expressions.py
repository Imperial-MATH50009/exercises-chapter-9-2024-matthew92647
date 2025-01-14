import numbers
from functools import singledispatch
class Expression:
    def __init__(self, *operands):
        self.operands = operands

    def __add__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Add(self, other)
    
    def __sub__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Sub(self, other)
    
    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Mul(self, other)
    
    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Div(self, other)
 
    def __pow__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Pow(self, other)

    def __radd__(self, other):
        return Add(Number(other), self)

    def __rsub__(self, other):
        return Sub(Number(other), self)
    
    def __rmul__(self, other):
        return Mul(Number(other), self)
    
    def __rtruediv__(self, other):
        return Div(Number(other), self)
    
    def __rpow__(self, other):
        return Pow(Number(other), self)


class Operator(Expression):
    def __repr__(self):
        return (type(self).__name__ + repr(self.operands))

    def __str__(self):
        pre = self.precedence
        pre1, pre2 = self.operands[0].precedence, self.operands[1].precedence
        if pre1 < pre and pre2 < pre:
            return f"({self.operands[0]}) {self.symbol} ({self.operands[1]})"
        elif pre1 < pre and pre2 >= pre:
            return f"({self.operands[0]}) {self.symbol} {self.operands[1]}"
        elif pre1 >= pre and pre2 < pre:
            return f"{self.operands[0]} {self.symbol} ({self.operands[1]})"
        else:
            return f"{self.operands[0]} {self.symbol} {self.operands[1]}"

class Terminal(Expression):
    precedence = 5

    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def __repr__(self):
        return repr(self.value)
    
    def __str__(self):
        return str(self.value)
  

class Number(Terminal):

    def __init__(self, value):
        super().__init__(value)
        self._validate()

    def _validate(self):
        if not isinstance(self.value, numbers.Number):
            raise ValueError("Element must be a number, not "
                             f"{type(self.value).__name__}")
        

class Symbol(Terminal):
    def __init__(self, value):
        super().__init__(value)
        self._validate()

    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Element must be a symbol, not "
                             f"{type(self.value).__name__}")
    

class Add(Operator):
    symbol = "+"
    precedence = 1


class Sub(Operator):
    symbol = "-"
    precedence = 1


class Mul(Operator):
    symbol = "*"
    precedence = 2


class Div(Operator):
    symbol = "/"
    precedence = 2


class Pow(Operator):
    symbol  = "^"
    precedence = 3


def postvisitor(expr, fn, **kwargs):
    stack = [expr]
    visited = {}
    while stack:
        e = stack.pop()
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)
        
        if unvisited_children:
            stack.append(e)
            stack += unvisited_children
        else:
            visited[e] = fn(e, *(visited[o] for o in e.operands), **kwargs)

    return visited[expr]

