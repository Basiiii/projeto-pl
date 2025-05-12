import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from parser import Parser

parser = Parser()

examples = [
    'IMPORT TABLE estacoes FROM "estacoes.csv";',
    "SELECT DataHoraObservacao,Id FROM observacoes;",
    "SELECT * FROM observacoes WHERE Temperatura > 22;",
    "CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22;",
    "PROCEDURE atualizar DO CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22 ; END",
    '-- comment\nEXPORT TABLE estacoes AS "est.csv";',
]

for example in examples:
    print("Input:", example)
    result = parser.parse(example)
    print("AST:", result)
    print("-" * 40)
