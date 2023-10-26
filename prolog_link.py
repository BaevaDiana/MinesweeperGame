from pyswip import Prolog

file_of_examples = open('./prolog_minesweeper/minesweeper.pl', 'r')
examples = file_of_examples.read().split('.')

prolog = Prolog()

prolog.consult("./prolog_minesweeper/minesweeper.pl")




