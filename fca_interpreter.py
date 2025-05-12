import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from pprint import PrettyPrinter

pp = PrettyPrinter(sort_dicts=False)


def read_file(filename):
    """Read the contents of a file and return as a string."""
    with open(filename, "r") as file:
        return file.read()


def main():
    """Main entry point for the FCA interpreter."""
    # Create the lexer, parser, and interpreter
    parser = Parser()
    interpreter = Interpreter()

    # Check if a file was provided as an argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        # Check if the file exists and has .cql extension
        if not os.path.exists(filename):
            print(f"Error: File {filename} does not exist.")
            sys.exit(1)
        if not filename.endswith(".cql"):
            print(f"Error: File {filename} must have .cql extension.")
            sys.exit(1)

        # Read the file and interpret it
        content = read_file(filename)
        try:
            # Parse and show AST
            ast = parser.parse(content)
            print("Abstract Syntax Tree:")
            pp.pprint(ast)
            print("\nExecution Results:")
            # Execute the commands
            interpreter.interpret(content)
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
    else:
        # Interactive mode
        print("CQL Interpreter (type 'EXIT' to quit)")
        while True:
            try:
                line = input("cql> ")
                if line.strip().upper() == "EXIT":
                    break
                # Parse and show AST
                ast = parser.parse(line)
                print("Abstract Syntax Tree:")
                pp.pprint(ast)
                print("\nExecution Results:")
                # Execute the command
                result = interpreter.interpret(line)
                if result:
                    print(result)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
