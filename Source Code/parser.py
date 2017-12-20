import ply.lex as lex
import sys, os
import ply.yacc as yacc


tokens=(
	'genin_tok',
	'lBrace_tok',
	'rBrace_tok',
	'kage_tok',
	'byakugan_tok',
	'lParen_tok',
	'rParen_tok',
	'summon_tok',
	'varName_tok',
	'anything_tok',
	'comma_tok',
	'dataType_tok',
	'lThan_tok',
	'gThan_tok',
	'equal_tok',
	'naruto_tok',
	'boruto_tok',
	'comment_tok',
	'plusMinus_tok',
	'mulDivMod_tok',
	'relationalOp_tok',
	'not_tok',
	'num_tok',
	'izanami_tok',
	'seal_tok',
	'mission_tok',
	'end_tok',
	'ifsu_tok',
	'elsu_tok',
	'float_tok',
	)

t_genin_tok = r"(@genin)"
t_lBrace_tok = r'\['
t_rBrace_tok = r']'
t_kage_tok = r"(@kage)"
t_byakugan_tok = r"(@byakugan)"
t_lParen_tok = r'\('
t_rParen_tok = r'\)'
t_summon_tok = r"(@summon)"
t_dataType_tok=r"@number|@decimal|@boolean|@string"
t_comma_tok = r','
t_lThan_tok = r'<'
t_gThan_tok = r'>'
t_equal_tok=r'='
t_naruto_tok = r"(@naruto)"
t_boruto_tok = r"(@boruto)"
t_comment_tok=r'!'
t_mulDivMod_tok=r'(\*|\/|\%)'
t_plusMinus_tok=r'(\+|-)'
t_relationalOp_tok=r"((==)|(>=)|(<=)|(~=))"
t_not_tok=r'~'
t_num_tok=r'[0-9]+'
t_izanami_tok=r"(@izanami)"
t_seal_tok=r"(@seal)"
t_mission_tok=r"(@mission)"
t_ifsu_tok=r"(@ifsu)"
t_elsu_tok=r"(@elsu)"
t_end_tok=r"(@end)"
t_ignore  = ' \t'
t_varName_tok = r"([A-Za-z][A-Za-z0-9]*)"



#t_float_tok=r'('+[1-9]+'\.'+[0-9]+')'                     PAAYOS NETO 
#t_anything = r'('



def t_INITIAL_COMMENTS(t):
	r"\![^\%]*\!"
	t.lexer.lineno += t.value.count('\n')
	return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)




def p_start(t):
	'''start : comment main'''
def p_main(t):
	'''main : genin_tok leftBrace_tok statements rightBrace_tok kage_tok'''

def p_statements(t):
	'''statements : expr statements
		|	varDec statements
		|	varAssign statements
		|	comment statements
		|	loops statements
		|	ifelse statements
		|	IO statements
		|	empty'''
def p_IO(t):
	'''IO :	byakugan_tok lParen_tok IOBody rParen_tok
		|	summon_tok varName_tok varDecArr
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
	'''boolAssign : naruto_tok | boruto_tok'''
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
	'''while : izanami_tok condition statements seal_tok izanami_tok'''
def p_for(t):
	'''for : mission_tok varAssign comma_tok num_tok comma_tok num_tok statements end mission_tok'''
def p_ifelse(t):
	'''ifelse : ifsu_tok condition statements seal_tok ifsu_tok elseif_tok'''
def p_elseif(t):
	'''elseif : elsu_tok ifsu_tok condition statements seal_tok elsu_tok ifsu_tok else_tok | empty '''
def p_else(t):
	'''else : elsu_tok_tok statements | elseif | empty'''
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