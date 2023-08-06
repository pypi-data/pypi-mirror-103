from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.4'
DESCRIPTION = 'Basic hello package'

# Setting up
setup(
    name="simple hello package",
    version=VERSION,
    author="Hirokazu Hirono",
    author_email="<hirono.hirokazu@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream',
              'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
