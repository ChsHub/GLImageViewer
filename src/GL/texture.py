from logging import info

import OpenGL.GL as gl
import numpy
from PIL import Image
from numpy.lib.arraypad import np


def get_texture_image(path):
    with Image.open(path) as texture_image:
        width, height = texture_image.size
        texture_image = texture_image.convert('RGB')
        texture_image = list(texture_image.getdata())
    return texture_image, width, height


def bind_texture(texture_image, height, width):
    texture = gl.glGenTextures(1, 0)
    info(gl.glGetError())

    texture_image = numpy.array(texture_image, dtype=np.uint8)
    texture_image.reshape((height, width, 3))
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_MIRRORED_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_MIRRORED_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB8, width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, texture_image)
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
    info(gl.glGetError())
