import sys
import ply.yacc as yacc
from lexer import *
#from compiler import ast # <-- built-in module
import ast as ast # <-- to be defined by us

#-- YACC --#

#-- Declaration of operator precedence --#
precedence = (
# associativity , operator 
	('left', 	'not_tok'), # level 0
	('left', 	'plus_tok','minus_tok'), # level 1
	('left', 	'mult_tok','div_tok','mod_tok'), # level 2
)	


def p_start(p):
	'''start : comments main'''

def p_main(p):
	'''main : progStart_tok lBrace_tok statements rBrace_tok progEnd_tok'''

def p_statements(p):
	'''statements : expr statements
		|	varDec statements
		|	varAssign statements
		|	comments statements
		|	loops statements
		|	ifelse statements
		|	IO statements
		|	empty'''

def p_IO(p):
	'''IO :	print_tok lParen_tok IOBody rParen_tok
		|	read_tok identifier_tok varDecArr
		'''

def p_IOBody(p):
	'''IOBody : identifier_tok varDecArr IOEnd 
		|	anything_tok IOEnd'''
	

def p_IOEnd(p):
	'''IOEnd : comma_tok IOBody 
		| empty'''
	
def p_varDec(p):
	'''varDec : dataType_tok identifier_tok varDecArr varDecBody'''

def p_varDecBody(p):
	'''varDecBody : comma_tok identifier_tok
		| empty '''

def p_varDecArr(p):
	'''varDecArr : varArr 
		| empty'''

def p_varArr(p):			
	'''varArr : lThan_tok int_tok gThan_tok 
		| lThan_tok identifier_tok gThan_tok '''

def p_varAssign(p):
	'''varAssign : identifier_tok varDecArr equal_tok expr'''

def p_boolAssign(p):
	'''boolAssign : true_tok 
		| false_tok'''

def p_comments(p):
	'''comments : comment 
		| empty'''

def p_expr(p):
	'''expr : expr plus_tok expr
		|	expr minus_tok expr
		|	expr mult_tok expr
		|	expr div_tok expr
		|	expr mod_tok expr   
		|	lParen_tok expr rParen_tok
		|	identifier_tok varDecArr
		|	id
	'''


def p_expr2(p):
	'''expr2 : expr relationalOp_tok expr
		|	boolAssign'''

def p_condition(p):
	'''condition : expr2 
		| not_tok condition 
		| int_tok'''

def p_loops(p):
	'''loops : while 
		| for'''

def p_while(p):
	'''while : while_tok condition statements end1_tok while_tok'''

def p_for(p):
	'''for : for_tok varAssign comma_tok int_tok comma_tok int_tok statements end2_tok for_tok'''

def p_ifelse(p):
	'''ifelse : if_tok condition statements end1_tok if_tok elseif'''

def p_elseif(p):
	'''elseif : else_tok if_tok condition statements end1_tok else_tok if_tok else 
		| empty '''

def p_else(p):
	'''else : else_tok statements 
		| elseif 
		| empty'''

def p_id(p):
	'''id : int_tok 
		| float_tok '''

def p_empty(p):
	'empty :'
	pass	

def p_error(p):
	if p:
		print("BAD SYNTAX: Error in line ",p.lineno)
		print("Syntax error at token",p.type)
	else:
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

	lexer = lex.lex()
	lexer.input(data)

	parser = yacc.yacc(debug=False)
	parser.parse(data,tracking=True)

	# Tokenize
	while True:
		tok = lexer.token()
		if not tok: 
			break      # No more input
		print(tok)

	return True


if __name__ == "__main__":
	startParse()
