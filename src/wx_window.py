from wx import Frame, ID_ANY, EVT_CLOSE, Icon, BITMAP_TYPE_ANY, EXPAND, Bitmap, VERTICAL, App, Panel, Slider, \
    StaticText, HORIZONTAL
from wxwidgets import SimpleSizer

from src.open_gl_canvas import OpenGLCanvas


class TitledSlider(Panel):
    def __init__(self, parent, text):
        Panel.__init__(self, parent)
        with SimpleSizer(self, VERTICAL) as sizer:
            text = StaticText(self, label=text)
            sizer.Add(text, EXPAND)
            slider = Slider(self)
            sizer.Add(slider, EXPAND)


class Window(Frame):
    def __init__(self, title):
        # init window
        Frame.__init__(self, None, ID_ANY, title, size=(1600, 900))
        self.Bind(EVT_CLOSE, lambda x: self.Destroy())
        loc = Icon()
        loc.CopyFromBitmap(Bitmap('icon.ico', BITMAP_TYPE_ANY))
        self.SetIcon(loc)

        panel = Panel(self, EXPAND)
        with SimpleSizer(panel, VERTICAL) as sizer:

            sliders = Panel(panel, EXPAND)
            with SimpleSizer(sliders, HORIZONTAL) as sizer1:
                for title in ['LOW', 'HIGH', 'SIGMA']:
                    new_slider = TitledSlider(sliders, title)
                    sizer1.Add(new_slider)

            new_element = OpenGLCanvas(panel,
                                       'IMAGE PATH',
                                       800)
            sizer.Add(sliders)
            sizer.Add(new_element)


if __name__ == '__main__':
    app = App()
    frame = Window('Image viewer')
    frame.Show()

    app.MainLoop()
    app.Destroy()
