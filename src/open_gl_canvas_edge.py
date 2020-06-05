from PIL import Image
from numpy import reshape
from skimage.feature import canny
from skimage.io import imread
from timerpy import Timer

from src.GL.texture import bind_texture
from src.open_gl_canvas import OpenGLCanvas


class OpenGLCanvasEdge(OpenGLCanvas):
    def __init__(self, parent, image_path, size):
        OpenGLCanvas.__init__(self, parent, image_path, size)
        self.image_data = imread(fname=image_path, as_gray=True)

    def set_edge_values(self, values):
        # Generate edge image from greyscale image
        with Timer('EDGE'):
            edge_img = canny(
                image=self.image_data,
                sigma=values[0],
                low_threshold=values[1],
                high_threshold=values[2],
            )
        with Timer('RESHAPE'):
            img = Image.new('1', (self.width, self.height))
            edge_img = reshape(edge_img, (self.width * self.height))
            img.putdata(edge_img)
        # img.show()
        with Timer('CONVERT'):
            img = img.convert('RGB')
        print('edges')
        with Timer('BIND'):
            bind_texture(img, self.height, self.width)
        self.OnDraw()