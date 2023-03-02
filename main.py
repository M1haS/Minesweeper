import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror
# Made by Michail Daskalu
colors = {
    0: "blue",
    1: "blue",
    2: "green",
    3: "#b2162d",
    4: "#96008e",
    5: "#057e7c",
    6: "#361101",
    7: "#b12ca9",
    8: "#857bd1"
}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, font="Calibri 15 bold", *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_mine = 0
        self.is_open = False


    def __repr__(self):
        return f'MyButton ({self.x}, {self.y}) {self.number} {self.is_mine}'


class Saper:
    window = tk.Tk()
    window.title("Сапер")
    ROW = 10
    COLUMNS = 7
    MINES = 15
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):

        self.buttons = []
        for i in range(self.ROW + 2):
            temp = []
            for j in range(self.COLUMNS + 2):
                btn = MyButton(self.window, x=i, y=j, width=3)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", lambda event, button=btn: self.right_click(event, button))
                temp.append(btn)
            self.buttons.append(temp)

        self.mines_fake = self.MINES
        self.timer = tk.Label(self.window, text="Время: 0 : 0 : 0", font="calibri 12", pady=13)
        self.second = 0
        self.minute = 0
        self.hour = 0
        self.stop_timer = False
        self.user_flags = []

    def right_click(self, event: tk.Event, button: MyButton):

        if self.IS_GAME_OVER:
            return
        if not self.IS_FIRST_CLICK:
            cur_btn = event.widget
            if self.mines_fake > 0:
                if cur_btn["state"] == "normal":
                    cur_btn["state"] = "disabled"
                    cur_btn["text"] = '🚩'
                    cur_btn["disabledforeground"] = "red"
                    self.mines_fake -= 1
                    self.user_flags.append(button.number)
                elif cur_btn["text"] == '🚩':
                    cur_btn["text"] = ' '
                    cur_btn["state"] = "normal"
                    self.mines_fake += 1
                    self.user_flags.pop()
                self.mines.configure(text=f"Осталось мин: {self.mines_fake}")

            elif self.mines_fake == 0:
                if cur_btn["text"] == '🚩':
                    cur_btn["text"] = ' '
                    cur_btn["state"] = "normal"
                    self.mines_fake += 1
                    self.user_flags.pop()
                self.mines.configure(text=f"Осталось мин: {self.mines_fake}")

        true_answers = []
        for i in self.index_mines:
            if i in self.user_flags:
                true_answers.append(i)

        print(len(true_answers))
        if len(true_answers) == self.MINES:
            self.IS_GAME_OVER = True
            self.stop_timer = True
            showinfo("Победа", "Вы выйграли!")

    def click(self, clicked_button: MyButton):
        if self.IS_GAME_OVER:
            return
        clicked_button = clicked_button
        if self.IS_FIRST_CLICK:
            self.incert_mines(clicked_button.number)
            self.count_mines_and_buttons()
            self.print_btn()
            self.IS_FIRST_CLICK = False
            self.update_clock()
        self.mines.configure(text=f"Осталось мин: {self.mines_fake}")

        print(clicked_button)
        if clicked_button.is_mine:
            self.stop_timer = True
            clicked_button.config(text="*", background="red", disabledforeground="black")
            clicked_button.is_open = True
            self.IS_GAME_OVER = True
            showinfo("Game Over", "Вы проиграли!")
            for i in range(1, self.ROW + 1):
                for j in range(1, self.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn["text"] = "*"
        else:
            color = colors.get(clicked_button.count_mine, "black")
            if clicked_button.count_mine:
                clicked_button.config(text=clicked_button.count_mine, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state="disabled")
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_mine, "black")
            if cur_btn.count_mine:
                cur_btn.config(text=cur_btn.count_mine, disabledforeground=color)
            else:
                cur_btn.config(text=" ", disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state="disabled")
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_mine == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1:
                        #     continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= self.ROW and \
                                1 <= next_btn.y <= self.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        self.IS_FIRST_CLICK = True
        self.IS_GAME_OVER = False

    def settings_window(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title("Настройки")

        tk.Label(win_settings, text="Колличество строк").grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, self.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(win_settings, text="Колличество столбцов").grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, self.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)

        tk.Label(win_settings, text="Колличество мин").grid(row=2, column=0)
        mins_entry = tk.Entry(win_settings)
        mins_entry.insert(0, self.MINES)
        mins_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = tk.Button(win_settings, text="Применить",
                             command=lambda: self.change_settings(row_entry, column_entry, mins_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror("Ошибка", "вы ввели неправельное значение!")
            return
        self.ROW = int(row.get())
        self.COLUMNS = int(column.get())
        self.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=False)
        settings_menu.add_command(label="Играть", command=self.reload)
        settings_menu.add_command(label="Настройки", command=self.settings_window)
        settings_menu.add_command(label="Выход", command=self.window.destroy)
        menubar.add_cascade(label="Файл", menu=settings_menu)

        count = 1
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick="NWES")
                count += 1

        for i in range(1, self.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(1, self.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

        self.timer.grid(column=1, columnspan=3)

        self.mines = tk.Label(self.window, text=f"Осталось мин: 0", font="calibri 12")
        self.mines.grid(column=self.COLUMNS // 2 + 2, row=self.ROW + 1, columnspan=3)

    def update_clock(self):
        if self.second != 60:
            self.second += 1
        elif self.minute != 60:
            self.minute += 1
            self.second = 0
        else:
            self.hour += 1
            self.minute = 0
            self.second = 0
        
        if not self.stop_timer:
            self.timer.configure(text="Время: " + str(self.hour) + " : " + str(self.minute) + " : " + str(self.second))
            self.timer.after(1000, self.update_clock)
        else:
            return

    def open_all_buttons(self):
        for i in range(self.ROW + 2):
            for j in range(self.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background="red", disabledforeground="black")
                else:
                    color = colors.get(btn.count_mine, "black")
                    btn.config(text=btn.count_mine, fg=color)

    def start(self):
        self.create_widgets()
        # self.open_all_buttons()
        self.window.mainloop()

    def print_btn(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("M", end=" ")
                else:
                    print(btn.count_mine, end=" ")
            print()

    def incert_mines(self, number: int):
        index_mines = self.get_mine_place(number)
        print(index_mines)
        self.index_mines = index_mines

        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]

                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_and_buttons(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_mine = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_mine += 1
                btn.count_mine = count_mine

    def get_mine_place(self, exclude_number: int):
        indexes = list(range(1, self.COLUMNS * self.ROW + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:self.MINES]


if __name__ == "__main__":
    game = Saper()
    game.start()
