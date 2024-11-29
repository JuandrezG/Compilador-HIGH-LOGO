#libraries and dependencies used
import sys
from lark import Lark, tree, Token, Transformer, v_args

if len(sys.argv) != 2:
    print('Error: Debes proporcionar un archivo de entrada para el compilador.')
    sys.exit(1)

# The rules of the "High-LOGO" language are defined
high_logo_grammar = r"""
# A High-LOGO program consists of one or more basic instructions


start: (basic_instruction | function_def)+

basic_instruction: move_instruction
                 | PEN
                 | conditional
                 | single_for
                 | double_for
                 | function_call

function_def: DEF NAME LPAREN param_list? RPAREN block

function_call: NAME LPAREN arg_list? RPAREN

param_list: NAME (COMMA expression)*

arg_list: expression (COMMA expression)*   # Definición de arg_list añadida

expression: INTNUM | NAME

conditional: IF boolean_expression block (ELSE block)?

single_for: SINGLE_FOR VAR IN RANGE LPAREN range_args RPAREN block
double_for: DOUBLE_FOR VAR COMMA VAR IN ZIP LPAREN range_expr COMMA range_expr RPAREN block

range_expr: RANGE LPAREN range_args RPAREN

range_args: INTNUM COMMA INTNUM COMMA INTNUM
           | INTNUM COMMA INTNUM
           | INTNUM

boolean_expression: "(" boolean_term ")"

boolean_term: comparison
            | NOT boolean_term
            | boolean_term AND boolean_term
            | boolean_term OR boolean_term
            | "(" boolean_term ")"

comparison: INTNUM COMPARATOR INTNUM

block: LBRACE basic_instruction* RBRACE

move_instruction: MOVEMENT expression

DEF: "def"
NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
SINGLE_FOR: "for"
DOUBLE_FOR: "for"
VAR: /[i-z]/
IN: "in"
ZIP: "zip"
RANGE: "range"
LPAREN: "("
RPAREN: ")"
COMMA: ","
IF: "if"
ELSE: "else"
LBRACE: "{"
RBRACE: "}"
MOVEMENT: "FD" | "BK" | "LT" | "RT" | "WIDTH"
PEN: "PU" | "PD"
COMPARATOR: "==" | "!=" | "<" | ">" | "<=" | ">="
NOT: "!"
AND: "&&"
OR: "||"
INTNUM: /-?\d+(\.\d+)?([eE][+-]?\d+)?/
COMMENT: /#[^\n]*/
%ignore /[ \t\n\f\r]+/
%ignore COMMENT
"""

# Map High-LOGO commands to Python (turtle) commands
command_map_move = {
    "FD": "forward",    # "FD" in High-LOGO maps to "forward" in Python 
    "BK": "backward",   # "BK" in high-LOGO maps to "backward" in Python 
    "LT": "left",       # "LT" in High-LOGO maps to "left" in Python
    "RT": "right",      # "RT" in High-LOGO maps to "right" in Python
    "WIDTH": "width"    # "WIDTH" in High-LOGO maps to "width" in Python
}

# Dictionary mapping High-LOGO pen commands to the corresponding turtle methods in Python
command_map_pen = {
    "PU": "penup",   # "PU" in High-LOGO translates to "penup" in Python
    "PD": "pendown"  # "PD" in High-LOGO translates to "pendown" in Python
}

# Comparison operator mapping dictionary
comparison_map = {
    "==": "==",    # "==" maps the equality operator in the input language to the equality operator in Python (==)
    "!=": "!=",    # "!=" maps the inequality operator to its Python equivalent (!=)
    "<": "<",      # "<" maps the "less than" operator to its Python equivalent (<)
    ">": ">",      # ">" maps the "greater than" operator to its Python equivalent (>).
    "<=": "<=",    # "<=" maps the "less than or equal to" operator to its Python equivalent (<=)
    ">=": ">=",    # ">=" maps the "greater than or equal to" operator to its Python equivalent (>=)
    "!": "not "    # "!" maps the logical negation operator (!) to the Python equivalent (not ), ensuring a space for integration with logical expressions
}

def translate_boolean_expression(ast, output_file=''):
    """Recursively translate Boolean expressions to Python"""
    if isinstance(ast, Token):
        output_file += comparison_map.get(ast.value, ast.value)
        return output_file

    if ast.data == "boolean_expression":
        return translate_boolean_expression(ast.children[0])

    elif ast.data == "boolean_term":
        if len(ast.children) == 1:
            if isinstance(ast.children[0], Token):
                return ast.children[0].value
            return translate_boolean_expression(ast.children[0])
        
        #NOT handling
        if ast.children[0] == "!":
            for c in ast.children:
                output_file = translate_boolean_expression(c, output_file)
        
        #AND handling
        elif len(ast.children) == 3 and ast.children[1].type == "AND":
            left = translate_boolean_expression(ast.children[0])   # Recursively translate the left-hand side of the AND expression
            right = translate_boolean_expression(ast.children[2])  # Recursively translate the right-hand side of the AND expression
            output_file += f"({left} and {right})"  # Combine the left and right expressions using Python's 'and' operator
            return output_file
        
        #OR handling
        elif len(ast.children) == 3 and ast.children[1].type == "OR":
            left = translate_boolean_expression(ast.children[0])
            right = translate_boolean_expression(ast.children[2])
            output_file += f"({left} or {right})"
            return output_file

    elif ast.data == "comparison":
        left, op, right = ast.children
        output_file += f"{left.value} {comparison_map[op.value]} {right.value}"
        return output_file

    return output_file

