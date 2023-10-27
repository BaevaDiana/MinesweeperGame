import random
from pyswip import Prolog
from tkinter import *
from tkinter import Button
from  random import choice
import time

xBtn=16;yBtn=16;
btn = [[]]  # Списки с кнопками
playTime = 0  # Время игры
imgMark = '\u2661'; imgMine = '\u2665'  # Символ маркера и мины
nMoves = 0; mrk = 0  #Счётчик ходов и маркеров
tk = Tk()
tk.title('Игра Сапер')
tk.geometry(str(44 * xBtn) + 'x' + str(44 * yBtn + 10))

def play(ni,nj):  # Обработка нажатия на клетку
    global xBtn, yBtn,input_field, mines, nMoves, mrk, playTime
    if len(input_field) < xBtn * yBtn:  # Если поле ещё не создано
        return()
    nMoves += 1
    if nMoves == 1:  # Если это первый ход игрока
        playTime = time.time()
        for i in range(0, xBtn):
            for j in range (0,yBtn):# Подсчитываем количество мин вокруг каждой клетки
                if input_field[i][j] != '*':
                    k = 0
                    if input_field[i - 1][j] == '*': k += 1  # слева
                    if input_field[i - 1][j-1] == '*': k += 1  # слева сверху
                    if input_field[i-1][j+1] == '*': k += 1  # слева снизу
                    if input_field[i + 1][j] == '*': k += 1  # справа
                    if input_field[i+1][j-1] == '*': k += 1  # справа сверху
                    if input_field[i + 1][j+1] == '*': k += 1  # справа снизу
                    if input_field[i][j+1] == "*": k += 1  # сверху
                    if input_field[i][j-1] == '*': k += 1  # снизу
                    input_field[i][j] = k
    if btn[ni][nj].cget('text') == imgMark:  # Если поле было промаркировано
        mrk -= 1
        tk.title('Осторожно! Вокруг ' + str(mines - mrk) + ' Мин(ы)!!!!')
    btn[ni][nj].config(text=input_field[ni][nj], state=DISABLED, bg='white')  # Отображаем игровую ситуацию
    if input_field[ni][nj] == 0:  # Пустое поле без соседей
        btn[ni][nj].config(text=' ', bg='#ccb')
    elif input_field[ni][nj] == '*':  # Мина
        btn[ni][nj].config(text=imgMine)
        if nMoves <= (xBtn * yBtn - mines) or mines >= mrk:  # Если открытых клеток меньше чем может быть или мин больше помеченных,то проиграл
            nMoves = 32000  # Если проиграл, то уже не выиграет
            chainReaction(0,0)  # Цепная реакция
            tk.title('Вы проиграли :(')
    if nMoves == (xBtn * yBtn - mines) and mines == mrk:  # Если все клетки открыты и мины помечены
        tk.title('Поздравляю! Вы выиграли за ' + str(int(time.time() - playTime)) + ' сек')
        winner(0,0)
#
def chainReaction(i,j):  # Цепная реакция при проигрыше
    if i < xBtn:
        if j < yBtn:
            if input_field[i][j] == -1 and btn[i][j].cget('text') == ' ': #мина и клетка пустая
                btn[i][j].config(text=imgMine)
                btn[i][j].flash()
                tk.bell()
                tk.after(50, chainReaction, i, j + 1)  # Установить задержку 50 миллисекунд и рекурсивно вызвать функцию
        else:
            chainReaction(i + 1, 0)  # Если j превышает yBtn, вызвать для следующего i и сбросить j в 0


def winner(i, j):  # Функция для отображения победы
    if i < xBtn:
        if j < yBtn:
            if input_field[i][j] == 0:  # Если значение в массиве input_field равно 0
                btn[i][j].config(state=NORMAL, text='☺')  # Настроить кнопку btn на отображение "☺"
                btn[i][j].flash()  # Анимировать кнопку
                tk.bell()  # Воспроизвести звуковой сигнал
                btn[i][j].config(text=' ', state=DISABLED)  # Снова настроить кнопку на отображение пустоты и отключение
                tk.after(50, winner, i, j + 1)  # Установить задержку 50 миллисекунд и рекурсивно вызвать функцию winner для следующего j
        else:
            winner(i + 1, 0)  # Если j превышает yBtn, вызвать winner для следующего i и сбросить j в 0


