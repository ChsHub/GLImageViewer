import setuptools
from distutils.core import setup
from src import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='GlImageViewer',
    version=__version__,
    description=long_description.split('\n')[1], # First line of description
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ChsHub',
    packages=['src'],
    license='MIT License',
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['PyOpenGL']
)
