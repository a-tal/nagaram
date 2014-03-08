"""Anagram finding functions."""


from nagaram.scrabble import blank_tiles, word_list, word_score


def _letter_map(word):
    """Creates a map of letter use in a word.

    Args:
        word: a string to create a letter map from

    Returns:
        a dictionary of {letter: integer count of letter in word}
    """

    lmap = {}
    for letter in word:
        try:
            lmap[letter] += 1
        except KeyError:
            lmap[letter] = 1
    return lmap


def anagrams_in_word(word, sowpods=False, start="", end=""):
    """Finds anagrams in word.

    Args:
        word: the string to base our search off of
        sowpods: boolean to declare TWL or SOWPODS words file
        start: a string of starting characters to find anagrams based on
        end: a string of ending characters to find anagrams based on

    Yields:
        a tuple of (word, score) that can be made with the input_word
    """

    input_letters, blanks, questions = blank_tiles(word)

    for tile in start + end:
        input_letters.append(tile)

    for word in word_list(sowpods, start, end):
        lmap = _letter_map(input_letters)
        used_blanks = 0
        for letter in word:
            if letter in lmap:
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
            yield (word, word_score(word, input_letters, questions))
