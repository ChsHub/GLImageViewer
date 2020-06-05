from logger_default import Logger

from src.view import GlutWindow




def show_image(path):
    path = path.strip('"')

    with Logger():
        GlutWindow(title=b'Title', path=path)


if __name__ == '__main__':
    show_image(input('INPUT IMAGE PATH: '))
