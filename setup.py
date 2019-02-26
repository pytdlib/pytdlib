"""The setup and build script for the pytdlib library."""

from setuptools import setup, find_packages
import os
import re


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join('pytdlib', 'version.py'), encoding='utf-8') as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

setup(
    name="Pytdlib",
    version=version,
    description="Telegram TDLib Client Library for Python",
    long_description=long_description,

    url="https://github.com/pytdlib/pytdlib",

    author="Naji",

    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="telegram chat td tdlib api client library python mtproto",
    python_requires="~=3.4",
    packages=find_packages(),
)
