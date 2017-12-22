import ply.lex as lex
import sys, os
import ply.yacc as yacc
from compiler import ast

#-- List of Tokens --#
tokens=(
	'progStart_tok',
	'progEnd_tok',
	'print_tok',
	'read_tok',
	'true_tok',
	'false_tok',
	'while_tok',
	'if_tok',
	'else_tok',
	'end1_tok',
	'for_tok',
	'end2_tok',
	'comma_tok',
	'dataType_tok',
	'varName_tok',
	'num_tok',
	'lBrace_tok',
	'rBrace_tok',
	'lParen_tok',
	'rParen_tok',
	'lThan_tok',
	'gThan_tok',
	'equal_tok',
	'relationalOp_tok',
	'not_tok',
	'plus_tok',
	'minus_tok',
	'mult_tok',
	'div_tok',
	'mod_tok',
	'comment',
	'float_tok',
	'anything_tok'
	)

#-- Tokens for program header/footer --#
t_progStart_tok = r"(@genin)"
t_progEnd_tok = r"(@kage)"

#-- Tokens for input/output --#
t_print_tok = r"(@byakugan)"
t_read_tok = r"(@summon)"

#-- Tokens for loop/if-else statements --#
t_while_tok=r"(@izanami)"
t_if_tok=r"(@ifsu)"
t_else_tok=r"(@elsu)"
t_end1_tok=r"(@seal)"
t_for_tok=r"(@mission)"
t_end2_tok=r"(@end)"

#-- RegEx for Tokens -- #
t_dataType_tok=r"@number|@decimal|@boolean|@string"
integer=r'[0-9]+'
t_num_tok=integer
t_float_tok=r'('+integer+'\.'+integer+')'
t_varName_tok = r"([A-Za-z][A-Za-z0-9]*)"

#-- Tokens for symbols --#
t_true_tok = r"(@naruto)"
t_false_tok = r"(@boruto)"
t_comma_tok = r','
t_lBrace_tok = r'\['
t_rBrace_tok = r']'
t_lParen_tok = r'\('
t_rParen_tok = r'\)'
t_lThan_tok = r'<'
t_gThan_tok = r'>'
t_equal_tok=r'='
t_relationalOp_tok=r"((==)|(>=)|(<=)|(~=))"
t_not_tok=r'~'
t_plus_tok = r'\+'
t_minus_tok = r'-'
t_mult_tok = r'\*'
t_div_tok = r'\/'
t_mod_tok = r'\%'



#-- Token to ignore: whitespace --#
t_ignore  = ' \t'


def t_comment(t):
    r'\![^\!]*\!'
    return t
    # No return value. Token discarded
def t_anything_tok(t):
    r'\"[^\"]*\"'
    return t
    # No return value. Token discarded

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


#-- YACC --#
precedence = (
	('nonassoc', 'lParen_tok','rParen_tok','varName_tok','dataType_tok','comment',
		'if_tok','print_tok','read_tok','num_tok','float_tok','while_tok',
		'for_tok','rBrace_tok','lBrace_tok','end1_tok','end2_tok'),
	('left', 'plus_tok','minus_tok'),
	('left', 'mult_tok','div_tok','mod_tok'),
)



def p_start(p):
	'''start : comments main'''
	p[0] = p[1] + p[2]

def p_main(p):
	'''main : progStart_tok lBrace_tok statements rBrace_tok progEnd_tok'''
	p[0] = [p[3]]

def p_statements(p):
	'''statements : expr statements
		|	varDec statements
		|	varAssign statements
		|	comments statements
		|	loops statements
		|	ifelse statements
		|	IO statements
		|	empty'''
	if len(p) == 3:
		
	else:
		p[0] = p[1]

def p_IO(p):
	'''IO :	print_tok lParen_tok IOBody rParen_tok
		|	read_tok varName_tok varDecArr
		'''
	if len(p) == 4:
		p[0] = p[3]

def p_IOBody(p):
	'''IOBody : varName_tok varDecArr IOEnd 
		|	anything_tok IOEnd'''
	if len(p) == 3:
		p[0] = p[3]

def p_IOEnd(p):
	'''IOEnd : comma_tok IOBody 
		| empty'''
	if len(p) == 2:
		p[0] = p[1]
def p_varDec(p):
	'''varDec : dataType_tok varName_tok varDecArr varDecBody'''

def p_varDecBody(p):
	'''varDecBody : comma_tok varName_tok
		| empty '''

def p_varDecArr(p):
	'''varDecArr : varArr 
		| empty'''

def p_varArr(p):			
	'''varArr : lThan_tok num_tok gThan_tok 
		| lThan_tok varName_tok gThan_tok '''

def p_varAssign(p):
	'''varAssign : varName_tok varDecArr equal_tok expr'''

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
		|	varName_tok varDecArr
		|	id
	'''

def p_expr2(p):
	'''expr2 : expr relationalOp_tok expr
		|	boolAssign'''

def p_condition(p):
	'''condition : expr2 
		| not_tok condition 
		| num_tok'''

def p_loops(p):
	'''loops : while 
		| for'''

def p_while(p):
	'''while : while_tok condition statements end1_tok while_tok'''

def p_for(p):
	'''for : for_tok varAssign comma_tok num_tok comma_tok num_tok statements end2_tok for_tok'''

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
	'''id : num_tok 
		| float_tok '''
	#p[0] = p[1]

def p_empty(p):
	'empty :'
	pass	

def p_error(p):
	if p:
		print("Error in line ",p.lineno)
		print("Syntax error at token",p.type)
	else:
		print("Syntax error at EOF! ``@kage'' should be at the last line to end the program properly.")

def startParse():
	data = []
	sourceFile = sys.argv[1]
	if ".naruto" not in sourceFile:
		print "Invalid file type!"
		sys.exit()

	with open(sourceFile, 'r') as content_file:
	    data = content_file.read()

	lexer = lex.lex()
	lexer.input(data)

	parser = yacc.yacc()
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
