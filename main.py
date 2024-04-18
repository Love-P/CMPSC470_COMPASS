import re

def lexer(code):
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS)
    line_number = 1
    token_list = []
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group().lower()  # Normalize to lowercase
        if kind == 'NUMBER':
            value = int(value)
        elif kind == 'STRING':
            value = value[1:-1]
        elif kind == 'SKIP' or kind == 'NEWLINE':
            continue
        token_list.append((kind, value, line_number))
    return token_list

TOKENS = [
    ('NUMBER',    r'\d+'),
    ('STRING',    r'"[^"]*"|\'[^\']*\''),
    ('ASSIGN',    r'\bset\b'),
    ('TO',        r'\bto\b'),
    ('PRINT',     r'\bprint\b'),
    ('ADD',       r'\badd\b'),
    ('SUBTRACT',  r'\bsub\b'),
    ('MULTIPLY',  r'\bmult\b'),
    ('DIVIDE',    r'\bdiv\b'),
    ('IDENT',     r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('HELP',      r'\bhelp\b'),
    ('SKIP',      r'[ \t]+'),
    ('NEWLINE',   r'\n'),
    ('MISMATCH',  r'.'),
]

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.commands = ["set", "print", "add", "sub", "mult", "div", "help", "clear", "exit"]

    def clear(self):
        self.variables.clear()

    def execute(self, tokens):
        it = iter(tokens)
        try:
            while True:
                token = next(it)
                if token[0] in ['SKIP', 'NEWLINE']:
                    continue
                if token[0] == 'MISMATCH' or token[1] not in self.commands:
                    print(f"Unrecognized command '{token[1]}'. Type 'help' for command list.")
                    return

                if token[1] == 'set':
                    self.handle_assignment(it)
                elif token[1] == 'print':
                    self.handle_print(it)
                elif token[1] in ['add', 'sub', 'mult', 'div']:
                    self.handle_math_operation(token[1], it)
                elif token[1] == 'help':
                    self.print_help()
                elif token[1] == 'clear':
                    self.clear()
                    print("Environment cleared.")
                elif token[1] == 'exit':
                    exit()
                break  # Break after processing a command
        except StopIteration:
            print("Incomplete command. Please check your syntax.")

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
            print(self.variables[var_name])
        else:
            print(f"Undefined variable '{var_name}'.")

    def handle_math_operation(self, operation, it):
        operand1 = next(it)
        to_token = next(it)  # This captures the 'to' in your command.
        operand2 = next(it)

        op1 = self.variables.get(operand1[1], operand1[1]) if operand1[0] == 'IDENT' else operand1[1]
        op2 = self.variables.get(operand2[1], operand2[1]) if operand2[0] == 'IDENT' else operand2[1]
        try:
            result = 0
            if operation == 'add':
                result = op1 + op2
            elif operation == 'sub':
                result = op1 - op2
            elif operation == 'mult':
                result = op1 * op2
            elif operation == 'div':
                if op2 == 0:
                    print("Error: Division by zero")
                    return
                result = op1 / op2
            print(f"The result of {operation} is {result}")
        except TypeError as e:
            print(f"Error: {e} - check that both operands are numbers or properly defined variables.")

    def print_help(self):
        print("Available commands:")
        print("  set <var> to <value> - Assigns a value to a variable")
        print("  print <var> - Prints the value of a variable")
        print("  add <arg1> <arg2> - Adds two values")
        print("  sub <arg1> <arg2> - Subtracts second from the first")
        print("  mult <arg1> <arg2> - Multiplies two values")
        print("  div <arg1> <arg2> - Divides the first by the second")
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
