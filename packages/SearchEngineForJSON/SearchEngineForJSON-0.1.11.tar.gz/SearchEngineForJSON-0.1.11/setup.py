
from setuptools import setup, find_packages



with open("./README.md", mode="r") as file:
	long_description = file.read()

setup(
	name="SearchEngineForJSON",
	version="v0.1.11",
	author="AoiNakamura",
	author_email="example@gmail.com",
	description="SearchEngineForJSON",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/aoimaru/packagingTutorial",
	packages=find_packages(),
	classifiers=[
        "Programming Language :: Python :: 3",
    ],
	python_requires='>=3.7',
	)

import sys