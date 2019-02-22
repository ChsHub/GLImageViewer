from utility.logger import Logger

from src.view import Viewer
from PIL import Image

def main(path):
    texture_image = None
    with Image.open(path) as texture_image:
        width, height = texture_image.size
        texture_image = texture_image.convert('RGB')
        texture_image = list(texture_image.getdata())
        points = [(x % width, x // width) for x in range(len(texture_image))]

    with Logger() as log:
        gl_width = 1.0
        gl_height = 1.0
        Viewer(points=[(0.0, 0.0), (width, 0.0), (0.0, height),(width, height)],
               colors=[],
               scale=2, gl_width=width / max(height, width), gl_height=height / max(height, width),
               vertex_file="vertex3d_mod.glsl", fragment_file="fragment1.glsl",
               title=b'Title', texture_image=texture_image, width=width, height=height)
if __name__ == '__main__':
    main("")
