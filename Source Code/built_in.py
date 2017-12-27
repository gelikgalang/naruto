# Galang, Angelika
# Gonzales Justin
# CS 150: MP - Naruto Language

''' 
This file assigns the built-in functions to the specified token.
'''

import interpreter
import ast as ast
import lexer
import parser
import sys

def str_format(string, *args):
    return string % tuple(args)

def dec_fxns(s):
	f = ast.BuiltInFxn

	#-- Typecasting functions --#
	s.set_func('integer', f(int))
	s.set_func('float', f(float))
	s.set_func('bool', f(bool))
	s.set_func('string', f(str))

	s.set_func('len', f(len))
	s.set_func('format', f(str_format))

	#-- User-input function --#
	s.set_func('summon', f(input))