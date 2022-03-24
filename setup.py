
import os
try:
    from setuptools import setup
except ImportError as e:
    from distutils.core import setup

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, "docs", "README.txt"), "r") as f:
    long_description = f.read()
with open(os.path.join(DIR, "requirements.txt"), "r") as f:
    REQUIRED = [i for i in f.read().split("\n") if len(i)]
with open(os.path.join(DIR, "dev-requirements.txt"), "r") as f:
    TESTS_REQUIRE = [i for i in f.read().split("\n") if len(i)]


setup(
    name="rightmove_webscraper",
    packages=["rightmove_webscraper"],
    version="1.1",
    description="A class for scraping data from rightmove.co.uk",
    long_description=long_description,
    author="Toby Petty",
    author_email="toby.b.petty@gmail.com",
    url="https://github.com/toby-p/rightmove_webscraper.py",
    install_requires=REQUIRED,
    tests_require=TESTS_REQUIRE,
    python_requires='>=3.6',
    keywords=["webscraping", "rightmove", "data"],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True,
    package_data={"rightmove_webscraper": ["docs/*", "docs/*/*"]}
)