def marker(ni, nj):  # Функция для пометки клеток, где могут быть мины
    global mrk, mines, playTime
    if (btn[ni][nj].cget('state')) != 'disabled':  # Проверка, что кнопка не отключена
        if btn[ni][nj].cget('text') == imgMark:  # Если на кнопке уже установлена метка
            btn[ni][nj].config(text=' ')  # Убрать метку
            mrk -= 1  # Уменьшить количество помеченных мин
        else:
            btn[ni][nj].config(text=imgMark, fg='blue')  # Установить метку на кнопке с синим текстом
            mrk += 1  # Увеличить количество помеченных мин
        tk.title('Осторожно! Вокруг ' + str(mines - mrk) + ' Мин!!!!')  # Обновление заголовка окна

    if nMoves == (xBtn * yBtn - mines) and mines == mrk:  # Если все клетки открыты и все мины помечены
        tk.title('Поздравляю! Вы выиграли за ' + str(int(time.time() - playTime)) + ' сек')  # Отобразить сообщение о победе
        winner(0, 0)  # Вызвать функцию winner для завершения игры и отображения анимации победы



def newGame():  # Начать новую игру
    global xBtn, yBtn, mines, nMoves, mrk
    nMoves = 0
    mrk = 0
    input_field.clear()
    if len(btn) != 0:
        for i in range(0, xBtn):
            for j in range(0, yBtn):
                btn[i][j].destroy()
        btn.clear()
    playground()
    tk.title('Осторожно! Вокруг ' + str(mines - mrk) + ' Мин(ы)!!!!')

def set5x5():  # Установить размер поля 5x5
    global xBtn, yBtn,mines,input_field
    input_field = [[0 for _ in range(5)] for _ in range(5)]

    xBtn = 5
    yBtn = 5
    file_of_examples = open('prolog_minesweeper/query_5.pl', 'r')
    examples = file_of_examples.read().split('.')
    random_example = random.randint(0, len(examples) - 1)
    prolog = Prolog()
    prolog.consult("prolog_minesweeper/minesweeper.pl")

    for solution in prolog.query(examples[random_example]):
        input_field = solution["X"]

    for x in range(0, xBtn):
        for y in range(0, yBtn):
            # Проверка, является ли ячейка миной
            if input_field[x][y] == '*':
                mines += 1
    newGame()

def set8x8():  # Установить размер поля 8x8
    global xBtn, yBtn, mines, input_field
    xBtn = 8
    yBtn = 8
    file_of_examples = open('prolog_minesweeper/query_8.pl', 'r')
    examples = file_of_examples.read().split('.')
    random_example = random.randint(0, len(examples) - 1)
    prolog = Prolog()
    prolog.consult("prolog/minesweeper.pl")

    for solution in prolog.query(examples[random_example]):
        input_field = solution["X"]

    for x in range(0, xBtn):
        for y in range(0, yBtn):
            # Проверка, является ли ячейка миной
            if input_field[x][y] == '*':
                mines += 1
    newGame()

def set16x16():  # Установить размер поля 16x16
    global xBtn, yBtn, mines, input_field
    xBtn = 16
    yBtn = 16
    file_of_examples = open('prolog_minesweeper/query_16.pl', 'r')
    examples = file_of_examples.read().split('.')
    random_example = random.randint(0, len(examples) - 1)
    prolog = Prolog()
    prolog.consult("prolog/minesweeper.pl")

    for solution in prolog.query(examples[random_example]):
        input_field = solution["X"]

    for x in range(0, xBtn):
        for y in range(0, yBtn):
            # Проверка, является ли ячейка миной
            if input_field[x][y] == '*':
                mines += 1
    newGame()

def playground():  # Создать игровое поле
    global xBtn, yBtn

    # Создание и размещение кнопок на графическом интерфейсе
    for i in range(yBtn):
        for j in range(xBtn):
            btn[i][j] = tk.Button(tk, text=' ', font=('mono', 16, 'bold'), width=1, height=1, padx=0, pady=0)
            btn[i][j].grid(row=i, column=j)

    # Изменение размера шрифта, если общее количество кнопок больше 256
    for i in range(0, xBtn):
        for j in range(0, yBtn):
            if xBtn * yBtn > 256:
                btn[i][j].config(font=('mono', 8, 'normal'))

            # Назначение функции play(i, j) на кнопку для обработки кликов
            btn[i][j].config(command=play(i, j))

            # Привязка функции marker(n, j) к правой кнопке мыши (Button-3)
            btn[i][j].bind('<Button-3>', lambda event, n=i: marker(n, j))

            # Настройка параметров и отображение кнопки
            btn[i][j].pack(side=LEFT, expand=YES, fill=BOTH, padx=0, pady=0)
            btn[i][j].update()


frmTop = Frame()  # Создаем верхний фрейм для кнопок "New game"
frmTop.pack(expand=YES, fill=BOTH)
Label(frmTop, text=' Новая игра:  ').pack(side=LEFT, expand=NO, fill=X, anchor=N)
Button(frmTop, text='5x5', font=(16), command=set5x5).pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='8x8', font=(16), command=set8x8).pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='16x16', font=(16), command=set16x16).pack(side=LEFT, expand=YES, fill=X, anchor=N)
mainloop()

