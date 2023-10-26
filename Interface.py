import random
from pyswip import Prolog
from tkinter import *
from  random import choice
import time

#сделать везде масиив input_filed


xBtn=16;yBtn=16;
frm = []; btn = []  # Списки с фреймами и кнопками
playTime = 0  # Время игры
imgMark = '\u2661'; imgMine = '\u2665'  # Символ маркера и мины
nMoves = 0; mrk = 0  # Игровое поле, счётчик ходов и маркеров
tk = Tk()
tk.title('Игра Сапер')
tk.geometry(str(44 * xBtn) + 'x' + str(44 * yBtn + 10))

def play(n):  # Обработка нажатия на клетку
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
    if btn[n].cget('text') == imgMark:  # Если поле было промаркировано
        mrk -= 1
        tk.title('Осторожно! Вокруг ' + str(mines - mrk) + ' Мин(ы)!!!!')
    btn[n].config(text=input_field[n], state=DISABLED, bg='white')  # Отображаем игровую ситуацию
    if input_field[n][n] == 0:  # Пустое поле без соседей
        btn[n].config(text=' ', bg='#ccb')
    elif input_field[n][n] == '*':  # Мина
        btn[n].config(text=imgMine)
        if nMoves <= (xBtn * yBtn - mines) or mines >= mrk:  # Если игрок ещё не выиграл, то проиграл
            nMoves = 32000  # Если проиграл, то уже не выиграет
            chainReaction(0)  # Цепная реакция
            tk.title('Вы проиграли :(')
    if nMoves == (xBtn * yBtn - mines) and mines == mrk:  # Если все клетки открыты и мины помечены
        tk.title('Поздравляю! Вы выиграли за ' + str(int(time.time() - playTime)) + ' сек')
        winner(0)
#
def chainReaction(j):  # Цепная реакция
    if j <= len(input_field):  # Если не запустили новую игру
        for i in range(j, xBtn * yBtn):
            if input_field[i] == -1 and btn[i].cget('text') == ' ':
                btn[i].config(text=imgMine)
                btn[i].flash()
                tk.bell()
                tk.after(50, chainReaction, i + 1)
                break

def winner(j):  # Победа
    if j <= len(input_field):  # Если не запустили новую игру
        for i in range(j, xBtn * yBtn):
            if input_field[i] == 0:
                btn[i].config(state=NORMAL, text='☺')
                btn[i].flash()
                tk.bell()
                btn[i].config(text=' ', state=DISABLED)
                tk.after(50, winner, i + 1)
                break

def marker(n):  # Помечаем, где возможно скрывается мина
    global mrk, mines, playTime
    if (btn[n].cget('state')) != 'disabled':
        if btn[n].cget('text') == imgMark:
            btn[n].config(text=' ')
            mrk -= 1
        else:
            btn[n].config(text=imgMark, fg='blue')
            mrk += 1
        tk.title('Осторожно! Вокруг ' + str(mines - mrk) + ' Мин!!!!')
    if nMoves == (xBtn * yBtn - mines) and mines == mrk:  # Если все клетки открыты и мины помечены
        tk.title('Поздравляю! Вы выиграли за ' + str(int(time.time() - playTime)) + ' сек')
        winner(0)


def newGame():  # Начать новую игру
    global xBtn, yBtn, mines, nMoves, mrk
    nMoves = 0
    mrk = 0
    input_field.clear()
    if len(btn) != 0:
        for i in range(0, len(btn)):
            btn[i].destroy()
        btn.clear()
        for i in range(0, len(frm)):
            frm[i].destroy()
        frm.clear()
    playground()
    tk.title('Осторожно! Вокруг ' + str(mines - mrk) + ' Мин(ы)!!!!')

def set5x5():  # Установить размер поля 5x5
    global xBtn, yBtn,mines,input_field
    xBtn = 5
    yBtn = 5
    file_of_examples = open('prolog_minesweeper/query5.pl', 'r')
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

def set8x8():  # Установить размер поля 8x8
    global xBtn, yBtn, mines, input_field
    xBtn = 8
    yBtn = 8
    file_of_examples = open('prolog_minesweeper/query8.pl', 'r')
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
    file_of_examples = open('prolog_minesweeper/query16.pl', 'r')
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
    for i in range(0, yBtn):
        frm.append(Frame())
        frm[i].pack(expand=YES, fill=BOTH)
        for j in range(0, xBtn):
            btn.append(Button(frm[i], text=' ', font=('mono', 16, 'bold'),
                              width=1, height=1, padx=0, pady=0))
    for i in range(0, xBtn * yBtn):
        if xBtn * yBtn > 256:
            btn[i].config(font=('mono', 8, 'normal'))
        btn[i].config(command=lambda n=i: play(n))
        btn[i].bind('<Button-3>', lambda event, n=i: marker(n))
        btn[i].pack(side=LEFT, expand=YES, fill=BOTH, padx=0, pady=0)
        btn[i].update()



frmTop = Frame()  # Создаем верхний фрейм для кнопок "New game"
frmTop.pack(expand=YES, fill=BOTH)
Label(frmTop, text=' Новая игра:  ').pack(side=LEFT, expand=NO, fill=X, anchor=N)
Button(frmTop, text='5x5', font=(16), command=set5x5).pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='8x8', font=(16), command=set8x8).pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='16x16', font=(16), command=set16x16).pack(side=LEFT, expand=YES, fill=X, anchor=N)
mainloop()

