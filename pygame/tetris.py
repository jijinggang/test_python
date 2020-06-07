import enum
import pyxel as px
import random
import copy
import time
BOXS: [list] = [
    #  *O**
    [(0, 0), (-1, 0), (1, 0), (2, 0)],

    #   O*
    #   **
    [(0, 0), (1, 0), (1, 1), (0, 1)],

    #  *O*
    #  *
    [(0, 0), (-1, 0), (1, 0), (-1, 1)],

    #  *O*
    #    *
    [(0, 0), (-1, 0), (1, 0), (1, 1)],

    #  O*
    # **
    [(0, 0), (1, 0), (0, 1), (-1, 1)],
    #  *O
    #   **
    [(0, 0), (-1, 0), (0, 1), (1, 1)],

    #  *O*
    #   *
    [(0, 0), (-1, 0), (1, 0), (0, 1)]
]


class Box:
    def __init__(self, offset_x=0, offset_y=0):
        self._data = random.choice(BOXS).copy()  # 各方块相对起始点(第一个方块)的位置
        # 移动后的起始点(第一个方块)的偏移
        self._x = offset_x
        self._y = offset_y

    def rotate(self):
        new_data = []
        for x, y in self._data:
            new_data.append((-y, x))
        self._data = new_data

    def move(self, diff_x, diff_y):
        self._x += diff_x
        self._y += diff_y

    def data(self):
        if self._x == 0 and self._y == 0:
            return self._data
        new_data = []
        for x, y in self._data:
            new_data.append((x+self._x, y+self._y))
        return new_data


# 记录当前游戏状态
class State(enum.Enum):
    NORMAL = 0  # 正常下落
    ERASING = 1  # 消除满行
    END = 2  # 失败


class Tetris:

    def __init__(self, w, h):
        self.init_data(w, h)
        px.init(w, h, caption="俄罗斯方块", fullscreen=True)

        px.run(self.update, self.draw)

    def init_data(self, w: int, h: int):

        self.cx = 10  # 水平方向格子数
        self.cy = 15  # 垂直方向格子数
        self.GRID = 8  # 格子大小

        # 格子区左上角位置
        self.left = (w*3//4 - self.cx*self.GRID) // 2
        self.top = (h-self.cy*self.GRID)//2

        # 桌面上的方块数据,未填充为False,填充为True
        self.data = [[False for j in range(self.cy)]
                     for i in range(self.cx)]
        self.state: State = State.NORMAL  # 是否失败
        self.curr_box: Box = None
        self.next_box: Box = None
        self.speed = 2  # 基础速度,每秒下落几次
        self.speedRate = 1  # 加速系数
        self.lastTime = 0
        self.score = 0

    def update(self):
        if self.state == State.END:
            return
        elif self.state == State.NORMAL:
            if self.curr_box:
                self.check_key()
                self.check_time()
            else:
                if self.next_box:
                    self.curr_box = self.next_box
                else:
                    self.curr_box = Box((self.cx-1)//2, 0)
                self.next_box = Box((self.cx-1)//2, 0)
        elif self.state == State.ERASING:
            pass

    # 判读方块跟当前盘面冲突
    def judge_conflict(self, box: Box):
        data = box.data()
        for i, j in data:
            if i < 0 or i >= self.cx or j < 0 or j >= self.cy or self.data[i][j]:
                return True
        return False

    # 对按键做出响应
    def check_key(self):
        if px.btnp(px.KEY_UP):
            box = copy.copy(self.curr_box)
            box.rotate()
            if not self.judge_conflict(box):
                self.curr_box.rotate()
        elif px.btn(px.KEY_LEFT):
            self._check_and_move(-1, 0)
        elif px.btn(px.KEY_RIGHT):
            self._check_and_move(1, 0)
        if px.btn(px.KEY_DOWN):
            self.speedRate = 10
        else:
            self.speedRate = 1

    # 定时向下移动
    def check_time(self):
        # 获取某个格子对应的左上角坐标
        time_span = 1/(self.speed*self.speedRate)
        curr_time = time.time()
        if(curr_time-self.lastTime) < time_span:
            return
        self.lastTime = curr_time
        if not self._check_and_move(0, 1):
            # 冻结当前正下落的方块
            for i, j in self.curr_box.data():
                if(self.data[i][j]):
                    # 失败
                    self.state = State.END
                    return
                self.data[i][j] = True
            self.erase_full()
            self.curr_box = None

    # 消掉一行
    def _erase_line(self, line):
        for j in range(line, 1, -1):
            for i in range(self.cx):
                self.data[i][j] = self.data[i][j-1]

    # 根据当前下落方块消掉所有满行
    def erase_full(self):
        lines = set()
        for _, j in self.curr_box.data():
            if j in lines:
                continue
            isFull = all([self.data[i][j] for i in range(self.cx)])
            if(isFull):
                lines.add(j)
        count = len(lines)
        for j in lines:
            self._erase_line(j)
            # 计算积分
        SCORE = {1: 100, 2: 300, 3: 700, 4: 1500}

        if(count > 0):
            self.score += SCORE[count]

    # 判断并实际移动

    def _check_and_move(self, offset_i, offset_j):
        box = copy.copy(self.curr_box)
        box.move(offset_i, offset_j)
        if not self.judge_conflict(box):
            self.curr_box.move(offset_i, offset_j)
            return True
        else:
            return False

    def getpos(self, i, j):
        return self.left+i*self.GRID, self.top+j*self.GRID

    def draw(self):
        px.cls(px.COLOR_BLACK)
        self.draw_blocks()
        self.draw_curr_box()
        self.draw_sep_lines()
        self.draw_score()
        self.draw_next_box()

    # 画单个方格
    def draw_block(self, x, y, is_fill):
        if is_fill:
            px.rect(x, y, self.GRID, self.GRID, px.COLOR_WHITE)
        else:
            px.rect(x, y, self.GRID, self.GRID, px.COLOR_BLACK)

    # 根据盘面各个格子是否填充花不同颜色
    def draw_blocks(self):
        for i in range(self.cx):
            for j in range(self.cy):
                x, y = self.getpos(i, j)
                self.draw_block(x, y, self.data[i][j])

    # 画盘面方块间分割线
    def draw_sep_lines(self):
        sep_color = px.COLOR_GREEN
        # 画横隔线
        for i in range(self.cy+1):
            px.line(self.left, self.top+i*self.GRID, self.left +
                    (self.cx)*self.GRID, self.top+i*self.GRID, sep_color)
        # 画竖隔线
        for i in range(self.cx+1):
            px.line(self.left+i*self.GRID, self.top,
                    self.left+i*self.GRID, self.top+(self.cy)*self.GRID, sep_color)

        if self.state == State.END:
            px.text(80, 50, "You Lost !!!", px.COLOR_RED)

    # 画当前正在下落的方块
    def draw_curr_box(self):
        if not self.curr_box:
            return
        for i, j in self.curr_box.data():
            x, y = self.getpos(i, j)
            self.draw_block(x, y, True)

    # 画积分
    def draw_score(self):
        px.text(150, 70, f"Score:{self.score}", px.COLOR_RED)

    # 画下一个方块
    def draw_next_box(self):
        if not self.next_box:
            return
        for i, j in self.next_box.data():
            self.draw_block(140 + i*self.GRID, 20+j*self.GRID, True)


Tetris(240, 135)
