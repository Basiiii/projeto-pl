# FCA Interpreter

A Python interpreter for a custom SQL-like query language that manipulates CSV data.

## Installation

1. Make sure you have Python 3.x installed.
2. Install the required packages:
   ```
   pip install ply
   ```

## Usage

You can use the interpreter in two ways:

1. Interactive mode:
   ```
   python fca_interpreter.py
   ```

2. File mode:
   ```
   python fca_interpreter.py your_script.fca
   ```

## Language Syntax

The language supports the following commands:

### Table Commands

- Import a table from a CSV file:
  ```
  IMPORT TABLE tablename FROM "filename.csv"
  ```

- Export a table to a CSV file:
  ```
  EXPORT TABLE tablename AS "filename.csv"
  ```

- Remove a table from memory:
  ```
  DISCARD TABLE tablename
  ```

- Rename a table:
  ```
  RENAME TABLE oldname newname
  ```

- Display a table:
  ```
  PRINT TABLE tablename
  ```

### Query Commands

- Select all columns from a table:
  ```
  SELECT * FROM tablename
  ```

- Select specific columns:
  ```
  SELECT column1, column2 FROM tablename
  ```

- Filter with conditions:
  ```
  SELECT * FROM tablename WHERE column = value
  ```

- Limit the number of results:
  ```
  SELECT * FROM tablename LIMIT 10
  ```

- Combine conditions:
  ```
  SELECT * FROM tablename WHERE column1 = value1 AND column2 > value2
  ```

### Table Creation Commands

- Create a new table from a query:
  ```
  CREATE TABLE newtable SELECT * FROM tablename WHERE condition
  ```

- Join two tables:
  ```
  CREATE TABLE newtable FROM table1 JOIN table2 USING columnname
  ```

### Procedures

- Define a procedure:
  ```
  PROCEDURE name DO
    command1
    command2
    ...
  END
  ```

- Call a procedure:
  ```
  CALL name
  ```

### Comments

- Single-line comments:
  ```
  -- This is a comment
  ```

- Multi-line comments:
  ```
  {- This is a
     multi-line
     comment -}
  ```

## CSV Format

- The first line is the header with column names
- Values are separated by commas
- Quoted values can contain commas
- Lines starting with # are comments and are ignored

## Example

```
-- Import a CSV file
IMPORT TABLE employees FROM "employees.csv"

-- Display the table
PRINT TABLE employees

-- Create a new table with filtered data
CREATE TABLE senior_employees SELECT * FROM employees WHERE age > 40

-- Display the filtered table
PRINT TABLE senior_employees

-- Create a procedure
PROCEDURE print_tables DO
  PRINT TABLE employees
  PRINT TABLE senior_employees
END

-- Call the procedure
CALL print_tables 