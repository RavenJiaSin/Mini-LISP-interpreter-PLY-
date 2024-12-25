# Mini-LISP-interpreter-PLY-

Author: RavenJS
<NCU CISE 3-B 111502559 王嘉信>

In this project, I use Python PLY to make a Mini-LISP interpreter.
To run this project, you may have to create an Python 3.9.12 environment,with PLY.
```
pip install ply=3.11
```
This project include 3 file:
- final_lex.py (lex)
- final_yacc.py (yacc)
- readLSP.py

There's also a folder with test .lsp files: public_test_data.
You can run readLSP.py to read and run Mini-LISP program examples,
or you may put your own .lsp files in the folder and change the ```INPUT_FOLDER``` variable to the path of your own path.

## lex token:
```python
tokens = [
    'NUMBER',       # int value
    'ID',           # ID for variable and function
    'BOOL_VAL',     # boolean value (#t #f)
    'LPAREN',       # (
    'RPAREN',       # )

    'PLUS',         # +
    'MINUS',        # -
    'MULTIPLY',     # *
    'DIVIDE',       # /
    'MODULUS',      # mod
    'GREATER',      # >
    'SMALLER',      # <
    'EQUAL',        # =

    'DEFINE',       # define
    'PRINT_NUM',    # print-number
    'PRINT_BOOL',   # print-bool
     
    'AND',          # and
    'OR',           # or
    'NOT',          # not

    'IF',           # if

    'FUN'           # fun

]
```

## yacc production rules:
```
PROGRAM     : STMT_LIST
STMT_LIST   : STMT
            | STMT STMT_LIST
STMT        : EXP
            | DEF_STMT
            | PRINT_STMT
PRINT_STMT  : LPAREN PRINT_NUM EXP RPAREN
            | LPAREN PRINT_BOOL EXP RPAREN
EXP         : BOOL_VAL
            | NUMBER
            | ID
            | NUM_OP
            | LOGICAL_OP
            | FUN_EXP
            | FUN_CALL
            | IF_EXP
NUM_OP      : LPAREN PLUS EXP EXP_LIST RPAREN
            | LPAREN MINUS EXP EXP RPAREN
            | LPAREN MULTIPLY EXP EXP_LIST RPAREN
            | LPAREN DIVIDE EXP EXP RPAREN
            | LPAREN MODULUS EXP EXP RPAREN
            | LPAREN GREATER EXP EXP RPAREN
            | LPAREN SMALLER EXP EXP RPAREN
            | LPAREN EQUAL EXP EXP_LIST RPAREN
EXP_LIST    : EXP
            | EXP EXP_LIST
LOGICAL_OP  : LPAREN AND EXP EXP_LIST RPAREN
            | LPAREN OR EXP EXP_LIST RPAREN
            | LPAREN NOT EXP RPAREN
DEF_STMT    : LPAREN DEFINE ID EXP RPAREN
FUN_EXP     : LPAREN FUN LPAREN FUN_IDS RPAREN FUN_BODY RPAREN
FUN_IDS     : 
            | ID FUN_IDS
FUN_BODY    : EXP
            | DEF_STMT EXP
FUN_CALL    : LPAREN FUN_EXP PARAM_LIST RPAREN
            | LPAREN ID PARAM_LIST RPAREN
PARAM_LIST  : 
            | PARAM PARAM_LIST
PARAM       : EXP
IF_EXP      : LPAREN IF EXP EXP EXP RPAREN
```

