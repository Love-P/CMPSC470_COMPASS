import unittest
from io import StringIO
import sys
from main import lexer, Interpreter  # Importing from your main code

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()  # Initialize the interpreter
        self.old_stdout = sys.stdout  # Backup the current stdout
        self.mystdout = StringIO()  # Create a new stream to capture output
        sys.stdout = self.mystdout  # Redirect stdout to capture output


    def tearDown(self):
        sys.stdout = self.old_stdout  # Restore stdout to its original state

    def test_set_variable(self):
        code = "set x to 10"
        tokens = lexer(code)  # Generate tokens
        self.interpreter.execute(tokens)  # Execute tokens
        self.assertEqual(self.interpreter.variables["x"], 10)  # Assert variable set correctly

    def test_print_variable(self):
        self.interpreter.variables["x"] = 10  # Set a variable in advance
        code = "print x"
        tokens = lexer(code)
        self.interpreter.execute(tokens)
        output = self.mystdout.getvalue().strip()  # Get the captured output
        self.assertEqual(output, "10")  # Assert the printed value is correct

    def test_math_operations(self):
        self.interpreter.variables["x"] = 10  # Set a variable
        # Test addition
        code = "add x to 10"
        tokens = lexer(code)
        self.interpreter.execute(tokens)
        output = self.mystdout.getvalue().strip()  # Get the captured output
        self.assertIn("The result of add is 20", output)

        # Test multiplication
        code = "mult x to 10"
        tokens = lexer(code)
        self.interpreter.execute(tokens)
        output = self.mystdout.getvalue().strip()  # Get the captured output
        self.assertIn("The result of mult is 100", output)

    def test_if_statement(self):
        self.interpreter.variables["x"] = 10  # Set a variable
        code = "if x > 5: print x"
        tokens = lexer(code)
        self.interpreter.execute(tokens)
        output = self.mystdout.getvalue().strip()  # Get the captured output
        self.assertEqual(output, "10")  # Assert the correct output for the 'if' condition

    def tearDown(self):
        sys.stdout = self.old_stdout  # Restore stdout to its original state


if __name__ == "__main__":
    unittest.main()  # Run the tests
