from setuptools import setup

setup(
    name='emcpy',
    version='0.0.1',
    description="A python package to get information on the minecraft server EarthMC",
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
