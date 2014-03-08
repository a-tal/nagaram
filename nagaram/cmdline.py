"""Command line entry and exit points."""


from __future__ import print_function, unicode_literals

import sys
import argparse

import nagaram
from nagaram.anagrams import anagrams_in_word
from nagaram.scrabble import valid_scrabble_word


def pretty_print(input_word, anagrams, by_length=False):
    """Prints the anagram results sorted by score to stdout.

    Args:
        input_word: the base word we searched on
        anagrams: generator of (word, score) from anagrams_in_word
        by_length: a boolean to declare printing by length instead of score
    """

    scores = {}
    if by_length:
        noun = "tiles"
        for word, score in anagrams:
            try:
                scores[len(word)].append("{0} ({1:d})".format(word, score))
            except KeyError:
                scores[len(word)] = ["{0} ({1:d})".format(word, score)]
    else:
        noun = "points"
        for word, score in anagrams:
            try:
                scores[score].append(word)
            except KeyError:
                scores[score] = [word]

    print("Anagrams for {0}{1}:".format(input_word, " (score)" * by_length))

    if not valid_scrabble_word(input_word):
        print("{0} is not possible in Scrabble.".format(input_word))

    for key, value in sorted(scores.items(), reverse=True):
        print("{0:d} {1}: {2}".format(key, noun, ", ".join(value)))


def argument_parser(args):
    """Argparse logic, command line options.

    Args:
        args: sys.argv[1:], everything passed to the program after its name

    Returns:
        A tuple of:
            a list of words/letters to search
            a boolean to declare if we want to use the sowpods words file
            a boolean to declare if we want to output anagrams by length
            a string of starting characters to find anagrams based on
            a string of ending characters to find anagrams based on

    Raises:
        SystemExit if the user passes invalid arguments, --version or --help
    """

    parser = argparse.ArgumentParser(
        prog="nagaram",
        description="Finds Scabble anagrams.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "-h", "--help",
        dest="help",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--sowpods",
        dest="sowpods",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--length",
        "-l",
        dest="length",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--starts-with",
        "-s",
        dest="starts_with",
        metavar="chars",
        default="",
        nargs=1,
        type=str,
    )

    parser.add_argument(
        "--ends-with",
        "-e",
        dest="ends_with",
        metavar="chars",
        default="",
        nargs=1,
        type=str,
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="Nagaram {0} (Released: {1})".format(
            nagaram.__version__,
            nagaram.__release_date__,
        )
    )

    parser.add_argument(
        dest="wordlist",
        metavar="letters to find anagrams with (? for anything, _ for blanks)",
        nargs=argparse.REMAINDER,
    )

    settings = parser.parse_args(args)

    if settings.help:
        raise SystemExit(nagaram.__doc__.strip())

    if not settings.wordlist:
        raise SystemExit(parser.print_usage())

    if settings.starts_with:
        settings.starts_with = settings.starts_with[0]
    if settings.ends_with:
        settings.ends_with = settings.ends_with[0]

    return (settings.wordlist, settings.sowpods, settings.length,
            settings.starts_with, settings.ends_with)


def main(arguments=None):
    """Main command line entry point."""

    if not arguments:
        arguments = sys.argv[1:]

    wordlist, sowpods, by_length, start, end = argument_parser(arguments)
    for word in wordlist:
        pretty_print(
            word,
            anagrams_in_word(word, sowpods, start, end),
            by_length,
        )
