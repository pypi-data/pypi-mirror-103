from setuptools import find_packages, setup
from my_pip_pkg import __version__
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='nik_nik',
    version="1.0.1",

    description="A demo peoject for CS253 presentation",
    url='https://demo_project.com/dummy.xml',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Nikita',
    author_email='nikitachauhan622@gmail.com',
    install_requires=["numpy"],
    packages=find_packages(),
)
