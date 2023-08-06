from setuptools import setup, find_packages

setup(
    name="zenitai",
    version="0.1",
    packages=["zenitai", r"zenitai\transform", r"zenitai\utils"],
    descrption="A collection of tools and utils for data analysis. Contains functions and tools for WOE-transformations and other utils",
)
