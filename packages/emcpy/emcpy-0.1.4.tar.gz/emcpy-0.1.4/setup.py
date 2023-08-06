from setuptools import setup

with open('README.md', "r") as fh:
    long_description = fh.read()

setup(
    name='emcpy',
    version='0.1.4',
    author="WinterPhish",
    description="A python package to get information on the minecraft server EarthMC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["emcpy", "exceptions", "methods", "util"],
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
