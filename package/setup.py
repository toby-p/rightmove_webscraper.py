try:
    from setuptools import setup
except Exception as e:
    from distutils.core import setup

long_description = """A simple class for scraping data from the UK's most prominent property sales & lettings listings website, www.rightmove.co.uk

The package is intended for use by data analysts/scientists who require easy access to download property listing data in nicely formatted Pandas DataFrames ready for analysis.
"""

setup(
    name="rightmove_webscraper",
    packages=["rightmove_webscraper"],
    version="0.3",
    description="A class for scraping data from rightmove.co.uk",
    long_description=long_description,
    author="Toby Petty",
    author_email="hello@tobypetty.com",
    url="https://github.com/woblers/rightmove_webscraper.py",
    install_requires=[
        "pandas",
        "requests",
        "lxml"
    ],
    keywords=["webscraping", "rightmove", "data"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)
