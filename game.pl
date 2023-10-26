:- dynamic board/1.

% Инициализация игровой доски
initialize_board(Width, Height, NumMines) :-
    retractall(board(_)),
    assert(board([])),
    create_board(Width, Height, NumMines).

% Создание игровой доски с минами
create_board(_, _, 0).
create_board(Width, Height, NumMines) :-
    random(1, Width, X),
    random(1, Height, Y),
    add_mine(X, Y),
    NewMines is NumMines - 1,
    create_board(Width, Height, NewMines).

% Добавление мины на доску
add_mine(X, Y) :-
    assert(board([mine(X, Y)|OldBoard])),
    retract(board(OldBoard)).

% Подсчет мин вокруг клетки
count_adjacent_mines(X, Y, Count) :-
    board(Mines),
    findall(_, (member(mine(X1, Y1), Mines), adjacent(X, Y, X1, Y1)), MinesAround),
    length(MinesAround, Count).

% Определение, является ли клетка миной
is_mine(X, Y) :-
    board(Mines),
    member(mine(X, Y), Mines).

% Проверка, является ли клетка пустой (не имеет мин вокруг)
is_empty(X, Y) :-
    \+ is_mine(X, Y),
    count_adjacent_mines(X, Y, 0).

% Открытие клетки
open_cell(X, Y) :-
    is_mine(X, Y),
    write('Game Over! You hit a mine.'), nl,
    halt.
open_cell(X, Y) :-
    is_empty(X, Y),
    write('Opening empty cell at '), write(X), write(', '), write(Y), nl,
    open_adjacent_empty_cells(X, Y).
open_cell(X, Y) :-
    count_adjacent_mines(X, Y, Count),
    write('Cell at '), write(X), write(', '), write(Y), write(' has '), write(Count), write(' mines around.'), nl.

% Рекурсивное открытие пустых клеток вокруг
open_adjacent_empty_cells(X, Y) :-
    adjacent(X, Y, X1, Y1),
    \+ is_mine(X1, Y1),
    \+ is_open(X1, Y1),
    assert(open(X1, Y1)),
    open_cell(X1, Y1),
    open_adjacent_empty_cells(X1, Y1).

% Проверка, открыта ли клетка
is_open(X, Y) :-
    open(X, Y).

% Проверка, являются ли две клетки соседними
adjacent(X1, Y1, X2, Y2) :-
    abs(X1 - X2) =< 1,
    abs(Y1 - Y2) =< 1,
    \+ (X1 = X2, Y1 = Y2).

% Очистка игровой доски
clear_board :-
    retractall(board(_)),
    retractall(open(_,_)).

% Запуск игры
start_game(Width, Height, NumMines) :-
    initialize_board(Width, Height, NumMines),
    open_cell(1, 1).
