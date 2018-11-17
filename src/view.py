import OpenGL.GL as gl
import OpenGL.GLUT as glut
import sys
from utility.os_interface import read_file_data
import numpy
from numpy.lib.arraypad import np
from numpy import int32
import ctypes
from src.transforms import perspective, translate, rotate


class Viewer:
    point_count = 0
    projection = None
    program = None
    phi, theta = 0, 0

    def __init__(self, points, colors, scale, offset_x, offset_y, point_size, vertex_file, fragment_file, title, texture_image, width, height):

        self.point_count = len(points)

        self._init_glut(title)
        self.program = self._init_program(vertex_file, fragment_file)

        # read data
        data = self._init_data(points, colors)
        buffer = self._build_buffer(data)
        self._bind_buffers(data, buffer)
        print(gl.glGetError())


        texture = gl.glGenTextures(1, 0)
        print(gl.glGetError())

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


        print(gl.glGetError())

        # bind uniforms
        self._bind_target_value(scale, "scale")
        self._bind_target_value(offset_x, "offset_x")
        self._bind_target_value(offset_y, "offset_y")
        # self._bind_target_value(point_size, "point_size")
        self._bind_projection()

        glut.glutMainLoop()




    def _bind_projection(self):
        self.view = np.eye(4, dtype=np.float32)
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)
        translate(self.view, 0, 0, -5)

        self._bind_matrix(self.model, 'model')
        self._bind_matrix(self.view, 'view')
        self._bind_matrix(self.projection, 'projection')

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
        gl.glViewport(0, 0, width, height)
        self.projection = perspective(45.0, width / float(height), 2.0, 10.0)
        self._bind_matrix(self.projection, 'projection')

    def _keyboard(self, key, x, y):
        if key == '\033':
            sys.exit()

    def _timer(self, fps):
        self.theta += .5
        self.phi += .5
        self.model = np.eye(4, dtype=np.float32)
        # rotate(self.model, self.theta, 1, 0, 0)
        rotate(self.model, self.phi, 0, 1, 0)
        self._bind_matrix(self.model, 'model')
        # glut.glutTimerFunc(int(1000 / fps), self._timer, fps)
        glut.glutPostRedisplay()


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

    def _init_program(self, vertex_file, fragment_file):
        # read shaders
        path = "./shader"
        vertex_code = read_file_data(path, vertex_file)
        fragment_code = read_file_data(path, fragment_file)

        if not vertex_code:
            raise ValueError
        if not fragment_code:
            raise ValueError

        # TODO error handling
        self.program = gl.glCreateProgram()
        print(gl.glGetError())
        vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        print(gl.glGetError())
        fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        print(gl.glGetError())
        # Set shaders source
        gl.glShaderSource(vertex, vertex_code)
        print(gl.glGetError())
        gl.glShaderSource(fragment, fragment_code)
        print(gl.glGetError())
        # Compile shaders
        gl.glCompileShader(vertex)
        print(gl.glGetError())
        gl.glCompileShader(fragment)
        print(gl.glGetError())

        # We can now build and link the program

        gl.glAttachShader(self.program, vertex)
        print(gl.glGetError())
        gl.glAttachShader(self.program, fragment)
        print(gl.glGetError())
        gl.glLinkProgram(self.program)
        print(gl.glGetError())

        # We can not get rid of shaders, they won't be used again:

        gl.glDetachShader(self.program, vertex)
        print(gl.glGetError())
        gl.glDetachShader(self.program, fragment)
        print(gl.glGetError())

        # Finally, we make program the default program to be ran.
        # We can do it now because we'll use a single in this example:
        print(glut.glutReportErrors())
        if gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS) == 0:
            print(gl.glGetShaderInfoLog(vertex))

        if gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS) == 0:
            print(gl.glGetShaderInfoLog(fragment))

        if gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS) == 0:
            print(gl.glGetProgramInfoLog(self.program))

        gl.glUseProgram(self.program)
        print(gl.glGetError())

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

        gl.glVertexAttribPointer(loc, len(data), gl.GL_FLOAT, False, stride, offset)

        # offset = ctypes.c_void_p(data.dtype["position"].itemsize)
        # loc = gl.glGetAttribLocation(self.program, "color")

        # gl.glEnableVertexAttribArray(loc)
        # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        # gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)

    # Bind Uniform:
    def _bind_target_value(self, target_value, name):
        loc = gl.glGetUniformLocation(self.program, name)
        gl.glUniform1f(loc, target_value)

    def _bind_matrix(self, matrix, name):
        print("bind matrix: ", name)
        location = gl.glGetUniformLocation(self.program, name)
        print(gl.glGetError())
        if location == -1:
            raise ValueError
        gl.glUniformMatrix4fv(location, 1, False, matrix)
        # location, count, transpose, value
