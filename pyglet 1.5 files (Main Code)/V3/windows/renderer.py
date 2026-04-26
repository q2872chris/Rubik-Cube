import pyglet as py
import pyglet.gl as gl
from windows.window import window
from objects.camera import camera
from utilities.general_utilities import extend


class renderer(window):
    def __init__(self, *args, start_position: tuple, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_colour = (0.5, 0.7, 1)
        self.FOV = 70
        self.render_distance = 100
        self.clipping_distance = 0.1
        self.aspect_ratio = self.width / self.height
        self.batch_2D = py.graphics.Batch()
        self.batch_3D = py.graphics.Batch()
        self.camera = camera(start_position)

    def on_draw(self):
        self.set3D()
        # self.overlay2D()
        self.draw3D()

    def set3D(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.gluPerspective(self.FOV, self.aspect_ratio, self.clipping_distance,
                          self.render_distance)

    # Requires test
    def overlay2D(self):
        gl.glPushMatrix()
        gl.gluOrtho2D(0, self.width, 0, self.height)
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.batch_2D.draw()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPopMatrix()

    def draw3D(self):
        self.clear()
        gl.glClearColor(*self.background_colour, 1)
        gl.glRotatef(-self.camera.rot[1], 1, 0, 0)
        gl.glRotatef(-self.camera.rot[0], 0, 1, 0)
        gl.glTranslatef(*(-self.camera.pos))
        self.batch_3D.draw()

    @extend
    def update(self, dt: float):
        if self.exclusive_mouse:
            self.camera.move(dt, self.keys)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive_mouse:
            self.camera.orientate(-dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, b, m):
        if self.exclusive_mouse:
            self.camera.orientate(-dx, dy)



if __name__ == "__main__":
    from objects.objects3d import rubik_cube_generator
    from utilities.cube_utilities import rubik_cube_diagonal
    d, w, g = 7, 1.0, 0.2
    corner_position = rubik_cube_diagonal(d, w, g)
    start_pos = corner_position * 1.7
    test = renderer(width=600, height=400, caption="renderer test",
                    start_position=start_pos)
    rubik_cube_generator(test.batch_3D, d, w, g, True)
    py.gl.glEnable(py.gl.GL_DEPTH_TEST)
    py.gl.glEnable(py.gl.GL_CULL_FACE)
    py.app.run()












