import ply.lex as lex


class Lexer:
    # Reserved words
    reserved = {
        "import": "IMPORT",
        "table": "TABLE",
        "from": "FROM",
        "export": "EXPORT",
        "as": "AS",
        "discard": "DISCARD",
        "rename": "RENAME",
        "print": "PRINT",
        "select": "SELECT",
        "where": "WHERE",
        "limit": "LIMIT",
        "create": "CREATE",
        "join": "JOIN",
        "using": "USING",
        "procedure": "PROCEDURE",
        "do": "DO",
        "end": "END",
        "call": "CALL",
        "and": "AND",
    }

    # Token list
    tokens = [
        "ID",
        "STRING",
        "NUMBER",
        "ASTERISK",
        "COMMA",
        "EQUALS",
        "NOT_EQUALS",
        "LESS_THAN",
        "GREATER_THAN",
        "LESS_EQUALS",
        "GREATER_EQUALS",
        "SINGLE_COMMENT",
        "MULTI_COMMENT",
    ] + list(reserved.values())

    # Simple rules for tokens
    t_ASTERISK = r"\*"
    t_COMMA = r","
    t_EQUALS = r"="
    t_NOT_EQUALS = r"<>"
    t_LESS_THAN = r"<"
    t_GREATER_THAN = r">"
    t_LESS_EQUALS = r"<="
    t_GREATER_EQUALS = r">="

    # Ignored characters
    t_ignore = " \t"

    # String handling (including quoted values that can contain commas)
    def t_STRING(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]  # Remove quotes
        return t

    # Number rule
    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    # Identifier rule (including handling reserved words)
    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        # Check if it's a reserved word
        t.type = self.reserved.get(t.value.lower(), "ID")
        return t

    # Single line comment
    def t_SINGLE_COMMENT(self, t):
        r"--.*"
        pass  # No return value, so the comment is ignored

    # Multi-line comment
    def t_MULTI_COMMENT(self, t):
        r"\{-[\s\S]*?-\}"
        pass  # No return value, so the comment is ignored

    # New line handling
    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    # Error handling
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    # Test the lexer
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
