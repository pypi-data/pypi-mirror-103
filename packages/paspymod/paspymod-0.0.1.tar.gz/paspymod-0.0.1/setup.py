import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] 
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name="paspymod", 
    version="0.0.1",
    author="Andrew Schilling",
    author_email="andrew.schilling@centrify.com",
    description="Centrify PAS REST API Module to run scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajskrilla/pas_py_mod",
    packages=setuptools.find_packages(include=['paspymod']),    
    install_requires=install_requires,
    python_requires='>=3.6',
)
