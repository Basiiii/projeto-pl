import ply.yacc as yacc
from lexer import Lexer


class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

    # Start symbol for the grammar
    def p_program(self, p):
        """program : command
        | program command"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    # Command rules
    def p_command(self, p):
        """command : table_command
        | query_command
        | create_command
        | procedure_command
        | call_command"""
        p[0] = p[1]

    # Table commands
    def p_table_command(self, p):
        """table_command : import_command
        | export_command
        | discard_command
        | rename_command
        | print_command"""
        p[0] = p[1]

    def p_import_command(self, p):
        "import_command : IMPORT TABLE ID FROM STRING"
        p[0] = ("IMPORT", p[3], p[5])

    def p_export_command(self, p):
        "export_command : EXPORT TABLE ID AS STRING"
        p[0] = ("EXPORT", p[3], p[5])

    def p_discard_command(self, p):
        "discard_command : DISCARD TABLE ID"
        p[0] = ("DISCARD", p[3])

    def p_rename_command(self, p):
        "rename_command : RENAME TABLE ID ID"
        p[0] = ("RENAME", p[3], p[4])

    def p_print_command(self, p):
        "print_command : PRINT TABLE ID"
        p[0] = ("PRINT", p[3])

    # Query commands
    def p_query_command(self, p):
        """query_command : select_command
        | select_where_command
        | select_limit_command
        | select_where_limit_command"""
        p[0] = p[1]

    def p_select_command(self, p):
        """select_command : SELECT select_list FROM ID"""
        p[0] = ("SELECT", p[2], p[4], None, None)

    def p_select_where_command(self, p):
        """select_where_command : SELECT select_list FROM ID WHERE condition"""
        p[0] = ("SELECT", p[2], p[4], p[6], None)

    def p_select_limit_command(self, p):
        """select_limit_command : SELECT select_list FROM ID LIMIT NUMBER"""
        p[0] = ("SELECT", p[2], p[4], None, p[6])

    def p_select_where_limit_command(self, p):
        """select_where_limit_command : SELECT select_list FROM ID WHERE condition LIMIT NUMBER"""
        p[0] = ("SELECT", p[2], p[4], p[6], p[8])

    def p_select_list(self, p):
        """select_list : ASTERISK
        | id_list"""
        p[0] = p[1]

    def p_id_list(self, p):
        """id_list : ID
        | id_list COMMA ID"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_condition(self, p):
        """condition : ID EQUALS value
        | ID NOT_EQUALS value
        | ID LESS_THAN value
        | ID GREATER_THAN value
        | ID LESS_EQUALS value
        | ID GREATER_EQUALS value
        | condition AND condition"""
        if len(p) == 4 and p[2] != "AND":
            p[0] = ("CONDITION", p[1], p[2], p[3])
        elif len(p) == 4 and p[2] == "AND":
            p[0] = ("AND", p[1], p[3])

    def p_value(self, p):
        """value : ID
        | STRING
        | NUMBER"""
        p[0] = p[1]

    # Create commands
    def p_create_command(self, p):
        """create_command : create_select_command
        | create_join_command"""
        p[0] = p[1]

    def p_create_select_command(self, p):
        """create_select_command : CREATE TABLE ID SELECT select_list FROM ID WHERE condition
        | CREATE TABLE ID SELECT select_list FROM ID"""
        if len(p) == 9:
            p[0] = ("CREATE_SELECT", p[3], p[5], p[7], None)
        else:
            p[0] = ("CREATE_SELECT", p[3], p[5], p[7], p[9])

    def p_create_join_command(self, p):
        "create_join_command : CREATE TABLE ID FROM ID JOIN ID USING ID"
        p[0] = ("CREATE_JOIN", p[3], p[5], p[7], p[9])

    # Procedure commands
    def p_procedure_command(self, p):
        "procedure_command : PROCEDURE ID DO procedure_body END"
        p[0] = ("PROCEDURE", p[2], p[4])

    def p_procedure_body(self, p):
        """procedure_body : command
        | procedure_body command"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    # Call command
    def p_call_command(self, p):
        "call_command : CALL ID"
        p[0] = ("CALL", p[2])

    # Error rule for syntax errors
    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}', line {p.lineno}")
        else:
            print("Syntax error at EOF")

    # Parse the input
    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)
