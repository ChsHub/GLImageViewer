from utility.logger import Logger

from src.view import Viewer
from PIL import Image

with Image.open("D:\Making\Python\image_optimiser/tests/test.png") as texture_image:
    width, height = texture_image.size
    texture_image = list(texture_image.getdata())
    points = [(x % width, x // width) for x in range(len(texture_image))]

if __name__ == '__main__':
    with Logger() as log:
        Viewer(points=[(0.0, 0.0), (0.0, 1.0),(1.0, 0.0), (1.0, 1.0)],
               colors=[],
               scale=1, offset_x=0, offset_y=0, point_size=10,
               vertex_file="vertex3d_mod.glsl",
               fragment_file="fragment1.glsl",
               title=b'Title', texture_image=texture_image, width=width, height=height)
