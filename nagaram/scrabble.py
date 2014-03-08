"""Scrabble related functions, score counters, etc."""


import os


def letter_score(letter):
    """Returns the Scrabble score of a letter.

    Args:
        letter: a single character string

    Raises:
        TypeError if a non-Scrabble character is supplied
    """

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
    filled_by_blanks = []
    rack = list(input_letters)  # make a copy to speed up find_anagrams()
    for letter in word:
        if letter in rack:
            bingo += 1
            score += letter_score(letter)
            rack.remove(letter)
        else:
            filled_by_blanks.append(letter_score(letter))

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


def blank_tiles(input_word):
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
    input_letters = []
    for letter in input_word:
        if letter == "_":
            blanks += 1
        elif letter == "?":
            questions += 1
        else:
            input_letters.append(letter)
    return input_letters, blanks, questions


def word_list(sowpods=False, start="", end=""):
    """Opens the word list file.

    Args:
        sowpods: a boolean to declare using the sowpods list or TWL (default)
        start: a string of starting characters to find anagrams based on
        end: a string of ending characters to find anagrams based on

    Yeilds:
        a word at a time out of 178691 words for TWL, 267751 for sowpods. Much
        less if either start or end are used (filtering is applied here)
    """

    location = "/usr/share/nagaram"
    if not os.path.exists(location):
        location = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "wordlists",
        )

    if sowpods:
        filename = "sowpods.txt"
    else:
        filename = "twl.txt"

    filepath = os.path.join(location, filename)

    with open(filepath) as wordfile:
        for word in wordfile.readlines():
            word = word.strip()
            if start and end and word.startswith(start) and word.endswith(end):
                yield word
            elif start and word.startswith(start) and not end:
                yield word
            elif end and word.endswith(end) and not start:
                yield word
            elif not start and not end:
                yield word


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
