import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
 name="cmc_csci046_.data_structures",
 version="1.0.3",
 description="Implement efficent data structures",
 long_description=README,
 url="https://github.com/michaelhess17/containers-oop/tree/master",
 author="Michael Hess",
 author_email="mhess21@cmc.edu",
 license="MIT",
 classifiers=[
     "License :: OSI Approved :: MIT License",
     "Programming Language :: Python :: 3",
     "Programming Language :: Python :: 3.7",
             ],
 packages=["containers"],
 include_package_data=True,
 long_description_content_type='text/markdown',
 install_requires=["pytest", "attrs", "hypothesis"])
