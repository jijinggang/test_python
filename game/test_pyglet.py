from calendar import c
import pyglet
from pyglet import shapes
from pyglet.window import key
from pyglet import gui
from regex import P

win = pyglet.window.Window()
keys = key.KeyStateHandler()
win.push_handlers(keys)
label = pyglet.text.Label('Hello, world',
                        font_name='Times New Roman',
                        font_size=36,
                        x=win.width//2, y=win.height//2,
                        anchor_x='center', anchor_y='center')

circle = shapes.Circle(x=100, y=150, radius=100, color=(50, 225, 30))
square = shapes.Rectangle(x=200, y=200, width=200, height=200, color=(55, 55, 255))

@win.event
def on_draw():
    update()
    win.clear()

    circle.draw()
    label.draw()

    square.draw()
    #button.draw()

def update():
    if  keys[key.LEFT]:
        circle.x -= 10
    elif keys[key.RIGHT]:
        circle.x += 10

pyglet.app.run()

