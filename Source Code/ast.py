# Galang, Angelika
# Gonzales Justin
# CS 150: MP - Naruto Language

''' 
This file contains the classes that are responsible for storing the 
Abstract Syntax Tree of the Naruto Language.
'''

from __future__ import print_function
import operator # <-- for binary and unary operators
import interpreter

symbols = interpreter.SymbolTable() # <-- gets the symbol table from the interpreter

# PYTHON SPECIAL OBJECT PROPERTIES #
# __init__ functions are for initialization of the objects of the class
# __len__ functions return the length of the object specified
# __iter__ functions return iterator objects
# __repr__ functions return string representation of a class instance


class Node:
    def __init__(self,children=None): 
        if children is None:
            children = []
        self.children = children

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __repr__(self):
        return '<Node {0}>'.format(self.children)

    def evaluate(self):
        '''
        Function responsible for evaluating all the children of the
        class and returning their results from their own evaluate
        method as a list.
        '''
        returnList = []
        for i in self:              
            if isinstance(i,Exit): # <-- condition if a certain evaluation is not implemented
                return i

            result = i.evaluate()

            if isinstance(result,Exit): # <-- another condition if a certain evaluation is not implemented
                return result

            elif result is not None:    # <-- evaluation implemented; appends the evaluated result to the return list
                returnList.append(result)

        return returnList

class BaseClass:
    '''
    Class responsible for raising a built-in exception in Python
    called NotImplementedError. This represents the base class that
    is called when abstract methods require derived classes to override a method.
    '''
    def evaluate(self):
        raise NotImplementedError()

class Exit(BaseClass):
    '''
    Class that returns an empty iterator object and evaluates a
    pass statement--no command or code to execute.
    '''
    def __iter__(self):
        return []

    def evaluate(self):
        pass

class Print(BaseClass):
    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return '<Print {0}>'.format(self.items)

    def evaluate(self):
        '''
        Function responsible for assigning a print function to @byakugan
        and actually print the statements passed in it.
        '''
       
        print(*self.items.evaluate(), sep='', end='') # separator and end string are set to be empty

class Primitive(BaseClass):
    def __init__(self,value):
        self.value = value

    def __repr__(self):
        return '<Primitive "{0}"({1})>'.format(self.value,self.value.__class__)

    def evaluate(self):
        '''
        Function that returns the value of the primitive data passed.
        '''
        return self.value   

class Identifier(BaseClass):
    isFxn = False

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Identifier {0}>'.format(self.name)

    def assign(self,val):
        '''
        Function that assigns the identifier to its value.
        '''
        if self.isFxn: # <-- if identifier is being assigned to a function
            symbols.set_func(self.name,val)
        else: # <-- if identifier is being assigned to a single value
            symbols.set_sym(self.name,val)

    def evaluate(self):
        '''
        Function that returns the attributes of the identifier from the symbol table.
        '''
        if self.isFxn:
            return symbols.get_func(self.name)

        return symbols.get_sym(self.name)

class Assignment(BaseClass):
    def __init__(self, identifier, val):
        self.identifier = identifier
        self.val = val

    def __repr__(self):
        return '<Assignment sym={0}; val={1}>'.format(self.identifier, self.val)

    def evaluate(self):
        if self.identifier.isFxn:
            self.identifier.assign(self.val)
        else:
            self.identifier.assign(self.val.evaluate())


class BinaryOperation(BaseClass):
    __operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '%': operator.mod,
        '/': operator.truediv,


        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '~=': operator.ne,
    }

    def __repr__(self):
        return '<BinaryOperation left ={0} right={1} operation="{2}">'.format(self.left, self.right, self.op)

    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def evaluate(self):
        left = None
        right = None

        try:
            # find the operation that needs to be performed
            op = self.__operations[self.op]

            # The only lambda operations are logical and/or
            # Pass the arguments unevaluated as they will be during the lambda execution
            # This implements short circuit boolean evaluation

            # otherwise, straight up call the operation, also save the variables
            # in case they are to be used for the exception block
            left = self.left.evaluate()
            right = self.right.evaluate()
            return op(left, right)
        except TypeError:
            fmt = (left.__class__.__name__, left, self.op, right.__class__.__name__, right)
            raise Exception("Unable to apply operation (%s: %s) %s (%s: %s)" % fmt)


