/* вызов предиката minesweeper/2 с различными аргументами, который используется для создания игрового поля размером 5х5  */


minesweeper([
[_,_,_,_,_],
[_,_,2,2,_],
[_,_,2,*,_],
[_,_,2,2,_],
[_,_,_,_,_]], X).

minesweeper([
[_,_,_,_,_],
[_,_,1,2,2],
[_,_,1,_],
[_,_,1,2,2],
[_,_,_,_,_]], X).

minesweeper([
[_,_,2,_,3],
[2,_,_,_,_],
[_,_,2,4,_]
[1,_,3,4,_],
[_,_,_,_,_]], X).

minesweeper([
[_,_,3,_,3],
[2,_,_,_,_],
[_,_,2,4,_],
[1,_,3,4,_],
[_,_,_,_,_]], X).

minesweeper(
[[_,_,3,_,3],
[2,_,_,_,_],
[_,2,2,4,_],
[1,_,3,4,_],
[_,3,_,3,_]], X).

minesweeper([
[_,_,3,_,3],
[2,_,_,_,_],
[1,_,3,4,_],
[_,_,_,_,3],
[_,3,_,3,_,]], X).


minesweeper([
[_,_,_,_,_],
[2,_,1,2,_],
[_,_,1,_,_],
[_,_,1,2,_],
[_,_,_,_,_]], X).


minesweeper([
[_,_,2,_,3],
[2,_,_,_,_],
[_,_,2,4,_],
[1,_,3,4,_],
[_,_,_,_,3]], X).