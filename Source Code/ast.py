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


class Node:
    def __init__(self,children=None): 
        if children is None:
            children = []
        self.children = children

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def evaluate(self):
        '''
        Function responsible for evaluating all the children of the
        class and returning their results from their own evaluate
        method as a list.
        '''
        returnList = []
        for i in self:              
            if isinstance(i,Break): # <-- condition if a certain evaluation is not implemented
                return i

            result = i.evaluate()

            if isinstance(result,Break): # <-- another condition if a certain evaluation is not implemented
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

class Break(BaseClass):
    '''
    Class that returns an empty iterator object and evaluates a
    pass statement--no command or code to execute. Class for
    break (@kai) cases.
    '''
    def __iter__(self):
        return []

    def evaluate(self):
        pass

class Print(BaseClass):
    def __init__(self, items):
        self.items = items

    def evaluate(self):
        '''
        Function responsible for assigning a print function to @byakugan
        and actually print the statements passed in it.
        '''   
        print(*self.items.evaluate(), sep='', end='') # separator and end string are set to be empty

class ReturnValue(BaseClass):
    def __init__(self,value):
        self.value = value

    def evaluate(self):
        '''
        Function that returns the value of the primitive data passed.
        '''
        return self.value   

class Identifier(BaseClass):
    def __init__(self,name):
        self.name = name

    def assign(self,val):
        '''
        Function that assigns the identifier to its value.
        '''
        symbols.set_sym(self.name,val)

    def evaluate(self):
        '''
        Function that returns the attributes of the identifier from the symbol table.
        '''
        return symbols.get_sym(self.name)

class Assignment(BaseClass):
    def __init__(self, identifier, val):
        self.identifier = identifier
        self.val = val

    def evaluate(self):
        '''
        Function that assigns the given value to the given identifier.
        '''
        self.identifier.assign(self.val.evaluate())


class BinOp(BaseClass):
    oper = { # <-- Uses the operator module to assign operator value to the token specified
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '%': operator.mod,
        '/': operator.div,
        '//': operator.truediv,
        '**': operator.pow,


        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '~=': operator.ne,
    }

    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def evaluate(self):
        '''
        Function that evaluates the two expressions passed in correspondence
        to the operator passed as well.
        '''
        left = None
        right = None     
        op = self.oper[self.op] # looks for the operator passed in the list of operations
        left = self.left.evaluate() # evaluates left expr
        right = self.right.evaluate() # evaluates right expr
        return op(left, right) 


class UnaryOp(BaseClass):
    oper = { # <-- Uses the operator module to assign operator value to the token specified
        '-': operator.neg,
        '~': operator.not_
    }

    def __init__(self, operation, expr):
        self.operation = operation
        self.expr = expr

    def evaluate(self):
        '''
        Function that returns the evaluated expression computed upon 
        by a unary operator.
        '''
        return self.oper[self.operation](self.expr.evaluate())

class Array(BaseClass):
    def __init__(self,val):
        self.val = val

    def evaluate(self):
        '''
        Function that returns the values inside of an array.
        '''
        return self.val.evaluate()

class ArrayAccess(BaseClass):
    def __init__(self, arr, index):
        self.arr = arr
        self.index = index

    def evaluate (self):
        '''
        Function that returns the value of the element 
        being accessed in an array.
        '''
        return self.arr.evaluate()[self.index.evaluate()]

class ArrayAssign(BaseClass):
    def __init__(self, arr, index, val):
        self.arr = arr
        self.index = index
        self.val = val

    def evaluate(self):
        '''
        Function that assigns a value to an indexed array.
        '''
        self.arr.evaluate()[self.index.evaluate()] = self.val.evaluate()

class For(BaseClass):
    def __init__(self, ident, rangeStart, rangeEnd, colonTok, body):
        self.ident = ident
        self.rangeStart = rangeStart
        self.rangeEnd = rangeEnd
        self.colonTok = colonTok 
        self.body = body

    def evaluate(self):
        '''
        Function that evaluates for statement (@mission) passed.
        '''
        if self.colonTok: # <-- condition if colonTok argument passed is ':+'
            start = self.rangeStart.evaluate()
            end = self.rangeEnd.evaluate() + 1
            adder = 1 # <-- adds 1 per iteration
        else: # <-- condition if colonTok argument passed is ':-'
            start = self.rangeStart.evaluate()
            end = self.rangeEnd.evaluate() - 1
            adder = -1 # <-- adds -1 per iteration

        for i in range(start, end, adder):
            self.ident.assign(i)

            if isinstance(self.body.evaluate(), Break): # <-- breaks the loop if '@kai' (our own break statement) is encountered
                break

class While(BaseClass):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def evaluate(self):
        '''
        Function that evaluates while statement (@izanami) passed.
        '''
        while self.cond.evaluate():
            if isinstance(self.body.evaluate(), Break): # <-- breaks the loop if '@kai' (our own break statement) is encountered
                break

class If(BaseClass):
    def __init__(self, cond, ifBod, elseBod=None):
        self.cond = cond
        self.ifBod = ifBod
        self.elseBod = elseBod

    def evaluate(self):
        '''
        Function that evaluates the If Statement (@ifsu) passed.
        '''
        if self.cond.evaluate(): # <-- returns evaluation of the if statement's body if condition is true
            return self.ifBod.evaluate()
        elif self.elseBod is not None: # <-- returns evaluation of the else statement's body if condition is false
            return self.elseBod.evaluate()


class SetUserInput(BaseClass):
    '''
    Class that returns python's built-in function 'input ()'
    and assign it to '@summon'; for strings.
    '''
    def evaluate(self):
        return raw_input()

class SetUserInputInt(BaseClass):
    '''
    Class that returns python's built-in function 'input ()'
    and assign it to '@summon_Int'; for integers.
    '''
    def evaluate(self):
        return input()