from setuptools import *

with open ("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name = "semhue",
    version = "1.0.0",
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
    install_requires = requirements,
)