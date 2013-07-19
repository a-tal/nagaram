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

Bugs, comments or feedback can be sent to adam@talsma.ca

(c) 2013 Adam Talsma

Released under the GPL3+

Written for Python 3.3
"""


import os
import sys
import argparse


def pretty_print(input_word, anagrams, by_length=False):
    """Prints the anagram results sorted by score to stdout.

    Args:
        input_word: the base word we searched on
        anagrams: a list of anagrams from find_anagrams
        by_length: a boolean to declare printing by length instead of score
    """

    print("Anagrams for {}{}:".format(
        input_word,
        " (score)" * by_length,
    ))

    if not valid_scrabble_word(input_word):
        print("{} is not possible in Scrabble.".format(input_word))

    if by_length:
        length_map = dict()
        for word, score in anagrams:
            try:
                length_map[len(word)].append("{} ({:d})".format(word, score))
            except KeyError:
                length_map[len(word)] = ["{} ({:d})".format(word, score)]
        for key, value in sorted(length_map.items(), reverse=True):
            print("{:d} tiles: {}".format(key, ', '.join(value)))
    else:
        score_map = dict()
        for word, score in anagrams:
            try:
                score_map[score].append(word)
            except KeyError:
                score_map[score] = [word]
        for key, value in sorted(score_map.items(), reverse=True):
            print("{:d} points: {}".format(key, ', '.join(value)))


def argument_parser(args):
    """Argparse logic, command line options.

    Args:
        args: sys.argv[1:], everything passed to the program after its name

    Returns:
        A tuple of:
            a list of words/letters to search
            a boolean to declare if we want to use the sowpods words file
            a boolean to declare if we want to output anagrams by length
            a string or false to find anagrams based on starting characters
            a string or false to find anagrams based on ending characters

    Raises:
        SystemExit if the user passes invalid arguments, --version or --help
    """

    parser = argparse.ArgumentParser(
        prog='nagaram',
        description='Finds Scabble anagrams.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '--sowpods',
        dest='sowpods',
        action='store_true',
        default=False,
    )

    parser.add_argument(
        '--length',
        '-l',
        dest='length',
        action='store_true',
        default=False,
    )

    parser.add_argument(
        '--starts-with',
        '-s',
        dest='starts_with',
        metavar="chars",
        default=False,
        nargs=1,
        type=str,
    )

    parser.add_argument(
        '--ends-with',
        '-e',
        dest='ends_with',
        metavar="chars",
        default=False,
        nargs=1,
        type=str,
    )

    parser.add_argument(
        '--version',
        '-v',
        action='version',
        version="""Nagaram 0.1.1 (Released: July 18, 2013)
