import OpenGL.GL as gl
from numpy.lib.arraypad import np


# Bind Uniform:
def bind_target_value(program, target_value, name):
    loc = gl.glGetUniformLocation(program, name)
    gl.glUniform1f(loc, np.float32(target_value))


class Resizer:
    width = None
    height = None
    program = None

    def bind_size(self, width, height):

        gl_width = self.width / max(self.height, self.width)
        gl_height = self.height / max(self.height, self.width)

        if self.width > self.height:
            gl_height *= (width / height)
        else:
            gl_width *= (height / width)

        bind_target_value(self.program, gl_width, "width")
        bind_target_value(self.program, gl_height, "height")

    def set_window_size(self, width, height):
        """
        Function is called by GL, when window is resized
        :param width: New window width
        :param height: New window height
        """
        print(width, height)
        gl.glViewport(0, 0, width, height)
        self.bind_size(width, height)
