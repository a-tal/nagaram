nagaram
=======

[![Build Status](https://travis-ci.org/a-tal/nagaram.png?branch=master)](https://travis-ci.org/a-tal/nagaram)
[![Coverage Status](https://coveralls.io/repos/a-tal/nagaram/badge.png?branch=master)](https://coveralls.io/r/a-tal/nagaram?branch=master)
[![Stories in Backlog](https://badge.waffle.io/a-tal/nagaram.png?label=ready&title=Backlog)](https://waffle.io/a-tal/nagaram)
[![Stories In Progress](https://badge.waffle.io/a-tal/nagaram.png?label=ready&title=In+Progress)](https://waffle.io/a-tal/nagaram)
[![Version](https://pypip.in/v/nagaram/badge.png)](https://pypi.python.org/pypi/nagaram/)
[![Downloads this month](https://pypip.in/d/nagaram/badge.png)](https://pypi.python.org/pypi/nagaram/)

Scrabble anagram finder. Returns anagrams based on Scrabble score.

Usage
======

    nagaram [--sowpods] [-l] [-s chars] [-e chars] <letters>

? can be used to represent another tile on the board to play on  
_ can be used to represent blank tiles in your rack (no points)

By default it will use the Tournament Words List. The --sowpods command line
variable is available to use the SOWPODS words list.

The -l or --length flag if used will print the anagrams sorted by tiles used,
rather than the default of by Scrabble score.

The -s flag can be used to provide starting characters already on the board,
similarily the -e flag can be used for ending characters.


Install
=======

    $ git clone https://github.com/a-tal/nagaram
    $ cd nagaram
    $ python setup.py build
    $ sudo python setup.py install
    $ nagaram demo
    Anagrams for demo:
    7 points: demo, dome, mode
    6 points: dom, med, mod
    4 points: doe, em, me, mo, ode, om
    3 points: de, do, ed, od
    2 points: oe

Also available via pip or easyinstall.
