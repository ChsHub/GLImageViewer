from wx import Frame, ID_ANY, EVT_CLOSE, Icon, BITMAP_TYPE_ANY, EXPAND, Bitmap, VERTICAL, App, Panel, Slider, \
    StaticText, HORIZONTAL, EVT_SLIDER
from wxwidgets import SimpleSizer

from src.open_gl_canvas import OpenGLCanvas
from src.open_gl_canvas_edge import OpenGLCanvasEdge


class TitledSlider(Panel):
    def __init__(self, parent, slider_update, text, max_value=100):
        Panel.__init__(self, parent)

        with SimpleSizer(self, VERTICAL) as sizer:
            text = StaticText(self, label=text)
            sizer.Add(text, EXPAND)
            self.slider = Slider(self, maxValue=max_value)
            self.slider.Bind(EVT_SLIDER, slider_update)
            sizer.Add(self.slider, EXPAND)

    def get_value(self):
        return self.slider.GetValue() / 100

class Window(Frame):
    def __init__(self, title, path):
        # init window
        Frame.__init__(self, None, ID_ANY, title, size=(1600, 900))
        self.Bind(EVT_CLOSE, lambda x: self.Destroy())
        loc = Icon()
        loc.CopyFromBitmap(Bitmap('icon.ico', BITMAP_TYPE_ANY))
        self.SetIcon(loc)

        self._sliders = []

        panel = Panel(self, EXPAND)
        with SimpleSizer(panel, VERTICAL) as sizer:
            slider_panel = Panel(panel, EXPAND)
            with SimpleSizer(slider_panel, HORIZONTAL) as sizer1:
                for title in [('LOW',), ('HIGH',), ('SIGMA', 700)]:
                    new_slider = TitledSlider(slider_panel, self.slider_update, *title)
                    sizer1.Add(new_slider)
                    self._sliders.append(new_slider)

            images = Panel(panel, EXPAND)
            with SimpleSizer(images, HORIZONTAL) as sizer2:
                new_element = OpenGLCanvas(images,
                                           path,
                                           800)
                sizer2.Add(new_element)

                self._image_edge = OpenGLCanvasEdge(images,
                                           path,
                                           800)
                sizer2.Add(self._image_edge)

            sizer.Add(slider_panel)
            sizer.Add(images)

    def slider_update(self, event):
        values = list(map(lambda x: x.get_value(), self._sliders))
        print(values)
        self._image_edge.set_edge_values(values)


if __name__ == '__main__':
    app = App()
    frame = Window('Image viewer', input('IMAGE'))
    frame.Show()

    app.MainLoop()
    app.Destroy()
