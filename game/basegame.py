import pygame as pg


class BaseGame:
    def __init__(self, w, h, frame_rate=60):
        pg.init()
        self.screen = pg.display.set_mode((w, h))
        self.tick_span = 1000//frame_rate
        pg.key.set_repeat(self.tick_span)

    def loop(self):
        last_ticks = 0
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                else:
                    self.oninput(event)
            curr_ticks = pg.time.get_ticks()
            delay_tick = self.tick_span - (curr_ticks - last_ticks)
            last_ticks = curr_ticks
            if(delay_tick > 0):
                pg.time.delay(delay_tick)
            self.screen.fill((0, 0, 0))
            self.redraw()
            pg.display.flip()

    def redraw(self):
        pass

    def oninput(self, event: pg.event.Event):
        pass
