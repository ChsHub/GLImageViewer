import wx
from wx import glcanvas

from src.GL.program import init_GL, redraw
# https://stackoverflow.com/questions/39734211/how-do-i-get-pyopengl-to-work-with-a-wxpython-context-based-on-this-c-modern
from src.GL.uniforms import Resizer


class OpenGLCanvas(glcanvas.GLCanvas, Resizer):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(640, 480))
        self.InitGL = init_GL
        self.init = False
        self.context = glcanvas.GLContext(self)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnEraseBackground(self, event):
        pass  # Do nothing, to avoid flashing on MSW.

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL(self, input('IMAGE PATH:').strip('"'))
            self.init = True
        self.OnDraw()

    def OnDraw(self):
        redraw(self.point_count)
        self.SwapBuffers()
