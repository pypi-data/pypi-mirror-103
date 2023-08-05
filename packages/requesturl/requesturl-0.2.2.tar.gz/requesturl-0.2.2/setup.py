#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "free-proxy==1.0.2", "Proxy-List-Scrapper==0.2.2"]

setup_requirements = []

test_requirements = []

setup(
    author="Yasir Erkam Özdemir",
    author_email="yasir.erkam17@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Request URL",
    entry_points={
        "console_scripts": [
            "requesturl=requesturl.cli:main",
        ],
    },
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="requesturl",
    name="requesturl",
    packages=find_packages(include=["requesturl", "requesturl.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/yasirerkam/requesturl",
    version="0.2.2",
    zip_safe=False,
    license="Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)",
)
