from setuptools import *

setup(
    name = "semhue",
    version = "1.0.1",
    author = "Sem Moolenschot",
    author_email = "",
    description = "",
    packages = find_packages(),
    include_package_data = True,
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
