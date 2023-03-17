import pynecone as pc


class State(pc.State):
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

def about():
    return pc.center(pc.heading("About", font_size="2em"))

def index():
    # 加入一个页面头，包含两个链接

    return pc.center(pc.vstack(
        pc.heading("Pynecone", font_size="2em"),
        pc.hstack(
            pc.button(
                "Decrement",
                color_scheme="red",
                border_radius="1em",
                on_click=State.decrement,
            ),
            
            pc.text(State.count, font_size="2em"),
            pc.button(
                "Increment",
                color_scheme="green",
                border_radius="1em",
                on_click=State.increment,
            ),
    )))

app = pc.App(state=State)
app.add_page(index)
app.add_page(about)
app.compile()