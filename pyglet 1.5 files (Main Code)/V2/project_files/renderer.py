import pyglet as py
import pyglet.gl as gl
from pyglet.graphics import Batch, draw
from project_files.cube_utilities import cube_diagonal
from project_files.other_objects import grid
from project_files.camera import camera


class renderer(py.window.Window):
    def __init__(self, *args, dim=7, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_colour = (0.5, 0.7, 1)
        self._FOV = 70
        self._render_distance = 100
        self._clipping_distance = 0.1
        self.aspect_ratio = self.width / self.height
        self.batch_2D = Batch()
        self.batch_3D = Batch()
        dim = int(max(1, min(100, dim)))
        width = 1
        gap = 0.2
        self.grid_mode = 0
        self.grid = grid(dim, width, gap)
        corner_pos = cube_diagonal(dim, width, gap)
        start_pos = corner_pos * [1.3, 1.2, 1.3]
        self.camera = camera(start_pos)

    def on_draw(self):
        self.set3D()
        self.overlay2D()
        self.draw3D()
        # remove?
        if self.grid_mode:
            draw(*self.grid.grid_data)

    def set3D(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.gluPerspective(self._FOV, self.aspect_ratio,
                          self._clipping_distance,
                          self._render_distance)

    def draw3D(self):
        self.clear()
        gl.glClearColor(*self.background_colour, 1)
        gl.glRotatef(-self.camera.rot[1], 1, 0, 0)
        gl.glRotatef(-self.camera.rot[0], 0, 1, 0)
        gl.glTranslatef(*(-self.camera.pos))
        self.batch_3D.draw()

    def overlay2D(self):
        gl.glPushMatrix()
        gl.gluOrtho2D(0, self.width, 0, self.height)
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.batch_2D.draw()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPopMatrix()

    @property
    def FOV(self):
        return self._FOV

    @FOV.setter
    def FOV(self, value: int):
        self._FOV = min(max(90, value), 1)

    @property
    def clipping_distance(self):
        return self._clipping_distance

    @clipping_distance.setter
    def clipping_distance(self, value: float):
        value = min(max(0.01, value), self._render_distance)
        self._clipping_distance = value

    @property
    def render_distance(self):
        return self._render_distance

    @render_distance.setter
    def render_distance(self, value: float):
        value = min(max(self._clipping_distance, value), 1000)
        self._render_distance = value


if __name__ == "__main__":
    r = renderer(width=600, height=400, caption="Pyglet Rubix Cube 1.2")
    r.clipping_distance = 200
    r.render_distance = 10000
    print(r.clipping_distance, r.render_distance)
    # py.app.run()



