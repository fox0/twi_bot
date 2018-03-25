pattern
	: /* empty */
	| pattern command

command
	: function
	| while
	| if
	| assignment
	| expression
	'\n'

function
	: 'function' IDENTIFIER '(' args ')' block

block
	: '{' pattern '}'

args
	: /* empty */
	| IDENTIFIER endargs

endargs
	: /* empty */
	| ',' IDENTIFIER endargs

while
	: 'while' expression block

if
	: 'if' expression block endif

endif
	: /* empty */
	| elseif
	| else

elseif
	: 'elseif' expression block endif

else
	: 'else' block

assignment
	: IDENTIFIER assignment_operator expression

expression
	: IDENTIFIER
	| constant
	| '(' expression ')'
	| expression expression_operator expression
	| call_function

assignment_operator
	: '='
	| '+='
	| '-='
	| '*='
	| '/='
	| '//='
	| '%='

expression_operator
	: '+'
	| '-'
	| '*'
	| '/'
	| '//'
	| '%'
	| '=='
	| '!='
	| '<'
	| '>'
	| '<='
	| '>='
	| 'or'
	| 'and'

call_function
	: IDENTIFIER '(' args_func ')'

args_func
	: /* empty */
	| expression endargs_func

endargs_func
	: /* empty */
	| ',' expression endargs_func

constant
	: INT_CONSTANT
	| FLOAT_CONSTANT

%token IDENTIFIER INT_CONSTANT FLOAT_CONSTANT
