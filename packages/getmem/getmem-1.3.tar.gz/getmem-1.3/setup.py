import pathlib

"""

                888   888b     d888                      
                888   8888b   d8888                      
                888   88888b.d88888                      
.d88b.  .d88b. 888888888Y88888P888 .d88b. 88888b.d88b.  
d88P"88bd8P  Y8b888   888 Y888P 888d8P  Y8b888 "888 "88b 
888  88888888888888   888  Y8P  88888888888888  888  888 
Y88b 888Y8b.    Y88b. 888   "   888Y8b.    888  888  888 
"Y88888 "Y8888  "Y888888       888 "Y8888 888  888  888 
    888                                                 
Y8b d88P                                                 
"Y88P"                  

Getmem by Shaurya Pratap Singh
MIT LICENCE © SHAURYA PRATAP SINGH 2-0-2-1

"""

from setuptools import setup


setup(
    name="getmem",
    version="1.3",
    description="Find out the biggest files in your computer!",
    long_description="# Getmem 1.3",
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