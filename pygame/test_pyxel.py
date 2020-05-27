import pyxel as xel


class Game:
    def __init__(self):
        xel.init(160, 120)
        self.offsetX = 0
        self.offsetY = 0
        xel.run(self.update, self.draw)

    def update(self):
        if(xel.btn(xel.KEY_ESCAPE)):
            xel.quit()
        elif (xel.btn(xel.KEY_LEFT)):
            self.offsetX -= 1
        elif (xel.btn(xel.KEY_RIGHT)):
            self.offsetX += 1
        elif (xel.btn(xel.KEY_UP)):
            self.offsetY -= 1
        elif (xel.btn(xel.KEY_DOWN)):
            self.offsetY += 1

    def draw(self):
        xel.cls(xel.COLOR_BLACK)
        xel.rect(self.offsetX, self.offsetY, 10, 10, xel.COLOR_NAVY)
        xel.text(50, 50, "Hello", xel.COLOR_ORANGE)


Game()
