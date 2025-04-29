import csv
import os
from parser import Parser


class Interpreter:
    def __init__(self):
        self.parser = Parser()
        # Dictionary to store tables
        self.tables = {}
        # Dictionary to store procedures
        self.procedures = {}

    def interpret(self, code):
        """Parse and execute the code."""
        parsed = self.parser.parse(code)
        if not parsed:
            return None

        # Execute each command
        for command in parsed:
            result = self.execute_command(command)
            if result:
                return result

    def execute_command(self, command):
        """Execute a single command."""
        cmd_type = command[0]

        # Table commands
        if cmd_type == "IMPORT":
            return self.import_table(command[1], command[2])
        elif cmd_type == "EXPORT":
            return self.export_table(command[1], command[2])
        elif cmd_type == "DISCARD":
            return self.discard_table(command[1])
        elif cmd_type == "RENAME":
            return self.rename_table(command[1], command[2])
        elif cmd_type == "PRINT":
            return self.print_table(command[1])

        # Query commands
        elif cmd_type == "SELECT":
            columns, table_name, condition, limit = (
                command[1],
                command[2],
                command[3],
                command[4],
            )
            return self.select_data(columns, table_name, condition, limit)

        # Create commands
        elif cmd_type == "CREATE_SELECT":
            new_table, columns, table_name, condition = (
                command[1],
                command[2],
                command[3],
                command[4],
            )
            return self.create_table_select(new_table, columns, table_name, condition)
        elif cmd_type == "CREATE_JOIN":
            new_table, table1, table2, col_name = (
                command[1],
                command[2],
                command[3],
                command[4],
            )
            return self.create_table_join(new_table, table1, table2, col_name)

        # Procedure commands
        elif cmd_type == "PROCEDURE":
            return self.define_procedure(command[1], command[2])
        elif cmd_type == "CALL":
            return self.call_procedure(command[1])

    # CSV handling functions
    def read_csv(self, filename):
        """Read a CSV file and return its data as a dictionary."""
        if not os.path.exists(filename):
            print(f"Error: File {filename} does not exist.")
            return None

        try:
            data = []
            header = None

            with open(filename, "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # Skip comment lines
                    if row and row[0].startswith("#"):
                        continue

                    # First non-comment line is the header
                    if header is None:
                        header = row
                    else:
                        data.append(row)

            return {"header": header, "data": data}
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return None

    def write_csv(self, table, filename):
        """Write a table to a CSV file."""
        try:
            with open(filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(table["header"])
                writer.writerows(table["data"])
            return True
        except Exception as e:
            print(f"Error writing CSV file: {str(e)}")
            return False

    # Table commands implementation
    def import_table(self, table_name, filename):
        """Import a table from a CSV file."""
        data = self.read_csv(filename)
        if data:
            self.tables[table_name] = data
            return f"Table '{table_name}' imported successfully."

    def export_table(self, table_name, filename):
        """Export a table to a CSV file."""
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' does not exist."

        if self.write_csv(self.tables[table_name], filename):
            return f"Table '{table_name}' exported successfully to '{filename}'."
        return f"Error exporting table '{table_name}'."

    def discard_table(self, table_name):
        """Remove a table from memory."""
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' does not exist."

        del self.tables[table_name]
        return f"Table '{table_name}' discarded successfully."

    def rename_table(self, old_name, new_name):
        """Rename a table."""
        if old_name not in self.tables:
            return f"Error: Table '{old_name}' does not exist."
        if new_name in self.tables:
            return f"Error: Table '{new_name}' already exists."

        self.tables[new_name] = self.tables[old_name]
        del self.tables[old_name]
        return f"Table '{old_name}' renamed to '{new_name}' successfully."

    def print_table(self, table_name):
        """Print a table to the console."""
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' does not exist."

        table = self.tables[table_name]
        result = []

        # Print header
        header_str = " | ".join(table["header"])
        result.append(header_str)
        result.append("-" * len(header_str))

        # Print data
        for row in table["data"]:
            result.append(" | ".join(row))

        return "\n".join(result)

    # Query commands implementation
    def select_data(self, columns, table_name, condition, limit):
        """Select data from a table with optional condition and limit."""
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' does not exist."

        table = self.tables[table_name]
        header = table["header"]
        data = table["data"]

        # If columns is *, select all columns
        if columns == "*":
            selected_cols = header
        else:
            # Verify that all specified columns exist
            for col in columns:
                if col not in header:
                    return (
                        f"Error: Column '{col}' does not exist in table '{table_name}'."
                    )
            selected_cols = columns

        # Filter rows by condition if specified
        if condition:
            filtered_data = self.filter_by_condition(data, header, condition)
        else:
            filtered_data = data

        # Apply limit if specified
        if limit and limit > 0:
            filtered_data = filtered_data[:limit]

        # Project only the selected columns
        if columns == "*":
            result_header = header
            result_data = filtered_data
        else:
            col_indices = [header.index(col) for col in selected_cols]
            result_header = selected_cols
            result_data = [[row[i] for i in col_indices] for row in filtered_data]

        # Format the result
        result = []
        header_str = " | ".join(result_header)
        result.append(header_str)
        result.append("-" * len(header_str))

        for row in result_data:
            result.append(" | ".join(row))

        return "\n".join(result)

    def filter_by_condition(self, data, header, condition):
        """Filter table data by a condition."""
        if condition[0] == "CONDITION":
            col_name, op, value = condition[1], condition[2], condition[3]

            # Check if the column exists
            if col_name not in header:
                print(f"Error: Column '{col_name}' does not exist.")
                return data

            col_index = header.index(col_name)

            # Filter the data
            filtered = []
            for row in data:
                cell_value = row[col_index]

                if op == "=" and str(cell_value) == str(value):
                    filtered.append(row)
                elif op == "<>" and str(cell_value) != str(value):
                    filtered.append(row)
                elif op == "<" and str(cell_value) < str(value):
                    filtered.append(row)
                elif op == ">" and str(cell_value) > str(value):
                    filtered.append(row)
                elif op == "<=" and str(cell_value) <= str(value):
                    filtered.append(row)
                elif op == ">=" and str(cell_value) >= str(value):
                    filtered.append(row)

            return filtered

        elif condition[0] == "AND":
            # Apply both conditions
            left_filtered = self.filter_by_condition(data, header, condition[1])
            return self.filter_by_condition(left_filtered, header, condition[2])

        return data

    # Create commands implementation
    def create_table_select(self, new_table, columns, table_name, condition):
        """Create a new table from a select query."""
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' does not exist."
        if new_table in self.tables:
            return f"Error: Table '{new_table}' already exists."

        table = self.tables[table_name]
        header = table["header"]
        data = table["data"]

        # If columns is *, select all columns
        if columns == "*":
            selected_cols = header
        else:
            # Verify that all specified columns exist
            for col in columns:
                if col not in header:
                    return (
                        f"Error: Column '{col}' does not exist in table '{table_name}'."
                    )
            selected_cols = columns

        # Filter rows by condition if specified
        if condition:
            filtered_data = self.filter_by_condition(data, header, condition)
        else:
            filtered_data = data

        # Project only the selected columns
        if columns == "*":
            result_header = header
            result_data = filtered_data
        else:
            col_indices = [header.index(col) for col in selected_cols]
            result_header = selected_cols
            result_data = [[row[i] for i in col_indices] for row in filtered_data]

        # Create the new table
        self.tables[new_table] = {"header": result_header, "data": result_data}

        return f"Table '{new_table}' created successfully."

    def create_table_join(self, new_table, table1, table2, col_name):
        """Create a new table by joining two tables on a common column."""
        if table1 not in self.tables:
            return f"Error: Table '{table1}' does not exist."
        if table2 not in self.tables:
            return f"Error: Table '{table2}' does not exist."
        if new_table in self.tables:
            return f"Error: Table '{new_table}' already exists."

        # Check if the join column exists in both tables
        t1 = self.tables[table1]
        t2 = self.tables[table2]

        if col_name not in t1["header"]:
            return f"Error: Column '{col_name}' does not exist in table '{table1}'."
        if col_name not in t2["header"]:
            return f"Error: Column '{col_name}' does not exist in table '{table2}'."

        # Get column indices
        t1_col_idx = t1["header"].index(col_name)
        t2_col_idx = t2["header"].index(col_name)

        # Create new header (excluding the duplicate join column)
        new_header = t1["header"] + [col for col in t2["header"] if col != col_name]

        # Create new data (join where column values match)
        new_data = []
        for row1 in t1["data"]:
            join_val = row1[t1_col_idx]
            for row2 in t2["data"]:
                if row2[t2_col_idx] == join_val:
                    new_row = row1 + [
                        row2[i] for i in range(len(row2)) if t2["header"][i] != col_name
                    ]
                    new_data.append(new_row)

        # Create the new table
        self.tables[new_table] = {"header": new_header, "data": new_data}

        return f"Table '{new_table}' created by joining '{table1}' and '{table2}' on '{col_name}'."

    # Procedure commands implementation
    def define_procedure(self, proc_name, commands):
        """Define a procedure with a list of commands."""
        self.procedures[proc_name] = commands
        return f"Procedure '{proc_name}' defined successfully."

    def call_procedure(self, proc_name):
        """Call a procedure by name."""
        if proc_name not in self.procedures:
            return f"Error: Procedure '{proc_name}' does not exist."

        # Execute each command in the procedure
        for command in self.procedures[proc_name]:
            result = self.execute_command(command)
            if result:
                print(result)

        return f"Procedure '{proc_name}' executed successfully."
