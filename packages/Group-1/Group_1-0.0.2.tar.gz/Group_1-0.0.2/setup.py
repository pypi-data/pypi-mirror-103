from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2"]

setup(
    name="Group_1",
    version="0.0.2",
    author="Varun Dutt",
    author_email="varun9213@gmail.com",
    description="A package for clustering",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://cseegit.essex.ac.uk/2020_ce903/ce903_team01/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
