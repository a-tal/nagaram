"""Setup.py for nagaram."""


from setuptools import setup
from setuptools.command.test import test as TestCommand


with open("nagaram/__init__.py", "r") as openinit:
    for line in openinit.readlines():
        if line.startswith("__version__ ="):
            __version__ = line[14:].replace('"', "").replace('"', "").strip()
            break
    else:
        __version__ = "0.0-version-unknown"


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
    version=__version__,
    author='Adam Talsma',
    author_email='adam@talsma.ca',
    data_files=[
        ('/usr/share/nagaram', ['wordlists/twl.txt', 'wordlists/sowpods.txt']),
    ],
    packages=['nagaram'],
    provides=['nagaram'],
    install_requires=['argparse'],
    scripts=['bin/nagaram'],
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
