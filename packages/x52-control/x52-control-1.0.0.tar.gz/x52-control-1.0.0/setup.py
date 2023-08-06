import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

#import x52

# This call to setup() does all the work
setup(
    name="x52-control",
    version="1.0.0",
    description="Configures LEDs and display on Logitech X52 HOTAS",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Nerdeiro/x52-control",
    author="Bento Loewenstein Silveira",
    author_email="anarch157a@ninjazumbi.com",
    license="GPL2",
    py_modules=["x52"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Operating System :: POSIX :: Linux'
    ]
)
