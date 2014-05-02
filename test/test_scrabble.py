#coding: utf-8
"""Tests for nagaram's scrabble calculations."""


import pytest

import nagaram
from nagaram.scrabble import (
    blank_tiles,
    valid_scrabble_word,
    word_list,
    word_score,
    letter_score,
)


@pytest.mark.parametrize("word,score", (
    ("adam", 7),
    ("python", 14),
    ("qwerty", 21),
    ("tornado", 58),
    ("watches", 65),
))
def test_word_scores(word, score):
    """Some simple use cases, count the scores correctly, includes bingos."""

    assert word_score(word, [letter for letter in word]) == score


def test_built_on_points_counted():
    """Our score should contain the points of tiles we built on."""

    word = "yesterday"
    rack = ["y", "e", "s", "t", "e", "r", "d"]
    assert word_score(word, rack, questions=2) == 66


def test_blank_tiles_not_counted():
    """Blank tiles score no points."""

    word = "elephant"
    rack = ["e", "_", "e", "p", "h", "a", "n", "t"]
    assert word_score(word, rack) == 62


def test_prefer_to_use_questions():
    """If given the chance to play on the board vs a blank tile, do it."""

    word = "short"
    rack = ["s", "h", "_", "r", "t"]
    assert word_score(word, rack, questions=1) == 8


def test_impossible_word_in_rack():
    """This should return 0, because you're a cheater."""

    word = "madhacker"
    rack = ["q", "p", "i", "i", "x", "n", "y"]

    assert word_score(word, rack) == 0


def test_blank_tile_parse():
    """Should parse out underscores as blanks, verify returns."""

    test_data = {
        "so_me?h?ng": (["s", "o", "m", "e", "h", "n", "g"], 1, 2,),
        "w___r?ds": (["w", "r", "d", "s"], 3, 1),
        "mmhmm": (["m", "m", "h", "m", "m"], 0, 0),
    }

    for word, results in test_data.items():
        expected_letters, expected_blanks, expected_questions = results
        letters, blanks, questions = blank_tiles(word)
        assert expected_letters == letters
        assert expected_blanks == blanks
        assert expected_questions == questions


@pytest.mark.parametrize(
    "starting,ending,twl_expected,sowpods_expected",
    (
        (None, None, "aa", "aa"),
        ("saxifr", None, "saxifrage", "saxifragaceous"),
        (None, "stylar", "astylar",  "amphiprostylar"),
        ("ab", "nally", "abdominally", "abactinally"),
    ),
    ids=("basic", "starting", "ending", "both")
)
def test_word_lists(starting, ending, twl_expected, sowpods_expected):
    """Ensure we're getting the first words we should be."""

    for word in word_list(start=starting, end=ending):
        assert twl_expected == word
        break

    for word in word_list(start=starting, end=ending, sowpods=True):
        assert sowpods_expected == word
        break


@pytest.mark.parametrize("word, valid", [
    ("aabbccdd", True),
    ("????????????zyx__", True),
    ("????????????zyx___", False),
    ("zzabcdef", True),  # second z is assumed to be a blank
    ("zzzabcdef", True),  # there are two blanks
    ("zzzzabcdef", False),  # now it should return False
    ("xuyxj_ics_", False),
    ("ifoxfxajxk_cw", False),
    ("abcdefghijklmnopqrstuvwxyz_?", True),
])
def test_valid_scrabble_word(word, valid):
    """Confirm a word's validity given a full bag of tiles."""

    assert valid_scrabble_word(word) == valid


def test_unicode_word_is_invalid():
    """How many points for a unicode hamburger?"""

    assert not valid_scrabble_word("yummy_🍔")


@pytest.mark.parametrize("letter", ("🍔", ".", "4", ")"))
def test_unicode_letter_raises(letter):
    """Confirm letter_score is the one who raises TypeErrors."""

    with pytest.raises(TypeError):
        letter_score(letter)