class UnaryOperation(BaseClass):
    __operations = {
        '-': operator.neg,
        '~': operator.not_
    }

    def __repr__(self):
        return '<Unary operation: operation={0} expr={1}>'.format(self.operation, self.expr)

    def __init__(self, operation, expr):
        self.operation = operation
        self.expr = expr

    def evaluate(self):
        return self.__operations[self.operation](self.expr.evaluate())

class Array(BaseClass):
    def __init__(self,values):
        self.values = values

    def __repr__(self):
        return '<Array len={0} items={1}>'.format(len(self.values.children), self.values)

    def evaluate(self):
        '''
        
        '''
        return self.values.evaluate()

class ArrayAccess(BaseClass):
    def __init__(self, array, index):
        self.array = array
        self.index = index

    def __repr__(self):
        return '<Array index {0}>'.format(self.index)

    def evaluate (self):
        return self.array.evaluate()[self.index.evaluate()]

class ArrayAssign(BaseClass):
    def __init__(self, array, index, value):
        self.array = array
        self.index = index
        self.value = value

    def __repr__(self):
        return '<Array arr={0} index={1} value={2}>'.format(self.array, self.index, self.value)

    def evaluate(self):
        self.array.evaluate()[self.index.evaluate()] = self.value.evaluate()

class For(BaseClass):
    def __init__(self, variable, start, end, asc, body):
        self.variable = variable
        self.start = start
        self.end = end
        self.asc = asc  # ascending order
        self.body = body

    def __repr__(self):
        fmt = '<For start={0} direction={1} end={2} body={3}>'
        return fmt.format(self.start, 'asc' if self.asc else 'desc', self.end, self.body)

    def evaluate(self):
        if self.asc:
            lo = self.start.evaluate()
            hi = self.end.evaluate() + 1
            sign = 1
        else:
            lo = self.start.evaluate()
            hi = self.end.evaluate() - 1
            sign = -1

        for i in range(lo, hi, sign):
            self.variable.assign(i)

            # in case of exit statement prematurely break the loop
            if isinstance(self.body.evaluate(), Exit):
                break

class While(BaseClass):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return '<While cond={0} body={1}>'.format(self.condition, self.body)

    def evaluate(self):
        while self.condition.evaluate():
            if isinstance(self.body.evaluate(), Exit):
                break

class If(BaseClass):
    def __init__(self, condition, truepart, elsepart=None):
        self.condition = condition
        self.truepart = truepart
        self.elsepart = elsepart

    def __repr__(self):
        return '<If condition={0} then={1} else={2}>'.format(self.condition, self.truepart, self.elsepart)

    def evaluate(self):
        if self.condition.evaluate():
            return self.truepart.evaluate()
        elif self.elsepart is not None:
            return self.elsepart.evaluate()

def full_eval(expr):
    """
    Fully evaluates the passex expression returning it's value
    """

    while isinstance(expr, BaseClass):
        expr = expr.evaluate()

    return expr

class FunctionCall(BaseClass):
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def __repr__(self):
        return '<Function call name={0} params={1}>'.format(self.name, self.params)

    def evaluate_built_in(self):
        func = self.name.evaluate()
        args = []

        for p in self.params:
            args.append(full_eval(p))

        return func.evaluate(args)

    def evaluate(self):
        return self.evaluate_built_in

class BuiltInFxn(BaseClass):
    def __init__(self, func):
        self.func = func

    def __repr__(self):
        return '<Builtin function {0}>'.format(self.func)

    def evaluate(self, args):
        return self.func(*args)