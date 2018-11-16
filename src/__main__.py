from utility.logger import Logger

from src.view import Viewer
from src.points_test import points
from PIL import Image

points = list(zip(*points))
points1 = points[0]

with Image.open("D:\Making\Python\image_optimiser/tests/test.png") as image:
    width, height = image.size
    image = list(image.getdata())
    points = [(x % width, x // width) for x in range(len(image))]

if __name__ == '__main__':
    with Logger() as log:
        Viewer(points=points, colors=image,
               scale=0.01,offset_x=-width//2, offset_y=-height//2, point_size=10,
               vertex_file="vertex3d_mod.glsl",
               fragment_file="fragment1.glsl",
               title=b'Title')
