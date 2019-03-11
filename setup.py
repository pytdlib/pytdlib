"""The setup and build script for the pytdlib library."""

from setuptools import setup, find_packages, Command
from sys import argv
import shutil
import os
import re

from generate.api import generator

if len(argv) > 1 and argv[1] in ["bdist_wheel", "install"]:
    generator.start()


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join("pytdlib", "version.py"), encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]


class Clear(Command):
    DIST = ["./build", "./dist", "./Pytdlib.egg-info"]
    API = ["pytdlib/api/functions", "pytdlib/api/types"]
    ALL = DIST + API

    description = "Clean generated files"

    user_options = [
        ("dist", None, "Clean distribution files"),
        ("api", None, "Clean generated API files"),
        ("all", None, "Clean all generated files"),
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.dist = None
        self.api = None
        self.all = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        paths = set()

        if self.dist:
            paths.update(Clear.DIST)

        if self.api:
            paths.update(Clear.API)

        if self.all or not paths:
            paths.update(Clear.ALL)

        for path in sorted(list(paths)):
            try:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            except OSError:
                print("skipping {}".format(path))
            else:
                print("removing {}".format(path))


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
    cmdclass={
        "clean": Clear,
    }
)
