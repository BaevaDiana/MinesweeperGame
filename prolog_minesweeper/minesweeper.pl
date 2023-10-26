
/* реализация предиката minus_one/2
Предикат minus_one/2 используется для ограничения количества соседей для любой клетки на поле сапера до 8.
Каждый вызов minus_one/2 уменьшает первый аргумент на 1 и присваивает результат второму аргументу. */
minus_one(8, 7).
minus_one(7, 6).
minus_one(6, 5).
minus_one(5, 4).
minus_one(4, 3).
minus_one(3, 2).
minus_one(2, 1).
minus_one(1, 0).

/* реализация предиката valid_number/1
Предикат valid_number/1 используется для проверки, является ли аргумент числом.
Каждый вызов valid_number/1 проверяет, является ли его аргумент числом от 0 до 8. */
valid_number(8).
valid_number(7).
valid_number(6).
valid_number(5).
valid_number(4).
valid_number(3).
valid_number(2).
valid_number(1).
valid_number(0).


%% реализация предикатов nonempty/1 и empty/1
/* Предикат nonempty/1 проверяет, является ли аргумент непустым списком.
Предикат empty/1 проверяет, является ли аргумент пустым списком.*/

nonempty([[_|_] | _]).
nonempty([[] | Rest]) :- nonempty(Rest).

empty([]).
empty([[] | Rest]) :- empty(Rest).

/*  реализация предиката first_column/3
Предикат first_column/3 принимает список списков и возвращает первый элемент каждого подсписка в виде списка,
а также оставшуюся часть исходного списка. */
first_column([], [], []).
first_column([[] | Rows], [[] | Remainder], Column) :-
    first_column(Rows, Remainder, Column).

first_column([[Element | Row] | Rows], [Row | Remainder], [Element | Column]) :-
    first_column(Rows, Remainder, Column).


%% реализация предиката transpose/2
/* Предикат transpose/2 принимает список списков и возвращает транспонированный список списков.
Транспонирование списка списков означает, что строки становятся столбцами, а столбцы - строками. */
transpose(All, []) :- empty(All).
transpose(All, [NewRow | Result]) :-
    nonempty(All),
    first_column(All, YetToBeTransposed, NewRow),
    transpose(YetToBeTransposed, Result).


%% реализация предиката tile_reduces/2
/* Предикат tile_reduces/2 используется для проверки, может ли клетка быть уменьшена.
Клетка может быть уменьшена, если она является миной или если это число, которое равно количеству мин в соседних клетках.*/
tile_reduces(*, _).
tile_reduces(0, []).
tile_reduces(Number, [* | Neighbours]) :-
    minus_one(Number, NewNumber),
    tile_reduces(NewNumber, Neighbours).

tile_reduces(Number, [NeighbourNumber | Neighbours]) :-
    valid_number(Number),
    valid_number(NeighbourNumber),
    tile_reduces(Number, Neighbours).


%% реализация предиката row_reduces/2
/* Предикат row_reduces/2 используется для проверки, может ли строка быть уменьшена.
Строка может быть уменьшена, если все ее клетки могут быть уменьшены.*/
row_reduces([], _).
row_reduces([Tile | Row], [Neighbours | Others]) :-
    tile_reduces(Tile, Neighbours),
    row_reduces(Row, Others).


%%  реализация предиката grid_reduces/1
/* Предикат grid_reduces/1 используется для проверки, можно ли уменьшить все числа на игровом поле до 0.
Например, если все клетки на игровом поле содержат мины, то вызов grid_reduces([[*, *, *], [*, *, *], [*, *, *]]) вернет true.
Если все клетки на игровом поле пустые, то вызов grid_reduces([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) вернет true. */

% инициализация
grid_reduces([FirstRow, SecondRow | Tail]) :-
    grid_reduces(none, FirstRow, SecondRow, Tail).

grid_reduces([Row]) :-
    grid_reduces(none, Row, none, []).

%% проверка можно ли уменьшить первую строку
grid_reduces(none, ThisRow, SecondRow, [NextRow | Tail]) :-
    [_ | SecondRowTail] = SecondRow,
    [_ | ThisRowTail] = ThisRow,
    transpose([
        SecondRow,
        [0 | SecondRow],
        SecondRowTail,
        [0 | ThisRow],
        ThisRowTail
    ], Neighbours),
    row_reduces(ThisRow, Neighbours),
    grid_reduces(ThisRow, SecondRow, NextRow, Tail).

