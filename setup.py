"""Setup.py for nagaram."""


from setuptools import setup


setup(
    name='nagaram',
    version='0.3.2',
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
    description='Scrabble anagram finder',
    long_description=(
        "Scrabble anagram finder. Returns words based on Scrabble score. Works"
        " with both Tournament Words List and SOWPODS."
    ),
    download_url='https://github.com/a-tal/nagaram',
    tests_require=['nose'],
    test_suite='nose.collector',
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
