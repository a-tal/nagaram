from distutils.core import setup

setup(
    name='nagaram',
    version='0.2.0',
    author='Adam Talsma',
    author_email='adam@talsma.ca',
    package_dir={'nagaram': 'src'},
    data_files=[('/usr/share/nagaram', ['src/twl.txt', 'src/sowpods.txt'])],
    packages=['nagaram'],
    provides=['nagaram'],
    requires=['argparse'],
    scripts=['bin/nagaram'],
    url='https://github.com/a-tal/nagaram',
    description='Scrabble anagram finder',
    long_description=(
        "Scrabble anagram finder. Returns words based on Scrabble score. Works"
        " with both Tournament Words List and SOWPODS."
    ),
    download_url='https://github.com/a-tal/nagaram',
    license="GPL3+",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities',
    ],
)
