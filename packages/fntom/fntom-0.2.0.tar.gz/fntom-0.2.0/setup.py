from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "fntom", 
    version = "0.2.0",
    author = "Milan Petrík",
    author_email = "milan.petrik@protonmail.com",
    description = "Implements a finite, negative, totally ordered monoid together with methods to compute its one-element Rees coextensions",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "GPLv3",
    url = "https://gitlab.com/petrikm/fntom",
    packages = find_packages(),
    install_requires = [],
    python_requires = ">=3.6",
    keywords = ["discrete triangular norm", "finite negative totally ordered monoid", "Rees coextension", "Rees congruence", "Reidemeister closure condition", "tomonoid partition"],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Science/Research",
    ]
)
