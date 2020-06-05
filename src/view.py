import sys

import OpenGL.GLUT as glut
from timerpy import Timer

from src.GL.program import init_GL, redraw
from src.GL.uniforms import Resizer


class GlutWindow(Resizer):
    point_count = 0
    projection = None
    program = None
    phi, theta = 0, 0

    def __init__(self, title, path):
        self._init_glut(title)

        with Timer('INIT GL'):
            init_GL(self, path)

        glut.glutMainLoop()

    # GL methods:
    def _display(self):
        redraw(self.point_count)
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
