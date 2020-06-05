from wx import Frame, ID_ANY, EVT_CLOSE, Icon, BITMAP_TYPE_ANY, EXPAND, Bitmap, VERTICAL, App
from wx.glcanvas import GLCanvas
from wxwidgets import SimpleSizer

from src.open_gl_canvas import OpenGLCanvas


class Window(Frame):
    def __init__(self):
        # init window
        Frame.__init__(self, None, ID_ANY, "CUT", size=(800, 800))
        self.Bind(EVT_CLOSE, lambda x: self.Destroy())
        loc = Icon()
        loc.CopyFromBitmap(Bitmap('icon.ico', BITMAP_TYPE_ANY))
        self.SetIcon(loc)

        with SimpleSizer(self, VERTICAL) as sizer:
            new_element = OpenGLCanvas(self)
            sizer.Add(new_element)


if __name__ == '__main__':
    app = App()
    frame = Window()
    frame.Show()

    app.MainLoop()
    app.Destroy()
