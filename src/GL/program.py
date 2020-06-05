from logging import info
from os.path import join, abspath

import OpenGL.GL as gl

from src.GL.buffer import bind_buffers
from src.GL.texture import bind_texture
from src.GL.uniforms import bind_target_value, Resizer


class GLProgram(Resizer):
    def __init__(self, texture_image, width, height):
        self.width = width
        self.height = height

        points = [(0.0, 0.0), (width, 0.0), (0.0, height), (width, height)]

        program = init_program()
        bind_buffers(program, points)
        bind_texture(texture_image, height, width)
        bind_target_value(program, 1.0, "scale")

        self.program = program
        self.point_count = len(points)
        self.bind_size(1.0, 1.0)

    def redraw(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.point_count)


def _get_shader(path, file, shader_type, program):
    """
    Create the shader and link shader source code
    :param path: Shader code path
    :param file: Shader code file
    :param shader_type: GL_VERTEX_SHADER or GL_FRAGMENT_SHADER
    :return: glShader
    """
    with open(abspath(join(path, file)), mode='r') as f:
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
        if gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS) == 0:
            info(gl.glGetShaderInfoLog(shader))

    if gl.glGetProgramiv(program, gl.GL_LINK_STATUS) == 0:
        info(gl.glGetProgramInfoLog(program))

    gl.glUseProgram(program)
    info(gl.glGetError())

    return program
