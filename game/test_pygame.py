from basegame import BaseGame
# pip install pygame
import pygame as pg


class MyGame(BaseGame):
    def __init__(self):
        super().__init__(500, 500)
        self._rect = pg.Rect(100, 100, 10, 10)

    def redraw(self):
        pg.draw.rect(self.screen, (255, 255, 0), self._rect)

    def oninput(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if pg.K_UP == event.key:
                self._rect.y -= 10
            elif pg.K_DOWN == event.key:
                self._rect.y += 10
            elif pg.K_LEFT == event.key:
                self._rect.x -= 10
            elif pg.K_RIGHT == event.key:
                self._rect.x += 10


def main():
    game = MyGame()
    game.loop()


main()
