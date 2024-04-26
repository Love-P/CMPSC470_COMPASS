import re

TOKENS = [
    ('NUMBER', r'\d+'),
    ('STRING', r'"[^"]*"|\'[^\']*\''),
    ('ASSIGN', r'\bset\b'),
    ('TO', r'\bto\b'),
    ('PRINT', r'\bprint\b'),
    ('ADD', r'\badd\b'),
    ('SUBTRACT', r'\bsub\b'),
    ('MULTIPLY', r'\bmult\b'),
    ('DIVIDE', r'\bdiv\b'),
    ('IDENT', r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('EQUAL', r'=='),
    ('NOTEQUAL', r'!='),
    ('GREATER', r'>'),
    ('LESS', r'<'),
    ('GREATEREQ', r'>='),
    ('LESSEQ', r'<='),
    ('HELP', r'\bhelp\b'),
    ('SKIP', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('SEMICOLON', r';'),
    ('COLON', r':'),
    ('MISMATCH', r'.'),
]

def lexer(code):
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS)
    token_list = []
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group().lower()  # Normalize to lowercase
        if kind == 'NUMBER':
            value = int(value)
        elif kind in ['SKIP', 'NEWLINE']:
            continue
        token_list.append((kind, value))
    return token_list

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.commands = [
            "set", "print", "add", "sub", "mult", "div",
            "if", "else", "help", "clear", "exit"
        ]

    def clear(self):
        self.variables.clear()
        print("Environment cleared.")

    def execute(self, tokens):
        it = iter(tokens)
        try:
            while True:
                token = next(it)
                if token[1] == 'set':
                    self.handle_assignment(it)
                elif token[1] == 'print':
                    self.handle_print(it)
                elif token[1] in ['add', 'sub', 'mult', 'div']:
                    self.handle_math_operation(token[1], it)
                elif token[1] == 'if':
                    self.handle_if(it)
                elif token[1] == 'help':
                    self.print_help()
                elif token[1] == 'clear':
                    self.clear()
                elif token[1] == 'exit':
                    exit()
        except StopIteration:
            pass

    def handle_assignment(self, it):
        identifier = next(it)
        to_token = next(it)
        value_token = next(it)
        if identifier[0] != 'IDENT' or to_token[0] != 'TO':
            print("Syntax error in set command. Expected format: set <var> to <value>")
            return
        self.variables[identifier[1]] = value_token[1]
        print(f"Variable '{identifier[1]}' set to {value_token[1]}.")

    def handle_print(self, it):
        var_name_token = next(it)
        if var_name_token[0] != 'IDENT':
            print("Syntax error in print command. Expected format: print <var>")
            return
        var_name = var_name_token[1]
        if var_name in self.variables:
            print(str(self.variables[var_name]))  # Ensure the variable is converted to a string
        else:
            print(f"Undefined variable '{var_name}'.")

    def handle_math_operation(self, operation, it):
        operand1_token = next(it)
        to_token = next(it)  # This should be the 'to' token
        operand2_token = next(it)

        operand1 = self.variables.get(operand1_token[1], operand1_token[1])
        operand2 = self.variables.get(operand2_token[1], operand2_token[1])
        if isinstance(operand1, str) and operand1.isdigit():
            operand1 = int(operand1)
        if isinstance(operand2, str) and operand2.isdigit():
            operand2 = int(operand2)

        try:
            if operation == 'add':
                result = operand1 + operand2
            elif operation == 'sub':
                result = operand1 - operand2
            elif operation == 'mult':
                result = operand1 * operand2
            elif operation == 'div':
                if operand2 == 0:
                    print("Error: Division by zero")
                    return
                result = operand1 / operand2
            print(f"The result of {operation} is {result}")
        except TypeError as e:
            print(f"Error: {e} - check that both operands are numbers or properly defined variables.")

    def handle_if(self, it):
        condition = self.evaluate_condition(it)  # Get the condition
        next(it)  # Skip the colon token
        if condition:
            self.execute_inline(it)

    def evaluate_condition(self, it):
        operand1_token = next(it)
        operator = next(it)[1]
        operand2_token = next(it)

        operand1 = self.variables.get(operand1_token[1], operand1_token[1])
        operand2 = self.variables.get(operand2_token[1], operand2_token[1])
        if isinstance(operand1, str) and operand1.isdigit():
            operand1 = int(operand1)
        if isinstance(operand2, str) and operand2.isdigit():
            operand2 = int(operand2)

        if operator == '>':
            return operand1 > operand2
        elif operator == '<':
            return operand1 < operand2
        elif operator == '==':
            return operand1 == operand2
        elif operator == '!=':
            return operand1 != operand2
        elif operator == '>=':
            return operand1 >= operand2
        elif operator == '<=':
            return operand1 <= operand2
        else:
            raise ValueError("Unsupported operator")

    def execute_inline(self, it):
        token = next(it)
        if token[1] == 'print':
            self.handle_print(it)

    def print_help(self):
        print("Available commands:")
        print("  set <var> to <value> - Assigns a value to a variable")
        print("  print <var> - Prints the value of a variable")
        print("  add <arg1> to <arg2> - Adds two values")
        print("  sub <arg1> to <arg2> - Subtracts second from the first")
        print("  mult <arg1> to <arg2> - Multiplies two values")
        print("  div <arg1> to <arg2> - Divides the first by the second")
        print("  if <condition>: <command> - Executes a command if the condition is true")
        print("  clear - Clears all variables")
        print("  help - Displays this help message")
        print("  exit - Exits the program")

def main_loop():
    interpreter = Interpreter()
    print("Welcome to the world of programming! Get started with Compass.\nWith the help of Compass, you will master the art of coding! Type 'exit' to exit.")
    while True:
        try:
            line = input(">> ")
            if line.strip().lower() == "exit":
                break
            if not line.strip():
                continue
            tokens = lexer(line)
            interpreter.execute(tokens)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main_loop()
