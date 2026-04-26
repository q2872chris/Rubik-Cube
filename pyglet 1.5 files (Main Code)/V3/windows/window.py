import pyglet as py
from pyglet.window import key


class window(py.window.Window):
    def __init__(self, *args, exclusive_mouse=True, x=0.0, y=0.95, **kwargs):
        super().__init__(*args, **kwargs)
        # Defining attributes:
        self.exclusive_mouse = exclusive_mouse
        self.keys = key.KeyStateHandler()
        self.frame_rate = 60
        # Initialisation method calls:
        self.set_exclusive_mouse(self.exclusive_mouse)
        self.set_cursor("CURSOR_CROSSHAIR")
        self.screen_recentre(x, y)
        py.clock.schedule_interval(self.update, 1 / self.frame_rate)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case key.ESCAPE:
                self.close()
            case key.K:
                self.mouse_toggle()

    def update(self, dt: float):
        self.push_handlers(self.keys)

    def screen_recentre(self, x: float, y: float):
        """x,y in [-1,1]"""
        x_middle = (self.screen.width - self.width) / 2
        y_middle = (self.screen.height - self.height) / 2
        x_scaled = int(x_middle * (x + 1))
        y_scaled = int(y_middle * (0.96 - y * 0.8))
        self.set_location(x_scaled, y_scaled)

    def set_cursor(self, cursor_str="CURSOR_DEFAULT"):
        cursor_id = getattr(self, cursor_str, self.CURSOR_DEFAULT)
        cursor = self.get_system_mouse_cursor(cursor_id)
        self.set_mouse_cursor(cursor)

    def mouse_toggle(self):
        self.exclusive_mouse = not self.exclusive_mouse
        self.set_exclusive_mouse(self.exclusive_mouse)



if __name__ == "__main__":
    window(width=600, height=400, caption="window test",
           exclusive_mouse=False)
    py.app.run()






