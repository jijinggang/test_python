from pywebio import start_server
from pywebio.output import *
from pywebio.input import *
from pywebio.pin import *


def page():
    def refresh():
        with use_scope('res', clear=True):
            area = pin.w * pin.h
            print(area)
            put_text(f"area = {area}")
    put_input('w', type='number',label="width:", value=0)
    put_input('h', type='number', label="height",value=0)


    while True:
        changed = pin_wait_change('w', 'h')
        refresh()

        #put_button('submit', refresh)
def main():
    start_server(page,port=8080, auto_open_webbrowser=True)
if __name__ == '__main__':
    page()