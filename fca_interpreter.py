import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def read_file(filename):
    """Read the contents of a file and return as a string."""
    with open(filename, "r") as file:
        return file.read()


def main():
    """Main entry point for the FCA interpreter."""
    # Create the lexer, parser, and interpreter
    interpreter = Interpreter()

    # Check if a file was provided as an argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        # Check if the file exists and has .fca extension
        if not os.path.exists(filename):
            print(f"Error: File {filename} does not exist.")
            sys.exit(1)
        if not filename.endswith(".fca"):
            print(f"Error: File {filename} must have .fca extension.")
            sys.exit(1)

        # Read the file and interpret it
        content = read_file(filename)
        interpreter.interpret(content)
    else:
        # Interactive mode
        print("FCA Interpreter (type 'EXIT' to quit)")
        while True:
            try:
                line = input("fca> ")
                if line.strip().upper() == "EXIT":
                    break
                result = interpreter.interpret(line)
                if result:
                    print(result)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
