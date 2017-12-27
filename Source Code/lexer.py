# Galang, Angelika
# Gonzales Justin
# CS 150: MP - Naruto Language

''' 
This file declares and contains all the tokens used in
the Naruto Language.
'''

import ply.lex as lex

#-- List of Tokens --#
tokens=(
	'progStart_tok',
	'progEnd_tok',
	
	'print_tok',
	'read_tok',
	'readInt_tok',
	
	'true_tok',
	'false_tok',
	
	'while_tok',
	'if_tok',
	'else_tok',
	'for_tok',
	'in_tok',
	'end_tok',
	'break_tok',

	'int_tok',
	'float_tok',
	'string_tok',

	'identifier_tok',
	'newline_tok',
	'colonPlus_tok',
	'colonMinus_tok',
	'comma_tok',
	'lBrace_tok',
	'rBrace_tok',
	'lParen_tok',
	'rParen_tok',
	'lThan_tok',
	'gThan_tok',
	'equal_tok',
	'eqeq_tok',
	'ge_tok',
	'le_tok',
	'ne_tok',
	'not_tok',
	'plus_tok',
	'minus_tok',
	'mult_tok',
	'div_tok',
	'truediv_tok',
	'mod_tok',
	'pow_tok',
	'arrOpen_tok',
	'arrClose_tok',
	
	)

#-- Tokens for program header/footer --#
t_progStart_tok = r"(@genin)"
t_progEnd_tok = r"(@kage)"

#-- Tokens for input/output --#
t_print_tok = r"(@byakugan)"
t_read_tok = r"(@summon)"
t_readInt_tok = r"(@summon_Int)"

#-- Tokens for loop/if-else statements --#
t_while_tok=r"(@izanami)"
t_if_tok=r"(@ifsu)"
t_else_tok=r"(@elsu)"
t_for_tok=r"(@mission)"
t_in_tok=r"(@in)"
t_end_tok=r"(@end)"
t_break_tok=r"(@kai)"


#-- Tokens for symbols --#
t_identifier_tok = r"([A-Za-z][\$_A-Za-z0-9]*)"
t_colonPlus_tok=r':\+'
t_colonMinus_tok=r':-'
t_comma_tok = r','
t_lBrace_tok = r'\['
t_rBrace_tok = r']'
t_lParen_tok = r'\('
t_rParen_tok = r'\)'
t_lThan_tok = r'<'
t_gThan_tok = r'>'
t_equal_tok=r'='
t_eqeq_tok = r'=='
t_ge_tok = r'>='
t_le_tok = r'<='
t_ne_tok = r'~='
t_not_tok=r'~'
t_plus_tok = r'\+'
t_minus_tok = r'-'
t_mult_tok = r'\*'
t_pow_tok = r'\*\*'
t_div_tok = r'\/'
t_truediv_tok = r'\/\/'
t_mod_tok = r'\%'
t_arrOpen_tok = r'{'
t_arrClose_tok = r'}'


#-- Token to ignore: whitespace and comments--#
t_ignore  = ' \t'
t_ignore_COMMENTS = r'\$\$.+' # <-- Comments always start with double dollar sign e.g. $$ Henlo this is a comment!

#-- Returns true if @naruto token is found --#
def t_true_tok(t):
    '@naruto'
    t.value = True
    return t

#-- Returns false if @boruto token is found --#
def t_false_tok(t):
    '@boruto'
    t.value = False
    return t

#-- Returns the value of a float number --#
def t_float_tok(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t

#-- Returns the value of an integer --#
def t_int_tok(t):
    r'\d+'
    t.value = int(t.value)
    return t

#-- Fxn for any string enclosed with quotation marks except a single `"` --#
def t_string_tok(t):
   r'"(?:\\"|.)*?"'
   t.value = bytes(t.value.lstrip('"').rstrip('"')).encode("utf-8").decode("unicode_escape")
   return t

#-- Fxn for newline --#
def t_newline_tok(t):
    r'\n'
    t.lexer.lineno +=1
    t.lexer.linepos =0
    pass

#-- Error handling rule if invalid token --#
def t_error(t):
    print("Illegal character '%s' at line %d" % (t.value[0], t.lineno))
    t.lexer.skip(1)



# Build the lexer
lexer = lex.lex()
