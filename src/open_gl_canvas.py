import wx
from wx import glcanvas

from src.GL.program import GLProgram
# https://stackoverflow.com/questions/39734211/how-do-i-get-pyopengl-to-work-with-a-wxpython-context-based-on-this-c-modern
from src.GL.texture import get_texture_image
from src.GL.uniforms import Resizer


class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent, image_path, size):
        self.texture_image, self.width, self.height = get_texture_image(image_path)
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(size, size))

        self._image_path = image_path
        self.program = None
        self.context = glcanvas.GLContext(self)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnEraseBackground(self, event):
        pass  # Do nothing, to avoid flashing on MSW.

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)

        if not self.program:
            self.program = GLProgram(self.texture_image, width=self.width, height=self.height)

        self.OnDraw()

    def OnDraw(self):
        if self.program:
            self.program.redraw()
            self.SwapBuffers()