def translate_range_args(arguments, output_file=""):
    """Translate range arguments to Python"""
    if isinstance(arguments, Token):
        return arguments.value

    if arguments.data == "range_args":
        for c in arguments.children:
            output_file += translate_range_args(c, output_file)
        return output_file

# Translate the AST into Python code
def generate_python_code(ast, output_file, indent_level=0):
    indent = "    " * indent_level

    if ast.data == "start":
        output_file.write("import turtle\n")
        output_file.write("t = turtle.Turtle()\n\n")

        # Process function definitions first
        for child in ast.children:
            if isinstance(child, tree.Tree) and child.data == "function_def":
                generate_python_code(child, output_file)

        # Then process the rest of the instructions
        for child in ast.children:
            if not (isinstance(child, tree.Tree) and child.data == "function_def"):
                generate_python_code(child, output_file)

        output_file.write("\nturtle.mainloop()\n")

    elif ast.data == "function_def":
        function_name = ast.children[1].value
        parameters = []
        if len(ast.children) > 4:
            param_list = ast.children[3]
            if param_list.data == "param_list":
                parameters = [param.value for param in param_list.children if param.type == "NAME"]

        output_file.write(f"{indent}def {function_name}({', '.join(parameters)}):\n")

        block_node = ast.children[-1]
        for instruction in block_node.children:
            if not isinstance(instruction, Token):
                generate_python_code(instruction, output_file, indent_level + 1)
        output_file.write("\n")

    elif ast.data == "function_call":
        func_name = ast.children[0].value
        arguments = []
        if len(ast.children) > 2:
            arg_list = ast.children[2].children
            for arg in arg_list:
                if not isinstance(arg, Token):
                    arguments.append(arg.children[0].value)
        output_file.write(f"{indent}{func_name}({','.join(arguments)})\n")

    elif ast.data == "basic_instruction":
        if isinstance(ast.children[0], Token):
            output_file.write(f"{indent}t.{command_map_pen[ast.children[0].value]}()\n")
        else:
            for c in ast.children:
                generate_python_code(c, output_file, indent_level)

    elif ast.data == "conditional":
        condition = translate_boolean_expression(ast.children[1])
        output_file.write(f"{indent}if {condition}:\n")
        generate_python_code(ast.children[2], output_file, indent_level + 1)
        if len(ast.children) > 3:
            output_file.write(f"{indent}else:\n")
            generate_python_code(ast.children[4], output_file, indent_level + 1)

    elif ast.data == "single_for":
        loop_var = ast.children[1].value
        range_args = translate_range_args(ast.children[5])
        output_file.write(f"{indent}for {loop_var} in range({range_args}):\n")
        generate_python_code(ast.children[7], output_file, indent_level + 1)

    elif ast.data == "double_for":
        var1 = ast.children[1].value
        var2 = ast.children[3].value
        range_args1 = translate_range_args(ast.children[7].children[2])
        range_args2 = translate_range_args(ast.children[9].children[2])
        output_file.write(f"{indent}for {var1},{var2} in zip(range({range_args1}), range({range_args2})):\n")
        generate_python_code(ast.children[11], output_file, indent_level + 1)

    elif ast.data == "move_instruction":
        left, right = ast.children
        if isinstance(right, Token):
            value = right.value
        else:
            value = right.children[0].value
        output_file.write(f"{indent}t.{command_map_move[left.value]}({value})\n")

    else:
        print(f"No implementation for the node: {ast}")

# Check if the input file has been provided as an argument
input_file = sys.argv[1]
output_file = f'{sys.argv[1]}.py'  # The output file will have the .py extension

# Create the parser using the defined grammar
parser = Lark(high_logo_grammar)

# Open the input file to read the High-LOGO code
with open(input_file) as inputFile:
    # Open the output file
    with open(output_file, 'w') as output:
        # Parse the High-LOGO code and generate the abstract syntax tree (AST)
        ast = parser.parse(inputFile.read())
        print(ast.pretty())  # Print the abstract syntax tree (AST)
        tree.pydot__tree_to_png(ast, "tree.png")  # Generate an image of the AST
        tree.pydot__tree_to_dot(ast, "tree.dot", rankdir="TD")  # Generate a DOT file
        generate_python_code(ast, output)  # Call the function that translates the AST


'''Gracias por su atención'''
