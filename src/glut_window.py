import sys

import OpenGL.GLUT as glut
from logger_default import Logger
from timerpy import Timer

from src.GL.program import GLProgram
from src.GL.uniforms import Resizer
from src.GL.texture import get_texture_image

class GlutWindow(Resizer):
    point_count = 0
    projection = None
    program = None
    phi, theta = 0, 0

    def __init__(self, title, path):
        self._init_glut(title)

        with Timer('INIT GL'):
            self.program = GLProgram(self, *get_texture_image(path))

        glut.glutMainLoop()

    # GL methods:
    def _display(self):
        self.program.redraw()
        glut.glutSwapBuffers()

    def _keyboard(self, key, x, y):
        if key == '\033':
            sys.exit()

    def _init_glut(self, time):

        if type(time) != bytes:
            raise TypeError

        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
        glut.glutCreateWindow(time)
        glut.glutReshapeWindow(700, 700)
        glut.glutReshapeFunc(self.set_window_size)
        glut.glutDisplayFunc(self._display)
        glut.glutKeyboardFunc(self._keyboard)


if __name__ == '__main__':
    path = input('INPUT IMAGE PATH: ').strip('"')
    with Logger():
        GlutWindow(title=b'Title', path=path)
