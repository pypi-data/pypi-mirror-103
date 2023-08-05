import fdfd
import setuptools

with open("readme.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name=fdfd.__name__,
    version=fdfd.__version__,
    author=fdfd.__author__,
    author_email="floris.laporte@gmail.com",
    description=fdfd.__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/flaport/fdfd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
