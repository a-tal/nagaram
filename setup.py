"""Setup.py for nagaram."""


import io
import re
from setuptools import setup
from setuptools.command.test import test as TestCommand


def find_version(filename):
    """Uses re to pull out the assigned value to __version__ in filename."""

    with io.open(filename, encoding="utf-8") as version_file:
        version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                                  version_file.read(), re.M)
    if version_match:
        return version_match.group(1)
    return "0.0-version-unknown"


class PyTest(TestCommand):
    """Shim in pytest to be able to use it with setup.py test."""

    def finalize_options(self):
        """Stolen from http://pytest.org/latest/goodpractises.html."""

        TestCommand.finalize_options(self)
        self.test_args = (
            "-v -rf --cov-report term-missing --cov nagaram".split()
        )
        self.test_suite = True

    def run_tests(self):
        """Also shamelessly stolen."""

        # have to import here, outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


setup(
    name='nagaram',
    version=find_version("nagaram/__init__.py"),
    author='Adam Talsma',
    author_email='adam@talsma.ca',
    package_data={"nagaram": ['wordlists/twl.txt', 'wordlists/sowpods.txt']},
    include_package_data=True,
    packages=['nagaram'],
    entry_points={'console_scripts': ['nagaram = nagaram.cmdline:main']},
    url='https://github.com/a-tal/nagaram',
    zip_safe=False,
    description='Scrabble anagram finder',
    long_description=(
        "Scrabble anagram finder. Returns words based on Scrabble score. Works"
        " with both Tournament Words List and SOWPODS."
    ),
    download_url='https://github.com/a-tal/nagaram',
    tests_require=['pytest', 'pytest-cov'],
    cmdclass={'test': PyTest},
    license="BSD",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities',
    ],
)
