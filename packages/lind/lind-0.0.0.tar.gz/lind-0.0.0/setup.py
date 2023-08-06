#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup file for package install
"""

import re
from setuptools import setup, find_namespace_packages

################################################################################

# Note: setup.cfg is set up to only recognise tags starting with v

# Update Version Tag in Github
"""
git describe --tags # gets the current tag
git tag v0.0.015rc # update the tag to something, e.g. v0.0.01
git push origin --tags # push update to branch
"""

# Release New Version in PyPi and Update Docs
"""
conda activate python_env
rm -rf build;rm -rf dist;rm -rf *.info;rm -rf *.egg-info
python3 -m pip install --user --upgrade setuptools wheel && python3 setup.py sdist bdist_wheel
python3 -m twine upload --verbose --repository-url https://upload.pypi.org/legacy/ dist/*
cd docs && make html # update docs
"""

# Convenient cleanup script
"""
rm -rf build;rm -rf dist;rm -rf *.info;rm -rf *.egg-info;rm -rf .coverage; rm -rf .pytest_cache
"""

################################################################################

def fetch_version(VERSIONFILE):
    """ Convenience Function """
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)

    mo = ""
    if mo:
        verstr = mo.group(1)
    else:
        verstr = None

    return verstr

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


def read_text(file_name: str):
    """ Convenience Function """
    return open(file_name).read()


################################################################################


def install_r_packages():
    """
    Install required R packages dependencies.

    Developer Comments:

    I hate triggering this dependency install in this fashion. I originally
    tried using `--install-options`. However `pip install lind[rpy2] --install-options'--quailtyTools'`
    passed the install option to rpy2 instead of my custom cmdclass for install
    cauing install errors.

    https://stackoverflow.com/questions/18725137/how-to-obtain-arguments-passed-to-setup-py-from-pip-with-install-option

    I could have also used extras_require to trigger a custom function that
    installed rpy2 using a subprocess and then used rpy2 to install the r dependencies. That seemed like an antipattern.

    https://stackoverflow.com/questions/49870594/pip-main-install-fails-with-module-object-has-no-attribute-main

    Faced with all bad options, I chose this install mechanism instead.
    """
    try:
        from rpy2.robjects import r
        #r('install.packages("qualityTools", repos="http://cran.us.r-project.org")');
        r('install.packages("https://cran.r-project.org/src/contrib/Archive/qualityTools/qualityTools_1.54.tar.gz")');
    except:
        #r('remove.packages("qualityTools")');
        pass


################################################################################


def setup_package():
    """
    Function to manage setup procedures.

    >>> pip install -U "lind[tests, r_backends, static_designs]"
    >>> pip install -e ".[tests, r_backends, static_designs]"
    >>> pip uninstall lind -y

    """

    setup(
        name="lind",
        packages=find_namespace_packages(),
        version=fetch_version(VERSIONFILE="./lind/_version.py"),

        author="James Montgomery",
        author_email="jamesoneillmontgomery@gmail.com",
        description="Package for experiment design and analysis.",
        long_description=read_text("README.md"),
        long_description_content_type="text/markdown",
        license=read_text("LICENSE.md"),

        python_requires=">=3.6",
        platforms='any',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],

        setup_requires=['wheel'],
        install_requires=parse_requirements("requirements.txt"),
        extras_require={
            "tests": parse_requirements("requirements_test.txt"),
            "r_backends": ["rpy2==3.3.5"],
            "static_designs": ["lind-static-resources==0.0.6"]
        },
        cmdclass={},

        package_data={
            '': ['*.csv']
        },

    )

    # will automatically install R package dependencies if rpy2 is installed
    install_r_packages()


if __name__ == "__main__":
    setup_package()
