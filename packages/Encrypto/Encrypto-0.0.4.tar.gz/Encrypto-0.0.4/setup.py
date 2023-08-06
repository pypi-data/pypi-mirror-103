from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'Encrypting strings'
LONG_DESCRIPTION = 'A package that allows the Encryption or Decryption of data.'

# Setting up
setup(
    name="Encrypto",
    version=VERSION,
    author="Moritz Schittenhelm",
    author_email="moritz5911@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', "Encrypto", "encryption", "coding"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
