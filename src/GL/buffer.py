import ctypes
from logging import info

import OpenGL.GL as gl
import numpy
from numpy.lib.arraypad import np


def _build_buffer(data):
    # Request a buffer slot from GPU
    buffer = gl.glGenBuffers(1)
    # Make this buffer the default one
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
    # Upload data
    gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

    return buffer


def _init_data(points):
    data = numpy.zeros(len(points), dtype=[("position", np.float32, 2)])
    data['position'] = points
    return data


def bind_buffers(program, points):
    data = _init_data(points)
    buffer = _build_buffer(data)

    stride = data.strides[0]
    offset = ctypes.c_void_p(0)
    loc = gl.glGetAttribLocation(program, "position")

    gl.glEnableVertexAttribArray(loc)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
    info('DATA LENGTH %s' % len(data))
    gl.glVertexAttribPointer(loc, len(data[0]) * 2, gl.GL_FLOAT, False, stride, offset)
    info(gl.glGetError())


