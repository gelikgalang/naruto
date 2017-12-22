import operator

class Node(object):
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children
    
    def append(self, val):
        self.children.append(val)
    
    def __str__(self):
        return '\n'.join(str(x) for x in self)
    
    def __iter__(self):
        return iter(self.children)
    
    def calculate(self, context):
        for node in self.children:
            n = node.calculate(context)
            if n is not None:
                return n

class Expr(object):
    def calculate(self):
        raise NotImplementedError()

class BinOp(Expr):
    OPS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.div,
        '%': operator.mod,
        '==': operator.eq,
        '~=': operator.ne,
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
    }
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
    
    def __str__(self):
        return "<BinaryOperation: %s %s %s>" % (self.left, self.op, self.right)
    
    def calculate(self, context):
        return self.OPS[self.op](self.left.calculate(context), self.right.calculate(context))

class UnaryOp(Expr):
    OPS = {
        'not': operator.not_,
    }
    def __init__(self, value, op):
        self.value = value
        self.op = op
    
    def __str__(self):
        return "<UnaryOperation: %s %s>" % (self.op, self.value)
    
    def calculate(self, context):
        return self.OPS[self.op](self.value.calculate(context))

class Number(Expr):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "<Number: %s>" % self.value
    
    def calculate(self, context):
        return self.value

class Boolean(Expr):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "<Boolean: %s>" % self.value
    
    def calculate(self, context):
        return self.value

class NoneVal(Expr):
    def __str__(self):
        return "<None>"
    
    def calculate(self, context):
        return None

class Assignment(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return "<Assignment: %s = %s>" % (self.left, self.right)
    
    def calculate(self, context):
        val = self.right.calculate(context)
        for var in self.left:
            var.assign(val, context)

class Name(Expr):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return "<Name: %s>" % self.name
    
    def assign(self, value, context):
        context[self.name] = value
    
    def calculate(self, context):
        return context[self.name]

class If(Node):
    def __init__(self, condition, main_body, else_body=None, elifs=None):
        self.condition = condition
        self.main_body = main_body
        self.else_body = else_body
        # this is a list of two tuples, in the form of (condition, body)
        self.elifs = elifs
    
    def __str__(self):
        return "<If: %s>" % self.condition
    
    def calculate(self, context):
        if self.condition.calculate(context):
            return self.main_body.calculate(context)        
        if self.elifs is not None:
            for condition, body in self.elifs:
                if condition.calculate(context):
                    return body.calculate(context)
        if self.else_body is not None:
            return self.else_body.calculate(context)

class For(Node):
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body
    
    def calculate(self, context):
        for i in self.iterable.calculate(context):
            context[self.var_name] = i
            result = self.body.calculate(context)
            if result is not None:
                return result

#class While(Node)