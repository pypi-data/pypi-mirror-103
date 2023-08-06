import setuptools
import os 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="semitan",
    version="0.0.1",
    author="kikadisa",
    author_email="kikadisa@gmail.com",
    description="Library that interacts with Tan API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcpaulchan/semitan",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
    keywords='tan transport transports metropolitain semitan nantes tram chronobus bus',
)
