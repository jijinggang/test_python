import pyxel as xel
from enum import Enum


class Game:
    def __init__(self):
        self.screen = (200, 200)
        self.grid = 10
        self.grid_count = 19
        self.zero = ((self.screen[0]-self.grid*18)/2,
                     (self.screen[1]-self.grid*18)/2)
        self.data = [[0 for i in range(19)] for j in range(19)]
        self.isWhite = True
        self.win = 0
        xel.init(self.screen[0], self.screen[1],
                 caption="五子棋", fullscreen=True)
        xel.mouse(True)
        xel.run(self.update, self.draw)

    def update(self):
        if self.win != 0:
            return
        if xel.btnp(xel.MOUSE_LEFT_BUTTON):
            if ij := self.getgrid(xel.mouse_x, xel.mouse_y):
                i = ij[0]
                j = ij[1]
                if self.data[i][j] == 0:
                    if self.isWhite:
                        self.data[i][j] = 1
                    else:
                        self.data[i][j] = 2
                    if self.check_win(i, j):
                        self.win = 1 if self.isWhite else 2
                        return
                    self.isWhite = not self.isWhite

    def getpos(self, i, j):
        return self.zero[0]+i*self.grid, self.zero[1]+j*self.grid

    def getgrid(self, x, y):
        i = int((x-self.zero[0]) / self.grid + 0.5)
        j = int((y-self.zero[1]) / self.grid + 0.5)
        if(0 <= i <= 18 and 0 <= j <= 18):
            return (i, j)
        else:
            return None

    def check_win(self, i, j):
        l1 = [(i+diff, j) for diff in range(-4, 4)]
        l2 = [(i, j+diff) for diff in range(-4, 4)]
        l3 = [(i+diff, j+diff) for diff in range(-4, 4)]
        l4 = [(i+diff, j-diff) for diff in range(-4, 4)]
        for line in [l1, l2, l3, l4]:
            if self._check_win_line(line, self.data[i][j]):
                return True
        return False

    def _check_win_line(self, line, val):
        count = 0
        for (i, j) in line:
            if(self.data[i][j] == val):
                count += 1
                if(count == 5):
                    return True
            else:
                count = 0
        return False

    def draw(self):
        xel.cls(xel.COLOR_GREEN)
        self.draw_board()
        self.draw_stones()

    def draw_board(self):
        # 画横棋盘
        for i in range(19):
            xel.line(self.zero[0], self.zero[1]+i*self.grid, self.zero[0] +
                     (18)*self.grid, self.zero[1]+i*self.grid, xel.COLOR_BLACK)
        # 画竖棋盘
        for i in range(19):
            xel.line(self.zero[0]+i*self.grid, self.zero[1],
                     self.zero[0]+i*self.grid, self.zero[1]+18*self.grid, xel.COLOR_BLACK)

        if self.win != 0:
            if self.win == 1:
                xel.text(80, 50, "White Win!!!", xel.COLOR_RED)
            elif self.win == 2:
                xel.text(80, 50, "Black Win!!!", xel.COLOR_RED)

    def draw_stones(self):
        for i in range(19):
            for j in range(19):
                v = self.data[i][j]
                x, y = self.getpos(i, j)
                if v == 1:
                    xel.circ(x, y, 2, xel.COLOR_WHITE)
                elif v == 2:
                    xel.circ(x, y, 2, xel.COLOR_BLACK)


Game()
