import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="MRItoolkit",
    version="21.4.22.2",
    description="This package provides useful tools for MRI reconstruction in python",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Ali Nahardani",
    author_email="nahardani.ali@gmail.com",
    url="https://gitlab.com/nahardani.ali/python_recons_medphys/",
    packages=find_packages(),
    install_requires=["nbconvert", "notebook","numpy","pandas","matplotlib","scipy","more-itertools","mpld3","pynufft","scikit-image","sigpy","napari[all]"],
    include_package_data=True
)
