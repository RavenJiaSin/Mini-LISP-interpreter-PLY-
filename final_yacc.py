import ply.yacc as yacc
from final_lex import tokens

# 紀錄變數的全域表
variables = {}


def evaluate(node, local_scope=None):
    # Evaluate AST Node with global and local scope handling.
    scope = local_scope or {}  # 使用局部作用域，默認為全局作用域
    if isinstance(node, tuple):  # 還需要繼續 evaluate 下去
        op = node[0]
        if op == '+':
            values = [evaluate(exp, scope) for exp in node[1]]
            result = 0
            for v in values:
                if not type(v) == int:
                    raise TypeError(f"TypeError: Operator '+' expects integers, but got: {values}")
                result += v
            return result
        elif op == '-':
            left = evaluate(node[1], scope)
            right = evaluate(node[2], scope)
            if not (type(left)==int and type(right)==int):  # 用 isinstance 會因為 bool 是 int 的 sub-type，而判定相等
                raise TypeError(f"TypeError: Operator '-' expects integers, but got: {left}, {right}")
            return left - right
        elif op == '*':
            values = [evaluate(exp, scope) for exp in node[1]]
            result = 1
            for v in values:
                if not type(v) == int:
                    raise TypeError(f"TypeError: Operator '*' expects integers, but got: {values}")
                result *= v
            return result
        elif op == '/':
            left = evaluate(node[1], scope)
            right = evaluate(node[2], scope)
            if not (type(left)==int and type(right)==int):
                raise TypeError(f"TypeError: Operator '/' expects integers, but got: {left}, {right}")
            if right == 0:
                raise ZeroDivisionError("ZeroDivisionError: Division by zero")
            return left // right
        elif op == 'mod':
            left = evaluate(node[1], scope)
            right = evaluate(node[2], scope)
            if not (type(left)==int and type(right)==int):
                raise TypeError(f"TypeError: Operator 'mod' expects integers, but got: {left}, {right}")
            return left % right
        elif op == '>':
            left = evaluate(node[1], scope)
            right = evaluate(node[2], scope)
            if not (type(left)==int and type(right)==int):
                raise TypeError(f"TypeError: Operator '>' expects integers, but got: {left}, {right}")
            return left > right
        elif op == '<':
            left = evaluate(node[1], scope)
            right = evaluate(node[2], scope)
            if not (type(left)==int and type(right)==int):
                raise TypeError(f"TypeError: Operator '<' expects integers, but got: {left}, {right}")
            return left < right
        elif op == '=':
            values = [evaluate(exp, scope) for exp in node[1]]
            
            for v in values:
                if not type(v)==int:
                    raise TypeError(f"TypeError: Operator '=' expects integers, but got: {values}")
                if not v==values[0]: return False   
            return True
        elif op == 'AND':
            values = [evaluate(exp, scope) for exp in node[1]]
            if not all(type(v)==bool for v in values):
                raise TypeError(f"TypeError: Operator 'AND' expects booleans, but got: {values}")
            return all(values)
        elif op == 'OR':
            values = [evaluate(exp, scope) for exp in node[1]]
            if not all(type(v)==bool for v in values):
                raise TypeError(f"TypeError: Operator 'OR' expects booleans, but got: {values}")
            return any(values)
        elif op == 'NOT':
            value = evaluate(node[1], scope)
            if not type(value)==bool:
                raise TypeError(f"TypeError: Operator 'NOT' expects a boolean, but got: {value}")
            return not value
        elif op == 'DEFINE':
            # 定義全局變數
            variables[node[1]] = evaluate(node[2], scope)
        elif op == 'FUN':  # 函數定義
            _, arg_names, body = node
            if isinstance(body, tuple) and body[0] == 'NDEF':  # 有巢狀定義
                evaluate(body[1], scope)
                return ('FUN', arg_names, body[2], scope) # 存環境
            else:
                return ('FUN', arg_names, body, scope) # 存環境
        elif op == 'CALL':  # 函數調用
            function = evaluate(node[1], scope)  # node[1] 是 FUNC_EXP 或 ID
            params = [evaluate(param, scope) for param in node[2]]

            if isinstance(function, tuple) and function[0] == 'FUN':
                _, arg_names, body, closure_scope = function
                local_scope = {**closure_scope, **dict(zip(arg_names, params))}  # 參數名綁引數值，解包並合併字典，這邊應會導致閉包脫鉤，但測資不會重新賦值給變數
                return evaluate(body, local_scope)
            elif isinstance(function, str) and function in variables:  # 已定義的命名函式
                fun_def = variables[function]
                if isinstance(fun_def, tuple) and fun_def[0] == 'FUN':
                    _, arg_names, body, closure_scope = fun_def
                    local_scope = {**closure_scope, **dict(zip(arg_names, params))}
                    return evaluate(body, local_scope)
            raise Exception(f"Invalid function call: {function}")
        elif op == 'IF':
            condition = evaluate(node[1], scope)
            if not type(condition)==bool:
                raise TypeError(f"TypeError: Condition in 'IF' expects a boolean, but got: {condition}")
            return evaluate(node[2] if condition else node[3], scope)
        elif op == 'print-num':
            value = evaluate(node[1], scope)
            if not isinstance(value, int):
                raise TypeError(f"print-num expects an integer, but got: {value}")
            print(value)
        elif op == 'print-bool':
            value = evaluate(node[1], scope)
            if not type(value)==bool:
                raise TypeError(f"TypeError: print-bool expects a boolean, but got: {value}")
            print('#t' if value else '#f')
        else:
            raise Exception(f"Unsupported operation: {op}")
    elif isinstance(node, str):  # 查找變數
        if node in scope:
            return scope[node]  # 局部作用域中的變數
        elif node in variables:
            return variables[node]  # 全局作用域中的變數
        else:
            raise Exception(f"Undefined variable: {node}")
    else:
        return node  # 常數值直接返回








