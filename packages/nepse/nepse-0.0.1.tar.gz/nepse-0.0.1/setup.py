from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Python Wrapper for Newweb Nepse'
LONG_DESCRIPTION = 'Nepse.py allows you to get realtime market prices and stats off nepse.'

# Setting up
setup(
    name="nepse",
    version=VERSION,
    author="FRAPPÉ (FRAPPÉ#4101)",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'nepse', 'stock', 'nepal stock', 'nepal stock prices', 'nepse pythonb']
)