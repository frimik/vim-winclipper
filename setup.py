from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.exceptions import InstallationError

try:
    requirements = parse_requirements("requirements.txt")
    install_requires = [str(r.req) for r in requirements]
except InstallationError:
    install_requires = []

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="vim-winclipper",
    version="0.0.1",
    description="Vagrant VM vim register to Windows clipboard",
    license="MIT",
    author="Mikael Fridh",
    author_email="frimik@gmail.com",
    url="https://github.com/frimik/vim-winclipper",
    packages=find_packages(),
    install_requires=install_requires,
    long_description=long_description
)