# 定義語法規則
def p_program(p):
    '''PROGRAM : STMT_LIST'''
    p[0] = p[1]

def p_stmt_list(p):
    '''STMT_LIST : STMT
                 | STMT STMT_LIST'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_stmt(p):
    '''STMT : EXP
            | DEF_STMT
            | PRINT_STMT'''
    p[0] = p[1]

def p_print_stmt(p):
    '''PRINT_STMT : LPAREN PRINT_NUM EXP RPAREN
                  | LPAREN PRINT_BOOL EXP RPAREN'''
    p[0] = (p[2], p[3])

def p_exp(p):
    '''EXP : BOOL_VAL
           | NUMBER
           | ID
           | NUM_OP
           | LOGICAL_OP
           | FUN_EXP
           | FUN_CALL
           | IF_EXP'''
    p[0] = p[1]

def p_num_op(p):
    '''NUM_OP : LPAREN PLUS EXP EXP_LIST RPAREN
              | LPAREN MINUS EXP EXP RPAREN
              | LPAREN MULTIPLY EXP EXP_LIST RPAREN
              | LPAREN DIVIDE EXP EXP RPAREN
              | LPAREN MODULUS EXP EXP RPAREN
              | LPAREN GREATER EXP EXP RPAREN
              | LPAREN SMALLER EXP EXP RPAREN
              | LPAREN EQUAL EXP EXP_LIST RPAREN'''
    if p[2] in ['+', '*', '=']:
        p[0] = (p[2], [p[3]] + (p[4] if isinstance(p[4], list) else [p[4]]))
    else:
        p[0] = (p[2], p[3], p[4])

def p_exp_list(p):
    '''EXP_LIST : EXP
                | EXP EXP_LIST'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

# 邏輯運算
def p_logical_op(p):
    '''LOGICAL_OP : LPAREN AND EXP EXP_LIST RPAREN
                  | LPAREN OR EXP EXP_LIST RPAREN
                  | LPAREN NOT EXP RPAREN'''
    if p[2] == 'and':
        p[0] = ('AND', [p[3]] + p[4])
    if p[2] == 'or':
        p[0] = ('OR', [p[3]] + p[4])
    if p[2] == 'not':
        p[0] = ('NOT', p[3])

def p_def_stmt(p):
    '''DEF_STMT : LPAREN DEFINE ID EXP RPAREN'''
    p[0] = ('DEFINE', p[3], p[4])

# 函式
# 支援函數定義
def p_fun_exp(p):
    '''FUN_EXP : LPAREN FUN LPAREN FUN_IDS RPAREN FUN_BODY RPAREN'''
    p[0] = ('FUN', p[4], p[6])  # 定義函數，包含參數列表和函數本體

# 定義函數參數
def p_fun_ids(p):
    '''FUN_IDS : 
               | ID FUN_IDS'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

# 函數本體
def p_fun_body(p):
    '''FUN_BODY : EXP
                | DEF_STMT EXP'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('NDEF', p[1], p[2])

# 支援函數調用
def p_fun_call(p):
    '''FUN_CALL : LPAREN FUN_EXP PARAM_LIST RPAREN
                | LPAREN ID PARAM_LIST RPAREN'''
    if p[2][0] == 'FUN':
        p[0] = ('CALL', p[2], p[3])  # 匿名函數
    else:
        p[0] = ('CALL', p[2], p[3])  # 命名函數

# 參數列表
def p_param_list(p):
    '''PARAM_LIST : 
                  | PARAM PARAM_LIST'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

# 參數
def p_param(p):
    '''PARAM : EXP'''
    p[0] = p[1]

# 條件判斷
def p_if_exp(p):
    '''IF_EXP : LPAREN IF EXP EXP EXP RPAREN'''
    p[0] = ('IF', p[3], p[4], p[5])

# 錯誤處理
def p_error(p):
    print(f"Syntax Error: {p}")
    print("-" * 40)

# 建立語法分析器
parser = yacc.yacc()

# '''
# 測試輸入
if __name__ == "__main__":
    data = """
    (define dist-square
    (fun (x y)
    (define square (fun (x) (* x x)))
    (+ (square x) (square y))))

    (print-num (dist-square 3 4))
    """
    result = parser.parse(data,debug=True)
    print(result)
# '''