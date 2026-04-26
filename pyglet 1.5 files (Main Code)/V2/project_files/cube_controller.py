from pyglet.window import key
from project_files.objects import rubik_cube_generator
from project_files.cube_utilities import possible_moves_generator, wide
from project_files.general_utilities import extend
from project_files.engine import engine
from project_files.renderer import renderer
from project_files.window import window


class cube_controller(window, renderer):
    def __init__(self, *args, dim=7, **kwargs):
        super().__init__(*args, **kwargs)
        dim = int(max(1, min(100, dim)))
        width = 1
        gap = 0.2
        cubes = rubik_cube_generator(self.batch_3D, dim, width, gap)
        self.rotate_mode = 0
        self.number = 0
        self.cube_moves, self.higher_moves = possible_moves_generator(dim)
        self.engine = engine(dim, cubes, self.camera.quadrant)

    @extend
    def on_key_press(self, symbol, modifiers):
        match symbol:
            case key.O:
                self.engine.stack_solve()
            case key.P:
                self.engine.full_scramble()
            case key.J:
                self.engine.single_random_move()
            case key.EQUAL:
                self.engine.update_speed(inc=True)
            case key.MINUS:
                self.engine.update_speed(dec=True)
            case key.BRACKETRIGHT:
                self.grid.adjust_num(inc=True)
            case key.BRACKETLEFT:
                self.grid.adjust_num(dec=True)
            case key.T:
                self.engine.time_moves()
            case key.G:
                self.update_grid()
            case key.H:
                self.rotation_animation()
            case key.I:
                # test = "(X Y Z) * 10"
                # test = "(R U R' U') * 6"
                test = "(M E S) * 4"
                self.engine.test_move_sequence(test)
            case _:
                self.number_check(symbol)
                self.cube_move(symbol, modifiers & key.MOD_SHIFT)

    def on_key_release(self, symbol, modifiers):
        self.number_check(symbol, press=False)

    def number_check(self, symbol, press=True):
        for i in range(2, 10):
            if symbol == getattr(key, f"_{i}"):
                self.number = i if press else 0

    def cube_move(self, symbol, shift):
        # Some of the more advanced key combinations are key jammed
        for i in self.cube_moves:
            if symbol == getattr(key, i):
                wide_flag = self.keys[key.W]
                move = wide(i, wide_flag, self.number)
                if move in self.cube_moves + self.higher_moves:
                    move += "'" if shift else ""    # prime move
                    self.engine.update_buffer(move)

    def update_grid(self):
        self.grid_mode = (self.grid_mode + 1) % 5
        data = {"colour": (self.grid_mode - 1) & 1 and self.grid_mode,
                "full": (self.grid_mode - 1) & 2 and self.grid_mode}
        self.grid.generate_grid(**data)
        self.engine.update_grid(data["colour"])

    def rotation_animation(self):
        self.rotate_mode = (self.rotate_mode + 1) % 8
        self.camera.rotation_animation(self.rotate_mode)

    @extend
    def update(self, dt):
        if self.exclusive_mouse:
            # allows camera movement and tracks quadrant changes
            new_quadrant = self.camera.move(dt, self.keys)
            if new_quadrant is not None:
                self.engine.reorient_cube(new_quadrant)
        self.engine.run()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive_mouse:
            self.camera.orientate(-dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, b, m):
        if self.exclusive_mouse:
            self.camera.orientate(-dx, dy)

    def on_mouse_press(self, x, y, b, m):
        pass

    def on_mouse_release(self, x, y, b, m):
        pass


