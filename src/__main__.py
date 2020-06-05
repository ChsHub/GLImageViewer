from logger_default import Logger

from src.view import Viewer
from PIL import Image


def main(path):
    path = path.strip('"')
    with Image.open(path) as texture_image:
        width, height = texture_image.size
        texture_image = texture_image.convert('RGB')
        texture_image = list(texture_image.getdata())
    with Logger():
        Viewer(points=[(0.0, 0.0), (width, 0.0), (0.0, height), (width, height)],
               colors=[],
               scale=1,
               vertex_file="vertex3d_mod.glsl", fragment_file="fragment1.glsl",
               title=b'Title', texture_image=texture_image, width=width, height=height)

if __name__ == '__main__':
    main(input('INPUT IMAGE PATH: '))
