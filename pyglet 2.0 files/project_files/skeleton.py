import pyglet as py
from pyglet.gl import *
from pyglet.window import key
from project_files.objects import generate_rubik_cube
from pyglet.graphics.shader import Shader, ShaderProgram
from project_files.colours import sky, normalise_colour


class window(py.window.Window):
    def __init__(self, *args, dim=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(380, 50)      # update
        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)
        self.exclusive = True
        self.set_exclusive_mouse(self.exclusive)
        self.keys = key.KeyStateHandler()
        py.clock.schedule(self.update)
        glClearColor(*normalise_colour(sky), 1)
        self.FOV = 70
        self.render_distance = 100
        self.clipping_distance = 0.1
        self.batch_3D = py.graphics.Batch()
        self.program = self.activate_shader()
        self.update_projection()
        dim = int(max(min(dim, 20), 1))
        width = 1
        gap = 0.2
        cubes = generate_rubik_cube(self.program, self.batch_3D, dim, width, gap)
        self.fps_display = py.window.FPSDisplay(window=self)

    def update_projection(self):
        proj_mat = Mat4.perspective_projection(self.aspect_ratio,
            self.clipping_distance, self.render_distance, self.FOV)
        self.program['projection'] = proj_mat

    def update_FOV(self, inc=False, dec=False):
        if inc:
            self.FOV -= 1
        if dec:
            self.FOV += 1
        self.update_projection()

    @staticmethod
    def activate_shader():
        with open("project_files/shader_sources/vertex_source.gl") as reader:
            vertex_source = "".join(reader.readlines())
        with open("project_files/shader_sources/fragment_source.gl") as reader:
            fragment_source = "".join(reader.readlines())
        vert_shader = Shader(vertex_source, 'vertex')
        frag_shader = Shader(fragment_source, 'fragment')
        return ShaderProgram(vert_shader, frag_shader)

    def on_key_press(self, symbol, modifiers):
        match symbol:
            case key.ESCAPE:
                self.close()
            case key.K:
                self.exclusive = not self.exclusive
                self.set_exclusive_mouse(self.exclusive)
            case key.SEMICOLON:
                self.update_FOV(dec=True)
            case key.APOSTROPHE:
                self.update_FOV(inc=True)
            case _:
                pass

    def update(self, dt):
        if self.exclusive:
            pass
        self.push_handlers(self.keys)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            pass

    def on_mouse_drag(self, x, y, dx, dy, b, m):
        if self.exclusive:
            pass

    def on_draw(self):
        # print(self.fps_display.label.text)    # fps
        self.clear()
        self.batch_3D.draw()

    def on_key_release(self, symbol, modifiers):
        self.number_check(symbol, press=False)

    def on_mouse_press(self, x, y, b, m):
        pass

    def on_mouse_release(self, x, y, b, m):
        pass

