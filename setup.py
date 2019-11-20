
import os
try:
    from setuptools import setup
except ImportError as e:
    from distutils.core import setup

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, "README.md"), "r") as f:
    long_description = f.read()
with open(os.path.join(DIR, "requirements.txt"), "r") as f:
    REQUIRED = [i for i in f.read().split("\n") if len(i)]


setup(
    name="rightmove_webscraper",
    packages=["rightmove_webscraper"],
    version="1.0",
    description="A class for scraping data from rightmove.co.uk",
    long_description=long_description,
    author="Toby Petty",
    author_email="tobypetty@hotmail.com",
    url="https://github.com/woblers/rightmove_webscraper.py",
    install_requires=REQUIRED,
    keywords=["webscraping", "rightmove", "data"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True,
    package_data={"rightmove_webscraper": ["docs/*", "docs/*/*"]}
)
