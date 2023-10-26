from pyswip import Prolog

file_of_examples = open('prolog_minesweeper/query_5.pl', 'r')
examples = file_of_examples.read().split('.')

prolog = Prolog()
prolog.consult("./prolog_minesweeper/minesweeper.pl")

for solution in prolog.query(examples[0]):
    input_field=solution



