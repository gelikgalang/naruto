# Galang, Angelika
# Gonzales Justin
# CS 150: MP - Naruto Language

''' 
This file defines a  Symbol Table class for the Naruto language.
A Symbol Table contains information of an identifier such as its 
name, scope, and type that are necessary to properly interpret
the language's Abstract Syntax Tree. It is also responsible 
in determining whether an identifier is declared or not inside
the main function.
'''

class SymbolTable:
    symbols = 'symbols'

    table = {
        symbols: {},
    }

    def SymTable(self):
        '''
        Function that simply returns the Symbol Table.
        '''
        return self.table

    def get_sym(self, sym):
        '''
        Function that returns a symbol if found in the table; raises
        an exception otherwise.
        '''
        if sym in self.table[self.symbols]:
            return self.table[self.symbols][sym]

        raise Exception("Undefined variable '%s'" % sym)

    def set_sym(self, sym, val):
        '''
        Function that inserts a new symbol to the symbol table.
        '''
        self.table[self.symbols][sym] = val