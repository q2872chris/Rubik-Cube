import pyglet as py
from pyglet.window import key


class window(py.window.Window):
    def __init__(self, *args, exclusive_mouse=True, **kwargs):
        super().__init__(*args, **kwargs)
        # defining attributes:
        self.exclusive_mouse = exclusive_mouse
        self.keys = key.KeyStateHandler()
        self.title_screen_flag = False
        # initialisation method calls:
        self.mouse_toggle(toggle=False)
        self.set_cursor("CURSOR_CROSSHAIR")
        self.screen_recentre()
        py.clock.schedule(self.update)
        # self.set_icon(py.resource.image("image_path"))

    def title_screen_flip(self):
        pass

    def on_key_press(self, symbol, modifiers):
        match symbol:
            case key.ESCAPE:
                self.close()
            case key.K:
                self.mouse_toggle()

    def update(self, dt):
        self.push_handlers(self.keys)

    # unfinished, use type hints and take x/y shifting parameters
    def screen_recentre(self):
        x_middle = int((self.screen.width - self.width) // 2)
        y_middle = int((self.screen.height - self.height) // 2)
        x_scaled = x_middle
        y_scaled = y_middle - 160
        self.set_location(x_scaled, y_scaled)

    def set_cursor(self, cursor_str="CURSOR_DEFAULT"):
        cursor_id = getattr(self, cursor_str, self.CURSOR_DEFAULT)
        cursor = self.get_system_mouse_cursor(cursor_id)
        self.set_mouse_cursor(cursor)

    def mouse_toggle(self, toggle=True):
        if toggle:
            self.exclusive_mouse = not self.exclusive_mouse
        self.set_exclusive_mouse(self.exclusive_mouse)


if __name__ == "__main__":
    window(width=600, height=400, caption="Pyglet Rubix Cube 1.2")
    py.app.run()


