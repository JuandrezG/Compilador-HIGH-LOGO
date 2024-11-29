High-LOGO Compiler
This project implements a compiler for High-LOGO, a high-level programming language inspired by Logo. The compiler translates High-LOGO code into Python, enabling the use of the Turtle module to visualize graphical instructions.

How It Works
Input: The user writes a program in High-LOGO syntax and saves it in a .hlogo file.
Parsing: The compiler uses the Lark library to parse the code and generate an Abstract Syntax Tree (AST).
Translation: The AST is traversed, and the High-LOGO instructions are converted into equivalent Python code.
Execution: The generated Python code uses the Turtle module to execute the graphical commands, producing visual output.
Key Features
Control Structures: Support for if-else, single for loops, and nested for loops with range-based iteration.
Function Definitions: Allows the creation and invocation of reusable functions with parameters.
Graphical Commands: Includes commands for movement, pen control, and drawing.
Boolean Logic: Implements AND, OR, and NOT operators for conditional statements.
Range Expressions: Supports flexible range arguments for loops.
Error Handling: Provides clear error messages for invalid inputs or missing files.
Developer Workflow
Write the High-LOGO program in a .hlogo file.
Run the compiler to generate the corresponding Python script.
Execute the Python script to visualize the output using Turtle.
Technologies Used
Python: For implementing the compiler and executing generated code.
Lark Library: For parsing the High-LOGO grammar and generating the AST.
Turtle Module: For graphical rendering of commands.


Supported Features:
Movement Instructions (FD, BK, LT, RT): Control the turtle's movement, including forward, backward, turning, and changing the line thickness.
Pen Control (PU, PD): Raises or lowers the pen, determining whether the turtle draws on the canvas.
Numeric Expressions and Identifiers: Programs can use integers and variable names in expressions.
Conversion Process to Python:
Code Analysis: The compiler uses the Lark library to parse the High-LOGO code and generate an Abstract Syntax Tree (AST).
Instruction Mapping: Each High-LOGO instruction is translated into its Python equivalent. For example, FD 100 is converted to forward(100).
Python Code Generation: The compiler transforms the AST into executable Python code, using the Turtle library for graphics.


Code Examples:
Basic Movement:
High-LOGO:

logo
Copiar código
FD 100  # Move forward 100 units  
BK 50   # Move backward 50 units  
LT 90   # Turn left 90 degrees  
RT 45   # Turn right 45 degrees  
Equivalent Python:

python
Copiar código
forward(100)  
backward(50)  
left(90)  
right(45)  
Pen Control:
High-LOGO:

logo
Copiar código
PU  # Lift the pen  
PD  # Lower the pen  
Equivalent Python:

python
Copiar código
penup()  
pendown()  
Conditionals:
High-LOGO:

logo
Copiar código
if (10 > 5) {  
    FD 100  
} else {  
    BK 50  
}  
Equivalent Python:

python
Copiar código
if 10 > 5:  
    forward(100)  
else:  
    backward(50)  
For Loop:
High-LOGO:

logo
Copiar código
for i in range(5) {  
    FD 50  
}  
Equivalent Python:

python
Copiar código
for i in range(5):  
    forward(50)  
