import ctypes
import sys
from logging import info
from os.path import join

import OpenGL.GL as gl
import OpenGL.GLUT as glut
import numpy
from numpy.lib.arraypad import np
from timerpy import Timer


class Viewer:
    point_count = 0
    projection = None
    program = None
    phi, theta = 0, 0

    def __init__(self, points, colors, scale, vertex_file, fragment_file, title,
                 texture_image, width, height):

        self.width = width
        self.height = height

        with Timer('INIT GL'):
            self.point_count = len(points)

            self._init_glut(title)
            self.program = self._init_program(vertex_file, fragment_file)

            # read data
            data = self._init_data(points, colors)
            buffer = self._build_buffer(data)
            self._bind_buffers(data, buffer)
            info(gl.glGetError())

            texture = gl.glGenTextures(1, 0)
            info(gl.glGetError())

            texture_image = numpy.array(texture_image, dtype=np.uint8)
            texture_image.reshape((height, width, 3))
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_MIRRORED_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_MIRRORED_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB8, width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE,
                            texture_image)
            gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

            info(gl.glGetError())

            # bind uniforms
            self._bind_target_value(scale, "scale")
            self._bind_size(1.0, 1.0)

        glut.glutMainLoop()

    def _bind_size(self, width, height):

        gl_width = self.width / max(self.height, self.width)
        gl_height = self.height / max(self.height, self.width)

        if self.width > self.height:
            gl_height *= (width / height)
        else:
            gl_width *= (height / width)

        self._bind_target_value(gl_width, "width")
        self._bind_target_value(gl_height, "height")

    # GL methods:
    def _display(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.point_count)
        glut.glutSwapBuffers()

    def _set_window_size(self, width, height):
        """
        Function is called by GL, when window is resized
        :param width:
        :param height:
        :return:
        """

        print(width, height)
        gl.glViewport(0, 0, width, height)

        self._bind_size(width, height)
        # self.projection = perspective(45.0, width / float(height), 2.0, 10.0)
        # self._bind_matrix(self.projection, 'projection')

    def _keyboard(self, key, x, y):
        if key == '\033':
            sys.exit()

    def _init_data(self, points, colors):
        data = numpy.zeros(self.point_count, dtype=[("position", np.float32, 2)])
        data['position'] = points
        return data

    def _init_glut(self, time):

        if type(time) != bytes:
            raise TypeError

        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)  # | glut.GLUT_DEPTH)
        # gl.glEnable(gl.GL_DEPTH_TEST)
        glut.glutCreateWindow(time)
        glut.glutReshapeWindow(700, 700)
        glut.glutReshapeFunc(self._set_window_size)
        glut.glutDisplayFunc(self._display)
        glut.glutKeyboardFunc(self._keyboard)
        # glut.glutTimerFunc(int(1000 / 60), self._timer, 60)

    def _get_shader(self, path, file, shader_type):
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

        gl.glShaderSource(shader, shader_code)
        info(gl.glGetError())

        return shader

    def _init_program(self, vertex_file, fragment_file):
        # Read shaders
        path = "./shader"

        # TODO error handling
        self.program = gl.glCreateProgram()
        info(gl.glGetError())

        # Set shaders source
        vertex = self._get_shader(path, vertex_file, gl.GL_VERTEX_SHADER)
        fragment = self._get_shader(path, fragment_file, gl.GL_FRAGMENT_SHADER)

        # Compile shaders
        gl.glCompileShader(vertex)
        info(gl.glGetError())
        gl.glCompileShader(fragment)
        info(gl.glGetError())

        # We can now build and link the program

        gl.glAttachShader(self.program, vertex)
        info(gl.glGetError())
        gl.glAttachShader(self.program, fragment)
        info(gl.glGetError())
        gl.glLinkProgram(self.program)
        info(gl.glGetError())

        # We can not get rid of shaders, they won't be used again:

        gl.glDetachShader(self.program, vertex)
        info(gl.glGetError())
        gl.glDetachShader(self.program, fragment)
        info(gl.glGetError())

        # Finally, we make program the default program to be ran.
        # We can do it now because we'll use a single in this example:
        info(glut.glutReportErrors())
        if gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS) == 0:
            info(gl.glGetShaderInfoLog(vertex))

        if gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS) == 0:
            info(gl.glGetShaderInfoLog(fragment))

        if gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS) == 0:
            info(gl.glGetProgramInfoLog(self.program))

        gl.glUseProgram(self.program)
        info(gl.glGetError())

        return self.program

    def _build_buffer(self, data):
        # Request a buffer slot from GPU
        buffer = gl.glGenBuffers(1)

        # Make this buffer the default one
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

        # Upload data
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

        return buffer

    def _bind_buffers(self, data, buffer):

        stride = data.strides[0]
        offset = ctypes.c_void_p(0)
        loc = gl.glGetAttribLocation(self.program, "position")

        gl.glEnableVertexAttribArray(loc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        info('DATA LENGTH %s' % len(data))
        gl.glVertexAttribPointer(loc, len(data[0]) * 2, gl.GL_FLOAT, False, stride, offset)

        # offset = ctypes.c_void_p(data.dtype["position"].itemsize)
        # loc = gl.glGetAttribLocation(self.program, "color")

        # gl.glEnableVertexAttribArray(loc)
        # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        # gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)

    # Bind Uniform:
    def _bind_target_value(self, target_value, name):
        loc = gl.glGetUniformLocation(self.program, name)
        gl.glUniform1f(loc, np.float32(target_value))

    def _bind_matrix(self, matrix, name):
        info("bind matrix: %s" % name)
        location = gl.glGetUniformLocation(self.program, name=name)
        info(gl.glGetError())
        if location == -1:
            raise ValueError('Location not found')
        gl.glUniformMatrix4fv(location, 1, False, matrix)
        # location, count, transpose, value
