from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'Getting information about youtube video(s)'
LONG_DESCRIPTION = 'A package that allows you to get information such as "likes", "subs", "views", and more. No API needed.'

# Setting up
setup(
    name="ygetter",
    version=VERSION,
    author="Fred",
    author_email="unknown@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['urllib3', 'numpy', 'easygui'],
    keywords=['python', 'youtube', 'yt', 'info', 'info getter', 'easy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
