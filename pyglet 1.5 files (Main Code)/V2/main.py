from pyglet.gl import *
from pyglet.app import run
from project_files.cube_controller import cube_controller


if __name__ == "__main__":
    cube_controller(width=600, height=400, caption="Pyglet Rubix Cube 1.2")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    run()

