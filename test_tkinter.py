import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog


class App(tk.Frame):
    def __init__(self):
        # super(master)
        self._root = tk.Tk()
        self._pathVar = tk.StringVar()

    def on_click(self):
        if messagebox.askyesno('确认', '是否打开'):
            path = filedialog.askdirectory()
            print(path)
            self._pathVar.set(path)

    def show(self):
        lines = [
            [
                tk.Label(text="select a path:")
            ],
            [
                tk.Entry(textvariable=self._pathVar, width=50),
                tk.Button(text="OK", width=10, command=self.on_click)
            ]
        ]

        x = 1
        for line in lines:
            y = 1
            for control in line:
                control.grid(row=x, column=y, padx=5, pady=5)
                y += 1
                # control.pack(side='left')
            x += 1
        tk.mainloop()


def main():
    App().show()


if __name__ == '__main__':
    main()