%% проверка, можно ли уменьшить первую строка, если всего две строки
grid_reduces(none, ThisRow, SecondRow, []) :-
    [_ | SecondRowTail] = SecondRow,
    [_ | ThisRowTail] = ThisRow,
    transpose([
        SecondRow,
        [0 | SecondRow],
        SecondRowTail,
        [0 | ThisRow],
        ThisRowTail
    ], Neighbours),
    row_reduces(ThisRow, Neighbours),
    grid_reduces(ThisRow, SecondRow, none, []).

%% Первый предикат grid_reduces/4 используется для обработки первой строки, если на игровом поле только одна строка.
grid_reduces(none, ThisRow, none, []) :-
    [_ | ThisRowTail] = ThisRow,
    transpose([
        ThisRowTail, [0 | ThisRow]
    ], Neighbours),
    row_reduces(ThisRow, Neighbours).

%% Этот предикат grid_reduces/4 используется для обработки предпоследней строки игрового поля
grid_reduces(PenultimateRow, ThisRow, none, []) :-
    [_ | PenultimateRowTail] = PenultimateRow,
    [_ | ThisRowTail] = ThisRow,
    transpose([
        [0 | PenultimateRow], PenultimateRow, PenultimateRowTail,
        [0 | ThisRow], ThisRowTail
    ], Neighbours),
    row_reduces(ThisRow, Neighbours).


%% Этот предикат grid_reduces/4 используется для обработки последней строки игрового поля
grid_reduces(AboveRow, ThisRow, BelowRow, []) :-
    [_ | AboveRowTail] = AboveRow,
    [_ | BelowRowTail] = BelowRow,
    [_ | ThisRowTail] = ThisRow,
    transpose([
        AboveRow, [0 | AboveRow], AboveRowTail,
        BelowRow, [0 | BelowRow], BelowRowTail,
        [0 | ThisRow], ThisRowTail
    ], Neighbours),
    row_reduces(ThisRow, Neighbours),
    grid_reduces(ThisRow, BelowRow, none, []).

%% Этот предикат grid_reduces/4 обрабатывает все строки игрового поля, кроме первой и последней
grid_reduces(AboveRow, ThisRow, BelowRow, [NextRow | Tail]) :-
    [_ | AboveRowTail] = AboveRow,
    [_ | BelowRowTail] = BelowRow,
    [_ | ThisRowTail] = ThisRow,
    transpose([
        AboveRow, [0 | AboveRow], AboveRowTail,
        BelowRow, [0 | BelowRow], BelowRowTail,
        [0 | ThisRow], ThisRowTail
    ], Neighbours),
    row_reduces(ThisRow, Neighbours),
    grid_reduces(ThisRow, BelowRow, NextRow, Tail).

/* Этот предикат используется для проверки, можно ли уменьшить все числа на игровом поле до 0.
Он вызывает предикат grid_reduces/1, который проверяет, можно ли уменьшить все числа на игровом поле до 0.*/
valid_board(Board) :- grid_reduces(Board).

%% вывод игрового поля
/* Предикат print_board/1 используется для печати игрового поля. Он принимает список списков и печатает каждую строку, используя предикат print_row/1.
Предикат print_row/1 используется для печати строки игрового поля. Он принимает список и печатает каждый элемент списка, разделяя их пробелами. */

print_board([]).
print_board([Row | Rows]) :- print_row(Row), print_board(Rows).

print_row([]) :- nl.
print_row([Tile | Tiles]) :- write(Tile), write(" "), print_row(Tiles).

/* Предикат minesweeper/1 используется для проверки, можно ли уменьшить все числа на игровом поле до 0
(если все числа на игровом поле могут быть уменьшены до 0, то это означает, что все клетки, кроме тех, которые содержат мины, были открыты.)
Предикат minesweeper/2 используется для проверки, является ли игровое поле допустимым, и возвращает игровое поле в качестве результата.*/

minesweeper(Board) :- valid_board(Board).
minesweeper(Board, Result) :- minesweeper(Board), Result = Board.
