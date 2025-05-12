import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from interpreter import Interpreter

interpreter = Interpreter()

examples = [
    'IMPORT TABLE estacoes FROM "estacoes.csv";',
    'IMPORT TABLE observacoes FROM "observacoes.csv";',
    "SELECT * FROM estacoes;",
    "SELECT Id,Local FROM estacoes;",
    "SELECT * FROM observacoes WHERE Temperatura > 22;",
    "CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22;",
    "PRINT TABLE mais_quentes;",
    'EXPORT TABLE mais_quentes AS "mais_quentes.csv";',
    "DISCARD TABLE mais_quentes;",
    "RENAME TABLE estacoes est;",
    "PRINT TABLE est;",
    "PROCEDURE atualizar DO CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22 ; END",
    "CALL atualizar;",
]

for example in examples:
    print("Input:", example)
    output = interpreter.interpret(example)
    if output:
        print(output)
    print("-" * 40)
