import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "alexbasiccalculator",
    version = "0.0.1",
    author = "Alexandre Carvalho",
    author_email = "paraalexandrecarvalho@gmail.com",
    description = ("A very basic calculator."),
    license = "BSD",
    keywords = "calculator",
    url = "",
    packages = find_packages(),
    install_requires = [''],
    long_description = read('README.txt') + '\n\n' + read('CHANGELOG.txt'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
)