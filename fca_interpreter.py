import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from pprint import PrettyPrinter
import graphviz

pp = PrettyPrinter(sort_dicts=False)


def read_file(filename):
    """Read the contents of a file and return as a string."""
    with open(filename, "r") as file:
        return file.read()


def visualize_ast(ast, output_file="ast", command_index=None):
    """Create a visual representation of the AST using graphviz."""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create full output path with command index if provided
    if command_index is not None:
        output_file = f"{output_file}_command_{command_index}"

    # Create the full path for the output file
    output_path = os.path.join(output_dir, output_file)

    dot = graphviz.Digraph(comment="AST Visualization")
    dot.attr(rankdir="TB")

    def add_node(node, parent_id=None):
        if isinstance(node, (list, tuple)):
            node_id = str(id(node))
            label = node[0] if isinstance(node, tuple) else "List"
            dot.node(node_id, label, shape="box")

            if parent_id:
                dot.edge(parent_id, node_id)

            for child in node[1:] if isinstance(node, tuple) else node:
                add_node(child, node_id)
        else:
            node_id = str(id(node))
            dot.node(node_id, str(node), shape="ellipse")
            if parent_id:
                dot.edge(parent_id, node_id)

    add_node(ast)
    try:
        dot.render(output_path, view=False, format="png", cleanup=True)
        print(f"AST visualization saved to: {output_path}.png")
    except Exception as e:
        print(f"Error creating visualization: {str(e)}", file=sys.stderr)


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
            print(f"Error: File {filename} does not exist.", file=sys.stderr)
            sys.exit(1)
        if not filename.endswith(".cql"):
            print(f"Error: File {filename} must have .cql extension.", file=sys.stderr)
            sys.exit(1)

        content = read_file(filename)
        try:
            ast = parser.parse(content)

            # Create visual representation for each command
            base_name = os.path.splitext(os.path.basename(filename))[0]
            if isinstance(ast, list):
                for i, command in enumerate(ast):
                    print(f"\nCommand {i+1} AST:")
                    print("-" * 50)
                    pp.pprint(command)
                    print("-" * 50)
                    print(f"\nVisualizing command {i+1}:")
                    visualize_ast(command, output_file=base_name, command_index=i + 1)
            else:
                print("Abstract Syntax Tree:")
                pp.pprint(ast)
                visualize_ast(ast, output_file=base_name)

            print("\nExecution Results:")
            result = interpreter.interpret(content)
            if result:
                print(f"<< {result}")
        except Exception as e:
            print(e, file=sys.stderr)
    else:
        # Interactive mode
        print("CQL Interpreter (type 'EXIT' to quit)")
        while True:
            try:
                line = input(">> ")
                if line.strip().upper() == "EXIT":
                    break
                # Parse and show AST
                ast = parser.parse(line)
                print("Abstract Syntax Tree:")
                pp.pprint(ast)
                # Create visual representation
                visualize_ast(ast, output_file="interactive_ast")
                # Execute the command
                result = interpreter.interpret(line)
                if result:
                    print(f"<< {result}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
