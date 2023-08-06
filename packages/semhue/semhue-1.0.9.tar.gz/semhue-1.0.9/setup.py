from setuptools import *
from os import path

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.md"), encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name = "semhue",
    version = "1.0.9",
    author = "Sem Moolenschot",
    author_email = "",
    url = "https://github.com/semmoolenschot/semhue",
    description = "",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    include_package_data = True,
    py_modules=["semhue"],
    license = "MIT",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
    	"phue==1.1"
    ],
)
