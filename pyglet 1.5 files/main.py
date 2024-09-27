from pyglet.gl import *
from pyglet.app import run
from project_files.skeleton import window

# glEnable(GL_COLOR_MATERIAL)
# glEnable(GL_LIGHTING)
# glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat * 4)(3, 3, 3, 1))
# glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat * 4)(3, 3, 3, 1))
# glEnable(GL_LIGHT0)
# glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
# glEnable(GL_NORMALIZE)
# # glNormal3f

if __name__ == "__main__":
    window(600, 400, "Pyglet Rubix Cube")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    run()

