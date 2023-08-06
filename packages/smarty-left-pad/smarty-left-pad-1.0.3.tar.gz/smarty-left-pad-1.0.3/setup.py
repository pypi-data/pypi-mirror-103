#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup
from setuptools.command.install import install

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
readme_files = ["README.md"]
for readme in readme_files:
    if os.path.exists(os.path.abspath(readme)):
        with open(os.path.join(here, readme), encoding="utf-8") as f:
            long_description = f.read()

scripts = []
for dirname, dirnames, filenames in os.walk("scripts"):
    for filename in filenames:
        scripts.append(os.path.join(dirname, filename))

# Package meta-data.
AUTHOR = "Nirmal Chandra"
AUTHOR_EMAIL = "nirmal.fleet@gmail.com"
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "Programming Language :: Python :: 3.8",
]
DESCRIPTION = "Dynamic left pad creator"
GHUSERNAME = "nirmalchandra"
KEYWORDS = "leftpad left pad utility smarty-left-pad"
LICENSE = "Apache 2.0"
LONG_DESCRIPTION = long_description
NAME = "smarty-left-pad"

# Define all install and test requirements
REQUIRED = []
SETUP_REQ = []

REQUIRES_PYTHON = "~=3.8"
SCRIPTS = scripts
SOURCE = f"https://github.com/{GHUSERNAME}/smarty-left-pad/"
URL = f"https://github.com/{GHUSERNAME}/smarty-left-pad"
THANKS_URL = f"https://github.com/{GHUSERNAME}/smarty-left-pad"
ABOUTME_URL = "https://github.com/{GHUSERNAME}"
VERSION = None

EXTRAS = {  }


# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


def _printer(msg, hashx=28):
    print("\n")
    print("#" * 80)
    print("#" * hashx, msg, "#" * hashx)
    print("#" * 80)
    print("\n")


def _post_install():
    cmd = "".join(SCRIPTS).split("/")[-1]
    _printer("Installation Complete!")
    print(f"If you would like tab-completion on {cmd}")
    print("Run the following commands in your terminal:\n")
    print("\t activate-global-python-argcomplete --user")
    print(f'\t eval "$(register-python-argcomplete {cmd})"')
    _printer("Done! ", 36)


class PostInstallCommand(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(_post_install)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        try:
            import twine
        except ImportError:
            errmsg = ("\n'Twine' is not installed.\n\nRun: \n\tpip install twine")
            self.status(errmsg)
            raise SystemExit(1)

        self.status("Building Source and Wheel (universal) distribution...")
        # os.system('{0} setup.py sdist --universal'.format(sys.executable))
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags... (not really)")
        os.system(f"git tag v{about['__version__']}")
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    setup_requires=SETUP_REQ,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    scripts=SCRIPTS,
    project_urls={
        "Bug Reports": SOURCE + "/issues",
        "Source": SOURCE,
        "Say Thanks!": THANKS_URL,
        "AboutMe": ABOUTME_URL,
    },
    cmdclass={"upload": UploadCommand, "install": PostInstallCommand},
    test_suite="tests"
)