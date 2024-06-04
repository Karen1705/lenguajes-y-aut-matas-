import ply.yacc as yacc
import ply.lex as lex

# Lexer
# Lista de nombres de tokens
tokens = [
    "NUMBER", "PLUS", "MINUS", "TIMES", "DIVIDE",
    "LPAREN", "RPAREN", "EQUALS", "FINISH",
    "IDENTIFIER", "CHARACTER"
]

# Palabras clave
keywords = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN'
}

# Añadir los nombres de las palabras clave a la lista de tokens
tokens += list(keywords.values())

# Reglas de expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_FINISH = r';'

# Regla de expresión regular para reconocer números enteros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla de expresión regular para reconocer identificadores y palabras clave
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')  # Revisa si es una palabra clave
    return t

# Regla de expresión regular para reconocer caracteres individuales
def t_CHARACTER(t):
    r'\'[a-zA-Z]\''
    t.value = t.value[1]  # Obtiene el carácter dentro de las comillas simples
    return t

# Un string que contiene caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t\n'

# Regla de manejo de errores
def t_error(t):
    print(f"Carácter no válido: '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Parser
# Reglas de precedencia
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Reglas de producción
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# Manejo de errores de sintaxis
def p_error(p):
    if p:
        print("Error de sintaxis en la entrada:", p.value)
    else:
        print("Error de sintaxis al final de la entrada")

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Ejemplo de uso
data = "8 + 2 * (10 / 2)"
result = parser.parse(data)
print(result)


