import tkinter as tk
from tkinter import messagebox

PAWN_SIZE = 40
PAWN_PLACE_SIZE = 40
RESULT_SIZE = 40
ROW_SPACE = 2
COL_SPACE = 0
DELTA = 3
COLORS = ("blue", "red", "green", "yellow", "orange", "purple")


def do_about():
    messagebox.showinfo("About", "Enjoy !\n\nPascal Toutain - 2022")


class MasterMindBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Master Mind")
        self._game = game
        self._create_menu()
        self._played_cells = {}
        self._secret_code_cells = {}
        self._result_cells = {}
        self._create_board()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play again", command=self.reset_board)
        file_menu.add_command(label="About", command=do_about)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=quit)
        menu_bar.add_cascade(label="Menu", menu=file_menu)

    def _create_board(self):
        # graphic frame to display text
        frm_text = tk.Frame(self)
        frm_text.pack(padx=10, pady=10)
        self.display = tk.Label(frm_text, text="Round {}".format(self._game.round+1))
        self.display.pack()

        # graphic frame to show the result of the secret code
        frm_secret_code = tk.Frame(self)
        frm_secret_code.pack(fill=tk.X, padx=10, pady=10)

        # hidden color pawns for the secret code
        for col in range(self._game.nb_digits):
            cnv = tk.Canvas(master=frm_secret_code, width=40, height=40)
            cnv.create_oval([PAWN_SIZE-DELTA, PAWN_SIZE-DELTA, DELTA, DELTA],
                            fill="black", outline='black', width=1, tags="oval")
            cnv.grid(row=0, column=col, padx=COL_SPACE, pady=ROW_SPACE)
            self._secret_code_cells[cnv] = (0, col)

        # graphic frame for the color pawns played
        frm_pawns = tk.Frame(self)
        frm_pawns.pack(side=tk.LEFT, padx=10, pady=10)

        # graphic frame for the back and whites results
        frm_result = tk.Frame(self)
        frm_result.pack(side=tk.LEFT, padx=10, pady=10)

        # Each row is the color pawns for each round
        for row in range(self._game.max_round):

            # Each column is a color pawn which can be played
            for col in range(self._game.nb_digits):
                cnv = tk.Canvas(master=frm_pawns, width=PAWN_PLACE_SIZE, height=PAWN_PLACE_SIZE)
                if row == self._game.max_round - 1:
                    cnv.create_oval([DELTA, DELTA, PAWN_SIZE-DELTA, PAWN_SIZE-DELTA],
                                    fill="grey", outline='black', width=1, tags="oval")
                cnv.grid(row=row, column=col, padx=COL_SPACE, pady=ROW_SPACE)
                cnv.bind("<Button-1>", self.play)
                self._played_cells[cnv] = (row, col)

            # Rectangle to put the result (black and white _pawns)
            cnv = tk.Canvas(master=frm_result, width=RESULT_SIZE, height=RESULT_SIZE)
            cnv.grid(row=row, column=0, padx=COL_SPACE, pady=ROW_SPACE)
            cnv.bind("<Button-1>", self.show_result)
            self._result_cells[cnv] = (row, 0)

    def show_result(self, event):
        """Handle the result asked, means giving the number of blacks and whites"""
        if not self._game.found or not self._game.loose:

            # getting the result canvas and is coordinates
            clicked_cnv = event.widget
            row, col = self._result_cells[clicked_cnv]

            # if it's the row of the current round and all the colors are filled, then we can evaluate
            if row == self.current_row() and not (-1 in self._game.code_played[self._game.round]):
                self._game.evaluate()

                clicked_cnv.create_rectangle([0, 0, RESULT_SIZE, RESULT_SIZE],
                                             fill="grey", outline='grey', width=1, tags="rect")

                # init coordinates for the blacks and the whites
                result_coord = [[0, 0, RESULT_SIZE/2, RESULT_SIZE/2],
                                [RESULT_SIZE/2, 0, RESULT_SIZE, RESULT_SIZE/2],
                                [0, RESULT_SIZE/2, RESULT_SIZE/2, RESULT_SIZE],
                                [RESULT_SIZE / 2, RESULT_SIZE / 2, RESULT_SIZE, RESULT_SIZE]]

                # crd is incremented for each black and white
                crd = 0

                # display the blacks
                for i in range(self._game.nb_right_places):
                    clicked_cnv.create_rectangle(result_coord[crd],
                                                 fill="black", outline='dark grey', width=1, tags="rect")
                    crd += 1

                # display the whites
                for i in range(self._game.nb_right_places, self._game.nb_wrong_places + self._game.nb_right_places):
                    clicked_cnv.create_rectangle(result_coord[crd],
                                                 fill="white", outline='dark grey', width=1, tags="rect")
                    crd += 1

            if self._game.found or self._game.loose:
                if self._game.found:
                    self.display["text"] = "You have found in {} round{}".format(self._game.round,
                                                                                 's' if self._game.round > 1 else'')
                else:
                    self.display["text"] = "Sorry ! Try again !"

                # if the secret code is found then the secret code is shown
                i = 0
                for cnv in self._secret_code_cells.keys():
                    cnv.create_oval([PAWN_SIZE - DELTA, PAWN_SIZE - DELTA, DELTA, DELTA],
                                    fill=COLORS[self._game.secret_code[i]], outline='black',
                                    width=1, tag="oval")
                    i += 1

            # it's not finish and the player haven't found the secret code yet
            else:
                self.display["text"] = "Round {}".format(self._game.round+1)
                for cnv in self._played_cells.keys():
                    if self._played_cells[cnv][0] == self.current_row():
                        cnv.create_oval([DELTA, DELTA, PAWN_SIZE - DELTA, PAWN_SIZE - DELTA],
                                        fill="grey", outline='black', width=1, tags="oval")

    def play(self, event):
        """Handle the color choice"""
        if not self._game.found or not self._game.loose:

            clicked_cnv = event.widget
            row, col = self._played_cells[clicked_cnv]
            if row == self.current_row():
                if self._game.code_played[self._game.round][col] >= 0:
                    value = (self._game.code_played[self._game.round][col] + 1) % self._game.nb_colors
                    self._game.play_a_color(col, value)
                    clicked_cnv.create_oval([DELTA, DELTA, PAWN_SIZE - DELTA, PAWN_SIZE - DELTA],
                                            fill=COLORS[value], outline='black', width=1, tags="oval")
                else:
                    self._game.play_a_color(col, 0)
                    clicked_cnv.create_oval([DELTA, DELTA, PAWN_SIZE - DELTA, PAWN_SIZE - DELTA],
                                            fill=COLORS[0], outline='black', width=1, tags="oval")
            if -1 in self._game.code_played[self._game.round]:
                return
            for cnv in self._result_cells.keys():
                if self._result_cells[cnv][0] == self.current_row():
                    cnv.create_rectangle([0, 0, RESULT_SIZE, RESULT_SIZE],
                                         fill="grey", outline='black', width=1, tags="rect")

    def current_row(self):
        """the game's rounds start from 0 but the graphic rows start from max_round, is the inverse !"""
        return self._game.max_round - self._game.round - 1

    def reset_board(self):
        self._game.reset_game()

        # deleting the results box
        for cnv in self._result_cells.keys():
            cnv.delete("rect")

        # deleting all the colors played and init the first raw
        for cnv in self._played_cells.keys():
            cnv.delete("oval")
            if self._played_cells[cnv][0] == self._game.max_round - 1:
                cnv.create_oval([DELTA, DELTA, PAWN_SIZE - DELTA, PAWN_SIZE - DELTA],
                                fill="grey", outline='black', width=1, tags="oval")

        # deleting and hiding the secret code
        for cnv in self._secret_code_cells.keys():
            cnv.delete("oval")
            cnv.create_oval([PAWN_SIZE - DELTA, PAWN_SIZE - DELTA, DELTA, DELTA],
                            fill="black", outline='black', width=1, tags="oval")

        self.display["text"] = "Round {}".format(self._game.round + 1)

