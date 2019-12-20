import random
from tkinter import Frame, Label, CENTER

import logic
import constrants as c
import pprint
import numpy as np 

class Game():
    def __init__(self):
        self.grid_cells = []
        self.init_matrix()
        self.score = 0

        self.commands = {0: logic.up, 1: logic.down,
                         2: logic.left, 3: logic.right}

    # trying maximin
    def predict_maximin(self,matrix,depth = 2):
        if depth == 0:
            cur_scores = []
            for i in range(4):
                new_matrix, done, action_score = self.commands[i](matrix)
                a_score = self.singlePredict(new_matrix, done)
            cur_scores.append(a_score + action_score)
            return np.argmax(cur_scores)
        else:
            num_test = 3
            scores = np.array([0,0,0,0])
            depth -= 1
            for i in range(4):
                cur_scores = []
                for j in range(num_test):
                    new_matrix, done, action_score = self.commands[i](matrix)
                    a_score = self.singlePredict(new_matrix, done)
                    recur_score = self.predict_maximin(new_matrix,depth)
                    cur_scores.append(0.6 * a_score + 0.6 * action_score + recur_score)
                # minimum = np.argmin(cur_scores)

                scores[i] = (np.sum(cur_scores)/num_test)
            if max(scores) == 0:
                return np.random.randint(4)
           
            return np.argmax(scores)

    def singlePredict(self, matrix, done):
        maxi_pos = np.argmax(matrix)
        cur_scores = 0
        hor = 0
        ver = 0

        for i in range(3):
            for j in range(3): 
                if(matrix[i][j] == matrix[i+1][j]):
                    hor += matrix[i][j]
                if(matrix[i][j] == matrix[i][j+1]):
                    ver += matrix[i][j]
                if(matrix[i][j] == matrix[i+1][j]/2 or matrix[i][j]/2 == matrix[i+1][j]):
                    hor += min(matrix[i][j], matrix[i+1][j])
                if(matrix[i][j] == matrix[i][j+1]/2 or matrix[i][j]/2 == matrix[i][j+1]):
                    ver += min(matrix[i][j], matrix[i][j+1])
        if(maxi_pos == 0 or maxi_pos == 3 or maxi_pos == 15 or maxi_pos == 12):
            cur_scores += np.amax(matrix)

        if done:
            cur_scores += np.count_nonzero(matrix==0) * np.amax(matrix)/16
        else:
            cur_scores -= 10000

        if logic.game_state(matrix) == 'lose':
            cur_scores -= 100000

        # I think we need to weight this
        cur_scores += max(hor,ver)/5
        return cur_scores

    def init_matrix(self):  
        self.matrix = logic.new_game(4)
        self.history_matrixs = list()
        self.matrix = logic.add_two(self.matrix)
        self.matrix = logic.add_two(self.matrix)

    def play(self, strategy):
        while logic.game_state(self.matrix) == 'not over':
            if strategy == 0:
                key = np.random.randint(4)
            elif strategy == 1:
                key = self.predict_maximin(self.matrix)
            if key in self.commands:
                self.matrix, done, score = self.commands[key](self.matrix)
                self.score += score
                # print(self.score)
                if done:
                    
                    self.matrix = logic.add_two(self.matrix)
                    # record last move
                    self.history_matrixs.append(self.matrix)
                    done = False
                    if logic.game_state(self.matrix) == 'win':
                        print('you win')
                        print(self.score)
                        print(self.matrix)
                    if logic.game_state(self.matrix) == 'lose':
                        print('you lose')
                        print(self.score)
                        print(self.matrix)

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        # self.gamelogic = gamelogic
        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left, c.KEY_RIGHT_ALT: logic.right,
                         c.KEY_H: logic.left, c.KEY_L: logic.right,
                         c.KEY_K: logic.up, c.KEY_J: logic.down}
        
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = logic.new_game(4)
        self.history_matrixs = list()
        self.matrix = logic.add_two(self.matrix)
        self.matrix = logic.add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done,score = self.commands[key](self.matrix)
            print(done)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                done = False
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2


# gamegrid = GameGrid()

game = Game()
game.play(1)
