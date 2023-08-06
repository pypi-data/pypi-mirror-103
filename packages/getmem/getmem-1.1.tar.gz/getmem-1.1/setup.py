import pathlib
from setuptools import setup

# The directory containing this file
# HERE = pathlib.Path(__file__).parent
# The text of the README file
# README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="getmem",
    version="1.1",
    description="Find out the biggest files in your computer!",
    long_description="# Getmem 1.0",
    long_description_content_type="text/markdown",
    author="Shaurya Pratap Singh",
    author_email="shaurya.p.singh21@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["getmem"],
    scripts=['bin/getmem']
)