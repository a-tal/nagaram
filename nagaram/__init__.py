"""Nagaram. Scrabble word anagram finder.

Usage:
    nagaram [--sowpods] [-l] [-s chars] [-e chars] <letters>

? can be used to represent another tile on the board to play on
_ can be used to represent blank tiles in your rack (no points)

By default it will use the Tournament Words List. The --sowpods command line
variable is available to use the SOWPODS words list.

The -l or --length flag if used will print the anagrams sorted by tiles used,
rather than the default of by Scrabble score.

The -s flag can be used to provide starting characters already on the board,
similarily the -e flag can be used for ending characters.
"""


__version__ = "0.3.3"
__release_date__ = "May 2, 2014"
