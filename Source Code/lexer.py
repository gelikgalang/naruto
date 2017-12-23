import ply.lex as lex

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
	'identifier_tok',
	'int_tok',
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
t_identifier_tok = r"([A-Za-z][A-Za-z0-9]*)"

#-- Tokens for symbols --#
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

#-- Fxn definition for comments: e.g. ! Must always start and end with exclamation point !
def t_comment(t):
    r'\![^\!]*\!'
    return t
    # No return value. Token discarded

#-- Returns any string --#
def t_anything_tok(t):
    r'\"[^\"]*\"'
    return t
    # No return value. Token discarded

#-- Fxn for newline --#
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#-- Error handling rule if invalid token --#
def t_error(t):
    print("Illegal character '%s' at line %d" % (t.value[0], t.lineno))
    t.lexer.skip(1)



# Build the lexer
lexer = lex.lex()
# Test it out
data = '''
@genin [
	3 + 4 * 10.123123.123123
	  + -20 *2 !@izanami asdasd!
	  @izanami (x>1)
	  	x = x-1
	  @seal @izanami
	  
	  @byakugan ("hello world")
	  x=8%2/3.5
]@kage
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

