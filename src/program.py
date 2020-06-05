import ctypes
import sys
from logging import info
from os.path import join

import OpenGL.GL as gl
import OpenGL.GLUT as glut
import numpy
from numpy.lib.arraypad import np
from timerpy import Timer


def _get_shader(path, file, shader_type, program):
    """
    Create the shader and link shader source code
    :param path: Shader code path
    :param file: Shader code file
    :param shader_type: GL_VERTEX_SHADER or GL_FRAGMENT_SHADER
    :return: glShader
    """
    with open(join(path, file), mode='r') as f:
        shader_code = f.read()
    if not shader_code:
        raise ValueError

    shader = gl.glCreateShader(shader_type)
    info(gl.glGetError())
    # Link
    gl.glShaderSource(shader, shader_code)
    info(gl.glGetError())
    # Compile
    gl.glCompileShader(shader)
    info(gl.glGetError())
    # Attach
    gl.glAttachShader(program, shader)
    info(gl.glGetError())
    return shader


def init_program(vertex_file: str = "vertex3d_mod.glsl", fragment_file: str = "fragment1.glsl", path: str = "./shader"):
    # Read shaders

    # TODO error handling
    if not gl.glCreateProgram:
        raise ImportError

    program = gl.glCreateProgram()
    info(gl.glGetError())
    # Set shaders source
    vertex = _get_shader(path, vertex_file, gl.GL_VERTEX_SHADER, program)
    fragment = _get_shader(path, fragment_file, gl.GL_FRAGMENT_SHADER, program)
    gl.glLinkProgram(program)
    info(gl.glGetError())

    # We can now get rid of shaders, they won't be used again:
    for shader in [vertex, fragment]:
        gl.glDetachShader(program, shader)
        info(gl.glGetError())
        # Finally, we make program the default program to be ran.
        # We can do it now because we'll use a single in this example:
        info(glut.glutReportErrors())
        if gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS) == 0:
            info(gl.glGetShaderInfoLog(shader))

    if gl.glGetProgramiv(program, gl.GL_LINK_STATUS) == 0:
        info(gl.glGetProgramInfoLog(program))

    gl.glUseProgram(program)
    info(gl.glGetError())

    return program
