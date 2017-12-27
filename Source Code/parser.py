# Galang, Angelika
# Gonzales Justin
# CS 150: MP - Naruto Language

''' 
This file contains all the grammar rules for the Naruto
languages and is responsible for its parsing.
'''

import sys
import ply.yacc as yacc
from lexer import *
#from compiler import ast # <-- built-in module
import ast as ast # <-- to be defined by us


#-- Declaration of operator precedence --#
precedence = (
# associativity , operator 
	('left', 	'not_tok'), # level 0
	('left', 	'plus_tok','minus_tok'), # level 1
	('left', 	'mult_tok','div_tok','mod_tok'), # level 2
	('left',	'pow_tok'), # level 3
	('right', 'UMINUS'), # level 4
)	

#-- Grammar Rules --#

def p_main(p):
	'''
	main : progStart_tok lBrace_tok statements rBrace_tok progEnd_tok
	'''
	p[0] = p[3]

def p_statements(p):
	'''
	statements 	: statement
				| statements statement
	'''
	if len(p) == 2:  # <-- statements : statement; adds statement into a Node in the AST
		p[0] = ast.Node([p[1]])
	else: # <-- statements : statements statement; appends 'statement' to the children of node 'statements'
		p[1].children.append(p[2])
		p[0] = p[1]

def p_statement_general(p):
	'''
	statement 	: identifier
				| expr
				| ifStatement
	'''
	p[0] = p[1]

def p_statement_breal(p):
	'''
	statement : break_tok
	'''
	p[0] = ast.Break()
def p_statement_print(p):
	'''
	statement : print_tok arguments
	'''
	p[0] = ast.Print(p[2])

def p_statement_assign_arr(p):
	'''
	statement : identifier arrOpen_tok expr arrClose_tok equal_tok expr
	'''
	p[0] = ast.ArrayAssign(p[1],p[3],p[6])

def p_statement_for(p):
	'''
	statement 	: for_tok identifier in_tok expr colonPlus_tok expr lBrace_tok statements rBrace_tok end_tok for_tok
				| for_tok identifier in_tok expr colonMinus_tok expr lBrace_tok statements rBrace_tok end_tok for_tok
	'''
	p[0] = ast.For(p[2],p[4],p[6],p[5] == ':+',p[8])

def p_statement_while(p):
	'''
	statement : while_tok lParen_tok expr rParen_tok lBrace_tok statements rBrace_tok end_tok while_tok
	'''
	p[0] = ast.While(p[3],p[6])

def p_identifier(p):
	'''
	identifier : identifier_tok
	'''
	p[0] = ast.Identifier(p[1])

def p_expr(p):
	'''
	expr 	: identifier
			| primitive
			| string_tok
	'''
	p[0] = p[1]

def p_expr_BinOp(p):
	'''
	expr 	: expr plus_tok expr
			| expr minus_tok expr
			| expr mult_tok expr
			| expr div_tok expr
			| expr truediv_tok expr
			| expr mod_tok expr
			| expr pow_tok expr
	'''
	p[0] = ast.BinOp(p[1],p[3],p[2])

def p_expr_UnaryOp(p):
	'''
	expr 	: minus_tok expr %prec UMINUS
			| not_tok expr
	'''
	p[0] = ast.UnaryOp(p[1],p[2])

def p_expr_paren(p):
	'''
	expr : lParen_tok expr rParen_tok
	'''
	p[0] = p[2] if isinstance(p[2], ast.BaseClass) else ast.ReturnValue(p[2]) # <-- If: expr not primitive; Else: expr is primitive

def p_expr_arr(p):
	'''
	expr : arrOpen_tok arguments arrClose_tok
	'''
	p[0] = ast.Array(p[2])

def p_expr_arr_access(p):
	'''
	expr : identifier arrOpen_tok expr arrClose_tok
	'''
	p[0] = ast.ArrayAccess(p[1],p[3])

def p_expr_assign(p):
	'''
	expr : identifier equal_tok assignable
	'''
	p[0] = ast.Assignment(p[1],p[3])

def p_primitive(p):
	'''
	primitive 	: int_tok
				| float_tok
				| string_tok
				| boolean
	'''
	if isinstance(p[1], ast.BaseClass): # <-- primitive: boolean
		p[0] = p[1]
	else: # <-- primitive: int | string | float
		p[0] = ast.ReturnValue(p[1])

def p_boolean(p):
	'''
	boolean 	: expr eqeq_tok expr
				| expr ne_tok expr
				| expr gThan_tok expr
				| expr ge_tok expr
				| expr lThan_tok expr
				| expr le_tok expr
				| true_tok
				| false_tok
	'''
	if len(p )== 4:
		p[0] = ast.BinOp(p[1],p[3],p[2])
	else: # <-- boolean: true_tok | false_tok
		p[0] = ast.ReturnValue(p[1])
def p_assignable(p):
	'''
	assignable 	: primitive
				| expr
	'''
	p[0] = p[1]

def p_arguments(p):
	'''
	arguments 	: arguments comma_tok expr
				| expr
				|
	'''
	if len(p) == 1: # <-- arguments: <blank>; adds an empty node to the AST
		p[0] = ast.Node()
	elif len(p) == 2: # <-- arguments: expr; adds 'expr' to a node in the AST
		p[0] = ast.Node([p[1]])
	else:
		p[1].children.append(p[3]) # <-- arguments: arguments comma expr; appends 'expr' to the children of the node of the 'arguments'
		p[0] = p[1]

def p_ifStatement(p):
	'''
	ifStatement : if_tok lParen_tok expr rParen_tok lBrace_tok statements rBrace_tok
	'''
	p[0] = ast.If(p[3],p[6])

def p_ifStatement_w_else(p):
	'''
	ifStatement : if_tok lParen_tok expr rParen_tok lBrace_tok statements rBrace_tok else_tok lBrace_tok statements rBrace_tok
	'''
	p[0] = ast.If(p[3],p[6],p[10])

def p_ifStatement_w_elif(p):
	'''
	ifStatement : if_tok lParen_tok expr rParen_tok lBrace_tok statements rBrace_tok else_tok ifStatement
	'''
	p[0] = ast.If(p[3],p[6],p[9])

def p_user_input_str(p):
	'''
	expr : read_tok lParen_tok rParen_tok
	'''
	p[0] = ast.SetUserInput()

def p_user_input_int(p):
	'''
	expr : readInt_tok lParen_tok rParen_tok
	'''
	p[0] = ast.SetUserInputInt()

def p_error(p): # exception handler
	if p: # <-- Condition if one (or more) of the grammar rules is not followed
		print "BAD SYNTAX: Error in line ",p.lineno # prints the line number where the error occured
		print "Syntax error at token:",p.type # prints the token that made the error
	else: # <-- Condition if end of the file is met without "@kage" as its ender
		print("Syntax error at EOF! ``@kage'' should be at the last line to end the program properly.")

def startParse():
	data = []
	if len(sys.argv) != 2:
	    print("Error! No source file specified.")
	    exit()

	sourceFile = sys.argv[1]
	if ".naruto" not in sourceFile:
		print "Invalid file type! Your file should have a .naruto extension"
		sys.exit()

	with open(sourceFile, 'r') as content_file:
	    data = content_file.read()

	parser = yacc.yacc(debug=False)
	result = parser.parse(data,tracking=False)

	for node in result.children:
		node.evaluate()


if __name__ == "__main__":
	startParse()
