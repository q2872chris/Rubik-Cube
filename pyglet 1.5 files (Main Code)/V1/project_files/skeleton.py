import pyglet.gl as gl
from pyglet.window import key
from pyglet.graphics import Batch, draw
from pyglet.clock import schedule
from project_files.objects import rubik_cube_generator
from project_files.cube_utilities import possible_moves_generator, \
    wide, cube_diagonal
from project_files.general_utilities import timer
from project_files.other_objects import grid
from project_files.engine import engine
from project_files.camera import camera
import pyglet as py

def load_timer(func):
    def inner(self, *args, **kwargs):
        load_time = timer(msg="Time taken to load cubes")
        load_time.start()
        func(self, *args, **kwargs)
        load_time.end()
        print("Rubik cube shape: {}x{}x{}".format(*self.cubes.shape))
        print("Total cubes:", self.cubes.size)
        batched_cubes = sum(i.draw_self for i in self.cubes.ravel())
        print("Total batched cubes:", batched_cubes)
        print("\n")
        del self.cubes, self.dim
    return inner


class window(py.window.Window):
    @load_timer
    def __init__(self, *args, dim=7, **kwargs):
        super().__init__(*args, **kwargs)
        # self.set_icon(pyglet.resource.image("image_path"))
        screen_x = int((self.screen.width - self.width) / 2)
        screen_y = int(25 * self.screen.height / self.height)
        self.set_location(screen_x, screen_y)
        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)
        self.exclusive = True
        self.set_exclusive_mouse(self.exclusive)
        self.keys = key.KeyStateHandler()
        schedule(self.update)
        self.FOV = 70
        self.render_distance = 100
        self.clipping_distance = 0.1
        self.title_screen_flag = False
        self.batch_2D = Batch()
        self.batch_3D = Batch()
        dim = int(max(1, min(100, dim)))
        width = 1
        gap = 0.2
        cubes = rubik_cube_generator(self.batch_3D, dim, width, gap)
        self.grid_mode = 0
        self.grid = grid(dim, width, gap)
        self.rotate_mode = 0
        self.number = 0
        corner_pos = cube_diagonal(dim, width, gap)
        start_pos = corner_pos * [1.3, 1.2, 1.3]
        self.camera = camera(start_pos)
        self.cube_moves, self.higher_moves = possible_moves_generator(dim)
        self.engine = engine(dim, cubes, self.camera.quadrant)
        self.cubes, self.dim = cubes, dim    # used for load timer

    def title_screen_flip(self):
        pass

    def on_key_press(self, symbol, modifiers):
        match symbol:
            case key.ESCAPE:
                self.close()
            case key.K:
                self.exclusive = not self.exclusive
                self.set_exclusive_mouse(self.exclusive)
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

    def update(self, dt):
        if self.exclusive:
            # allows camera movement and tracks quadrant changes
            new_quadrant = self.camera.move(dt, self.keys)
            if new_quadrant is not None:
                self.engine.reorient_cube(new_quadrant)
        self.push_handlers(self.keys)
        self.engine.run()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            self.camera.orientate(-dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, b, m):
        if self.exclusive:
            self.camera.orientate(-dx, dy)

    def on_draw(self):
        # print(py.clock.get_fps())
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        if self.title_screen_flag:
            gl.gluOrtho2D(0, self.width, 0, self.height)
        else:
            gl.gluPerspective(self.FOV, self.width / self.height,
                              self.clipping_distance, self.render_distance)
            # self.overlay_2d()
            self.draw()

    def draw(self, sky_colour=(0.5, 0.7, 1)):
        self.clear()
        gl.glClearColor(*sky_colour, 1)
        gl.glRotatef(-self.camera.rot[1], 1, 0, 0)
        gl.glRotatef(-self.camera.rot[0], 0, 1, 0)
        gl.glTranslatef(*(-self.camera.pos))
        self.batch_3D.draw()
        if self.grid_mode:
            draw(*self.grid.grid_data)

    def overlay_2d(self):
        gl.glPushMatrix()
        gl.gluOrtho2D(0, self.width, 0, self.height)
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.batch_2D.draw()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPopMatrix()

    def on_key_release(self, symbol, modifiers):
        self.number_check(symbol, press=False)

    def on_mouse_press(self, x, y, b, m):
        pass

    def on_mouse_release(self, x, y, b, m):
        pass


