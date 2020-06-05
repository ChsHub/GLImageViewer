from wx import Frame, ID_ANY, EVT_CLOSE, Icon, BITMAP_TYPE_ANY, EXPAND, Bitmap, VERTICAL, App, Panel, Slider, StaticText
from wxwidgets import SimpleSizer

from src.open_gl_canvas import OpenGLCanvas


class Window(Frame):
    def __init__(self, title):
        # init window
        Frame.__init__(self, None, ID_ANY, title, size=(800, 800))
        self.Bind(EVT_CLOSE, lambda x: self.Destroy())
        loc = Icon()
        loc.CopyFromBitmap(Bitmap('icon.ico', BITMAP_TYPE_ANY))
        self.SetIcon(loc)

        with SimpleSizer(self, VERTICAL) as sizer:
            new_element = OpenGLCanvas(self)
            sizer.Add(new_element)


if __name__ == '__main__':
    app = App()
    frame = Window('Image viewer')
    frame.Show()

    app.MainLoop()
    app.Destroy()
