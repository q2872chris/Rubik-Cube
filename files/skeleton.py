from pyglet.gl import *
from pyglet.window import key, Window
from pyglet.graphics import Batch
from pyglet.clock import schedule
from files.objects import cube
from files.camera import camera


class window(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(380, 50)
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
        cube(self.batch_3D)
        start_pos = [3, 3, 3]
        start_angle = [45, -30]
        self.camera = camera(start_pos, start_angle)

    def on_key_press(self, symbol, modifiers):
        match symbol:
            case key.ESCAPE:
                self.close()
            case key.K:
                self.exclusive = not self.exclusive
                self.set_exclusive_mouse(self.exclusive)

    def update(self, dt):
        if self.exclusive:
            self.camera.move(dt, self.keys)
        self.push_handlers(self.keys)
        self.draw3d()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            self.camera.orientate(-dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, b, m):
        if self.exclusive:
            self.camera.orientate(-dx, dy)

    def draw3d(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.title_screen_flag:
            gluOrtho2D(0, self.width, 0, self.height)
        else:
            gluPerspective(self.FOV, self.width / self.height,
                           self.clipping_distance, self.render_distance)
            # self.overlay_2d()
            self.draw()

    def draw(self, sky_colour=(0.5, 0.7, 1)):
        self.clear()
        glClearColor(*sky_colour, 1)
        glRotatef(-self.camera.rot[1], 1, 0, 0)
        glRotatef(-self.camera.rot[0], 0, 1, 0)
        glTranslatef(*(-self.camera.pos))
        self.batch_3D.draw()

    def overlay_2d(self):
        glPushMatrix()
        gluOrtho2D(0, self.width, 0, self.height)
        glDisable(gl.GL_DEPTH_TEST)
        self.batch_2D.draw()
        glEnable(gl.GL_DEPTH_TEST)
        glPopMatrix()

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, b, m):
        pass

    def on_mouse_release(self, x, y, b, m):
        pass

    def on_draw(self):
        # py.clock.get_fps()
        pass

