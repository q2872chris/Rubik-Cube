import pyglet as py
import pyglet.gl as gl
from windows.main_controller import main_controller


if __name__ == "__main__":
    main_controller(width=600, height=400, caption="Pyglet Rubix Cube 3.0",
                    dim=7, cube_width=1.0, gap=0.2, start_speed=6)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_CULL_FACE)
    py.app.run()
