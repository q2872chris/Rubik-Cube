from pyglet.gl import *
from pyglet.app import run
from files.skeleton import window

window(600, 400, "Pyglet Rubix Cube")
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)


if __name__ == "__main__":
    run()

