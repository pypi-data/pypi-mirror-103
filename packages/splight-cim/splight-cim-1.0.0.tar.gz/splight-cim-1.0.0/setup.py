import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="splight-cim",
    version="1.0.0",
    description="Parse CIM RDF XML files and get output in JSON format",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/splight-dev/test/src/master/",
    author="Splight",
    author_email="splight@splight-ae.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["cimlib"],
    include_package_data=True,
)
