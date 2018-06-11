from tkinter import *
from tkinter import messagebox as mb
from random import shuffle
import State as pst
from time import sleep, time

global_user_moves = 0
global_pc_moves = -1


class Board():
    def __init__(self, parent, is_pc, values):
        self.parent = parent
        self.is_pc = is_pc
        self.values = values
        self.moves = -1
        self.start = time()
        self.pc_time = 0
        # noinspection PyBroadException
        try:
            self.puzzle = pst.State(values)
        except Exception:
            pass
        title = "   PC   " if is_pc else "  USER  "
        self.frame = LabelFrame(self.parent, borderwidth=2, relief="solid", text=title)

    def pack(self):
        right_side = "right" if self.is_pc else "left"
        self.frame.pack(side=right_side, expand=True, fill="both")

    def restart_with(self, values, force=False):
        if not self.has_started() and not force:
            return
        # self.moves = 0
        # self.start = time()
        if force:
            global global_user_moves
            if global_user_moves > 0 and not self.is_solved():
                mb.showinfo("Give up!", "So you gave up, huh?")
            global_user_moves = 0
        self.update_values(values)

    def update_values(self, values):
        self.values = values
        self.puzzle = pst.State(values)
        self.update_values_in_ui(values)

    def update_values_in_ui(self, values=[]):
        mult = 0
        for row in range(3):
            current_row = []
            for column in range(3):
                right_index = column + (mult * 3)

                num = 0
                # noinspection PyBroadException
                try:
                    num = values[right_index]
                except Exception:
                    num = 0

                right_text = str(num) if num > 0 else " "

                label = Label(self.frame, text=right_text, borderwidth=1, relief="groove", width=2,
                              justify='center')
                label.grid(row=row, column=column, sticky="nsew")
                current_row.append(label)
                if (column + 1) % 3 == 0:
                    mult += 1
            self.frame.grid_columnconfigure(row, weight=1)
            self.frame.grid_rowconfigure(row, weight=1)

    def move(self, key):
        # noinspection PyBroadException
        try:
            moved, state = self.puzzle.move(key)
            if moved:
                if self.moves == 0:
                    self.start = time()
                if not self.is_pc:
                    self.moves += 1
                    global global_user_moves
                    global_user_moves += 1
                self.update_values(state.to_array())
                self.check_if_solved()
        except Exception:
            pass

    # noinspection PyBroadException
    def has_started(self):
        try:
            return len(self.puzzle.to_array()) > 0
        except Exception:
            return False

    def is_solved(self):
        if self.is_pc:
            return self.has_started() and self.moves > 0
        else:
            return self.has_started() and self.puzzle.is_solved()

    def check_if_solved(self):
        if self.is_solved():
            winner = "You are" if global_user_moves <= global_pc_moves else "PC is"
            right_time = time() - self.start if not self.is_pc else self.pc_time
            title = "PC Solved it!" if self.is_pc else "You solved it!"
            if self.is_pc:
                mb.showinfo(title, "In %.3f seconds and %d movements." % (right_time, self.moves))
            else:
                if global_pc_moves < 0:
                    winner = "You are"
                mb.showinfo(title, "In %.3f seconds and %d movements.\n%s the winner" % (
                right_time, self.moves, winner))
        else:
            if self.is_pc:
                mb.showinfo("Error", "The PC could not solve the puzzle. Can you?")

    def update_from_solution(self, values, i):
        if i < len(values):
            self.update_values(values[i])
            self.parent.after(500, lambda: self.update_from_solution(values, i + 1))

    def solve(self):
        if not self.has_started():
            return
        if self.is_pc:
            if self.is_solved():
                self.check_if_solved()
            else:
                mb.showinfo("Working", "Please kindly wait for PC to solve the Puzzle")
                self.moves, self.pc_time, solved = self.puzzle.solve(False)
                global global_pc_moves
                global_pc_moves = self.moves if self.moves > 0 else 111111
                if self.moves > 0:
                    self.update_from_solution(solved, 0)
                self.check_if_solved()


class Window():
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Puzzle - Jahir Fiquitiva - 201521721')
        self.parent.geometry("400x200")
        self.parent.resizable(0, 0)
        self.values = []
        self.bind_keys_to(parent)
        self.init_ui()
        self.init_menu()

    def move_up(self, event):
        self.parent.after(10, lambda: self.user_panel.move(pst.UP_KEY))

    def move_down(self, event):
        self.parent.after(10, lambda: self.user_panel.move(pst.DOWN_KEY))

    def move_left(self, event):
        self.parent.after(10, lambda: self.user_panel.move(pst.LEFT_KEY))

    def move_right(self, event):
        self.parent.after(10, lambda: self.user_panel.move(pst.RIGHT_KEY))

    def bind_keys_to(self, to):
        to.bind('<Up>', self.move_up)
        to.bind('<w>', self.move_up)
        to.bind('<W>', self.move_up)

        to.bind('<Down>', self.move_down)
        to.bind('<s>', self.move_down)
        to.bind('<S>', self.move_down)

        to.bind('<Left>', self.move_left)
        to.bind('<a>', self.move_left)
        to.bind('<A>', self.move_left)

        to.bind('<Right>', self.move_right)
        to.bind('<d>', self.move_right)
        to.bind('<D>', self.move_right)

    def init_ui(self):
        self.user_panel = Board(self.parent, False, self.values)
        self.pc_panel = Board(self.parent, True, self.values)
        self.bind_keys_to(self.user_panel.frame)
        self.user_panel.pack()
        self.pc_panel.pack()
        return

    def init_menu(self):
        menubar = Menu(self.parent)
        menubar.add_command(label="Inicio", command=self.start_game)
        menubar.add_command(label="Reiniciar", command=self.restart_user_game)
        menubar.add_command(label="Solucionar", command=self.pc_panel.solve)
        menubar.add_command(label="Stats", command=self.show_stats)
        menubar.add_command(label="Ayuda", command=self.show_help)
        self.parent.config(menu=menubar)

    def show_stats(self):
        stats = "User moves: " + str(global_user_moves - 1) + ".\nPC moves: " + str(global_pc_moves)
        mb.showinfo("Stats", stats)

    def restart_user_game(self):
        self.user_panel.restart_with(self.values)

    def start_game(self, first_time=False, show_help=False):
        if first_time:
            self.user_panel.update_values_in_ui()
            self.pc_panel.update_values_in_ui()
            if show_help:
                self.parent.after(500, self.show_help)
        else:
            self.start_game(True)
            # initial_values = [4, 1, 3, 0, 5, 7, 6, 2, 8]
            initial_values = list(range(9))
            shuffle(initial_values)
            self.values = initial_values
            self.user_panel.restart_with(initial_values, True)
            self.pc_panel.update_values(initial_values)
            # mb.showinfo("Working", "Please kindly wait for PC to solve the Puzzle")
            # self.parent.after(1000, self.pc_panel.solve)

    def show_help(self):
        mb.showinfo("Normas", "Usa las flechas o las teclas WASD para jugar")


if __name__ == '__main__':
    root = Tk()
    ui = Window(root)
    ui.start_game(True, True)
    root.mainloop()
