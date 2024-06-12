from pyglet.math import Vec3

orange = [255, 150, 0]
white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
blue = [0, 0, 255]
green = [0, 255, 0]         # (lime)
pink = [255, 50, 255]
purple = [120, 40, 200]
yellow = [255, 255, 0]
turquoise = [0, 255, 255]
sky = [51, 179, 255]

normalise_colour = lambda colour: Vec3(*colour) / 255

