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



# Build the lexer
lexer = lex.lex()
# Test it out
data = '''
3 + 4 * 10.123123.123123
  + -20 *2 "!@izanami asdasd!"
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

