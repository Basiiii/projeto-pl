import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lexer import Lexer

lexer = Lexer()
lexer.build()

examples = [
    'IMPORT TABLE estacoes FROM "estacoes.csv";',
    "SELECT * FROM observacoes WHERE Temperatura > 22;",
    "-- This is a comment\nSELECT Id FROM estacoes;",
    '{- Multi-line\ncomment -}\nEXPORT TABLE estacoes AS "est.csv";',
]

for example in examples:
    print("Input:", example)
    lexer.lexer.input(example)
    for token in lexer.lexer:
        print(token)
    print("-" * 40)
