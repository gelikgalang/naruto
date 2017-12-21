import ply.lex as lex
import sys, os
import ply.yacc as yacc
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
	'plusMinus_tok',
	'mulDivMod_tok',
	'comment',
	'float_tok',
	'anything_tok'
	)
t_progStart_tok = r"(@genin)"
t_progEnd_tok = r"(@kage)"
t_print_tok = r"(@byakugan)"
t_read_tok = r"(@summon)"
t_true_tok = r"(@naruto)"
t_false_tok = r"(@boruto)"
t_while_tok=r"(@izanami)"
t_if_tok=r"(@ifsu)"
t_else_tok=r"(@elsu)"
t_end1_tok=r"(@seal)"
t_for_tok=r"(@mission)"
t_end2_tok=r"(@end)"
t_comma_tok = r','
t_dataType_tok=r"@number|@decimal|@boolean|@string"
integer=r'[0-9]+'
t_num_tok=integer
t_float_tok=r'('+integer+'\.'+integer+')'
t_varName_tok = r"([A-Za-z][A-Za-z0-9]*)"
t_lBrace_tok = r'\['
t_rBrace_tok = r']'
t_lParen_tok = r'\('
t_rParen_tok = r'\)'
t_lThan_tok = r'<'
t_gThan_tok = r'>'
t_equal_tok=r'='
t_relationalOp_tok=r"((==)|(>=)|(<=)|(~=))"
t_not_tok=r'~'
t_mulDivMod_tok=r'(\*|\/|\%)'
t_plusMinus_tok=r'(\+|-)'
t_ignore  = ' \t'


def t_comment(t):
    r'\!.*'
    return t
    # No return value. Token discarded
def t_anything_tok(t):
    r'\".*'
    return t
    # No return value. Token discarded

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)




def p_start(t):
	'''start : comments main'''
def p_main(t):
	'''main : progStart_tok leftBrace_tok statements rightBrace_tok progEnd_tok'''

def p_statements(t):
	'''statements : expr statements
		|	varDec statements
		|	varAssign statements
		|	comments statements
		|	loops statements
		|	ifelse statements
		|	IO statements
		|	empty'''
def p_IO(t):
	'''IO :	print_tok lParen_tok IOBody rParen_tok
		|	read_tok varName_tok varDecArr
		'''
def p_IOBody(t):
	'''IOBody : varName_tok varDecArr IOEnd 
		|	anything_tok IOEnd'''
def p_IOEnd(t):
	'''IOEnd : commma_tok IOBody | empty'''

def p_varDecArr(t):
	'''varDecArr : varArr | empty'''
def p_varArr(t):			
	'''varArr : lThan_tok num_tok gThan_tok varName_tok gThan_tok '''
def p_varAssign(t):
	'''varAssign : varName_tok varDecArr equal_tok expr'''
def p_boolAssign(t):
	'''boolAssign : true_tok | false_tok'''
def p_comments(t):
	'''comments : comment | empty'''
def p_expr(t):
	'''expr : expr plusMinus_tok expr 
		|	term
		|	varName_tok varDecArr
	'''
def p_expr2(t):
	'''expr2 : expr relationalOp_tok expr
		|	boolAssign'''
def p_condition(t):
	'''condition : expr2 | not_tok condition | num_tok'''
def p_loops(t):
	'''loops : while | for'''
def p_while(t):
	'''while : while_tok condition statements end1_tok while_tok'''
def p_for(t):
	'''for : for_tok varAssign comma_tok num_tok comma_tok num_tok statements end2 for_tok'''
def p_ifelse(t):
	'''ifelse : if_tok condition statements end1_tok if_tok elseif'''
def p_elseif(t):
	'''elseif : else_tok if_tok condition statements end1_tok else_tok if_tok else | empty '''
def p_else(t):
	'''else : else_tok statements | elseif | empty'''
def p_term(t):
	'''term: term mulDivMod_tok term | factor'''
def p_factor(t):
	'''id | lParen_tok expr rParen_tok'''
def p_id(t):
	'''id : num_tok | float_tok '''
def p_empty(t):
	'''empty :'''	


def startParse():
	data = []
	source_name = sys.argv[1]
	with open(source_name, 'r') as content_file:
	    data = content_file.read()

	lexer = lexy.lex()
	lexer.input(data)

	parser = yacc.yacc(debug=False)
	parser.parse(data,tracking=True)
	# print "Working"

	if debug == 1:
		toks = []
		tok1 =""
		lexer.input(data)
		while True:
		    tok = lexer.token()
		    if not tok: 
		        break      # No more input
		    toks.append(tok.value)
		    print tok
		    tok1 = tok1+tok.value
		print toks
		print tok1

	return True


if __name__ == "__main__":
	startParse()
