import tkinter as tk

def on_cell_click(x, y):
    # Здесь должна быть логика обработки щелчка на клетке
    pass

# Создание окна
root = tk.Tk()
root.title("Сапер")

# Создание игрового поля
width, height, num_mines = 10, 10, 10  # Установите нужные значения
cell_size = 30

canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
canvas.pack()

for x in range(width):
    for y in range(height):
        canvas.create_rectangle(
            x * cell_size,
            y * cell_size,
            (x + 1) * cell_size,
            (y + 1) * cell_size,
            fill="gray", outline="black"
        )
        canvas.tag_bind(
            f"{x}_{y}",
            "<Button-1>",
            lambda event, x=x, y=y: on_cell_click(x, y)
        )

# Запуск игры
# Здесь вы можете вызвать функцию start_game() с передачей нужных параметров

root.mainloop()
