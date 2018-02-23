from distutils.core import setup

long_description = """A simple class for scraping data from the UK's most prominent property sales & lettings listings website, www.rightmove.co.uk

The package is intended for use by data analysts/scientists who require easy access to download property listing data in nicely formatted Pandas DataFrames ready for analysis.
"""

setup(
    name = 'rightmove_webscraper',
    packages = ['rightmove_webscraper'], # Must be same as name
    version = '0.1',
    description = 'A class for scraping data from rightmove.co.uk',
    long_description = long_description,
    author = 'Toby Petty',
    author_email = 'hello@tobypetty.com',
    url = 'https://github.com/woblers/rightmove_webscraper.py',
    # This specifies which other Pip packages your package
    # requires to be installed:
    install_requires = [
      'pandas',
      'requests',
      'lxml'
    ],
    keywords = ['webscraping', 'rightmove', 'data'],
    license='MIT',
    classifiers=[
      # For full list of relevant classifiers, see:
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      
      # How mature is this project?
      'Development Status :: 4 - Beta',
      
      # Who is the project intended for?
      'Intended Audience :: End Users/Desktop',
      
      # Pick license (should match "license" above)
      'License :: OSI Approved :: MIT License',
      
      # Specify Python versions supported. In particular, ensure
      # to indicate whether you support Python 2, Python 3 or both.
      'Programming Language :: Python :: 3.6',
    ],
)