Copyright (C) 2013 Adam Talsma <adam@talsma.ca>
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.""",
    )

    parser.add_argument(
        dest='wordlist',
        metavar="letters to find anagrams with (? for anything, _ for blanks)",
        nargs=argparse.REMAINDER,
    )

    settings = parser.parse_args(args)

    if not settings.wordlist:
        raise SystemExit(parser.print_usage())

    if settings.starts_with:
        settings.starts_with = settings.starts_with[0]
    if settings.ends_with:
        settings.ends_with = settings.ends_with[0]

    return (settings.wordlist, settings.sowpods, settings.length,
            settings.starts_with, settings.ends_with)


def valid_scrabble_word(word):
    """Checks if the input word could be played with a full bag of tiles.

    Returns:
        True or false
    """

    letters_in_bag = {
        "a": 9,
        "b": 2,
        "c": 2,
        "d": 4,
        "e": 12,
        "f": 2,
        "g": 3,
        "h": 2,
        "i": 9,
        "j": 1,
        "k": 1,
        "l": 4,
        "m": 2,
        "n": 6,
        "o": 8,
        "p": 2,
        "q": 1,
        "r": 6,
        "s": 4,
        "t": 6,
        "u": 4,
        "v": 2,
        "w": 2,
        "x": 1,
        "y": 2,
        "z": 1,
        "_": 2,
    }

    for letter in word:
        if letter == "?":
            continue
        try:
            letters_in_bag[letter] -= 1
        except KeyError:
            return False
        if letters_in_bag[letter] < 0:
            letters_in_bag["_"] -= 1
            if letters_in_bag["_"] < 0:
                return False
    return True


def word_list(sowpods=False, start=False, end=False):
    """Opens the word list file.

    Args:
        sowpods: a boolean to declare using the sowpods list or twl (default)
        start: a string or false to find anagrams based on starting characters
        end: a string or false to find anagrams based on ending characters

    Returns:
        a large list of words. 178691 by default, 267751 if sowpods=True. Much
        less if either start or end are used (filtering is applied here)
    """

    if sowpods:
        filename = "sowpods.txt"
    else:
        filename = "twl.txt"

    cwd = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(cwd, filename)

    wordlist = list()
    with open(filepath) as wordfile:
        for word in wordfile.readlines():
            word = word.strip()
            if start and end and word.startswith(start) and word.endswith(end):
                wordlist.append(word)
            elif start and word.startswith(start) and not end:
                wordlist.append(word)
            elif end and word.endswith(end) and not start:
                wordlist.append(word)
            elif not start and not end:
                wordlist.append(word)
    return wordlist


def find_anagrams(input_word, sowpods=False, start=False, end=False):
    """Finds anagrams in input_word.

    Args:
        input_word: the string to base our search off of
        sowpods: boolean to declare TWL or SOWPODS words file
        start: a string or false to find anagrams based on starting characters
        end: a string or false to find anagrams based on ending characters

    Returns:
        a list of tuples (word, score) that can be made with the input_word
    """

    anagrams = list()
    for word in word_list(sowpods, start, end):
        input_letters, blanks, questions = _blank_tiles(input_word)
        if start:
            for tile in start:
                input_letters.append(tile)
        if end:
            for tile in end:
                input_letters.append(tile)
        lmap = _letter_map(input_letters)
        used_blanks = 0
        for letter in word:
            if letter in lmap.keys():
                lmap[letter] -= 1
                if lmap[letter] < 0:
                    used_blanks += 1
                    if used_blanks > (blanks + questions):
                        break
            else:
                used_blanks += 1
                if used_blanks > (blanks + questions):
                    break
        else:
            score = word_score(word, input_letters, questions)
            anagrams.append((word, score))
    return anagrams


def _blank_tiles(input_word):
    """Searches a string for blank tile characters ("?" and "_").

    Args:
        input_word: the user supplied string to search through

    Returns:
        a tuple of:
            input_word without blanks
            integer number of blanks (no points)
            integer number of questions (points)
    """

    blanks = 0
    questions = 0
    input_letters = list()
    for letter in input_word:
        if letter == "_":
            blanks += 1
        elif letter == "?":
            questions += 1
        else:
            input_letters.append(letter)
    return input_letters, blanks, questions


def _letter_map(word):
    """Creates a map of letter use in a word.

    Args:
        word: a string to create a letter map from

    Returns:
        a dictionary of letter: integer count of letter in word
    """

    lmap = dict()
    for letter in word:
        try:
            lmap[letter] += 1
        except KeyError:
            lmap[letter] = 1
    return lmap


def word_score(word, input_letters, questions=0):
    """Checks the Scrabble score of a single word.

    Args:
        word: a string to check the Scrabble score of
        input_letters: the letters in our rack
        questions: integer of the tiles already on the board to build on

    Returns:
        an integer Scrabble score amount for the word
    """

    score = 0
    bingo = 0
    filled_by_blanks = list()
    for letter in word:
        if letter in input_letters:
            bingo += 1
            score += _letter_score(letter)
            input_letters.remove(letter)
        else:
            filled_by_blanks.append(_letter_score(letter))

    # we can have both ?'s and _'s in the word. this will apply the ?s to the
    # highest scrabble score value letters and leave the blanks for low points.
    for blank_score in sorted(filled_by_blanks, reverse=True):
        if questions > 0:
            score += blank_score
            questions -= 1

    # 50 bonus points for using all the tiles in your rack
    if bingo > 6:
        score += 50

    return score


def _letter_score(letter):
    """Returns the Scrabble score of a letter.

    Args:
        letter: a single character string

    Raises:
        TypeError if a non-Scrabble character is supplied
    """

    if not isinstance(letter, str) or len(letter) != 1:
        raise TypeError("Invalid letter: %s", letter)

    score_map = {
        1: ["a", "e", "i", "o", "u", "l", "n", "r", "s", "t"],
        2: ["d", "g"],
        3: ["b", "c", "m", "p"],
        4: ["f", "h", "v", "w", "y"],
        5: ["k"],
        8: ["j", "x"],
        10: ["q", "z"],
    }

    for score, letters in score_map.items():
        if letter.lower() in letters:
            return score
    else:
        raise TypeError("Invalid letter: %s", letter)


def _find_all_anagrams():
    """Main command line entry point."""

    wordlist, sowpods, by_length, start, end = argument_parser(sys.argv[1:])
    for word in wordlist:
        pretty_print(word, find_anagrams(word, sowpods, start, end), by_length)


def main():
    """Main entry point."""

    try:
        _find_all_anagrams()
    except KeyboardInterrupt:
        raise SystemExit("Interrupted")


if __name__ == "__main__":
    main()
