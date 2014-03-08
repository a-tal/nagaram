#coding: utf-8


"""Tests for nagaram's scrabble calculations."""


import os
import unittest

from nagaram.scrabble import (
    blank_tiles,
    valid_scrabble_word,
    word_list,
    word_score,
    letter_score,
)


def _call_word_list(*args, **kwargs):
    """Call word_list but insider the test wordlist directory location."""

    location = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(
        __file__)))),
        "wordlists",
    )
    kwargs.update({"location": location})
    return word_list(*args, **kwargs)


class ScrabbleTests(unittest.TestCase):
    """TestCases for Scrabble(tm) related functions."""
    def test_basic_word_scores(self):
        """Some simple use cases, count the scores correctly."""

        test_data = [
            ("adam", 7),
            ("python", 14),
            ("qwerty", 21),
        ]

        for word, score in test_data:
            rack = [letter for letter in word]
            self.assertEqual(word_score(word, rack), score)

    def test_bingo_for_using_full_rack(self):
        """Ensure we get the extra 50 points for using all our tiles."""

        test_data = [
            ("tornado", 58),
            ("watches", 65),
        ]

        for word, score in test_data:
            rack = [letter for letter in word]
            self.assertEqual(word_score(word, rack), score)

    def test_built_on_points_counted(self):
        """Our score should contain the points of tiles we built on."""

        word = "yesterday"
        rack = ["y", "e", "s", "t", "e", "r", "d"]

        self.assertEqual(word_score(word, rack, questions=2), 66)

    def test_blank_tiles_not_counted(self):
        """Blank tiles score no points."""

        word = "elephant"
        rack = ["e", "_", "e", "p", "h", "a", "n", "t"]

        self.assertEqual(word_score(word, rack), 62)

    def test_prefer_to_use_questions(self):
        """If given the chance to play on the board vs a blank tile, do it."""

        word = "short"
        rack = ["s", "h", "_", "r", "t"]

        self.assertEqual(word_score(word, rack, questions=1), 8)

    def test_impossible_word_in_rack(self):
        """This should return 0, because you're a cheater."""

        word = "madhacker"
        rack = ["q", "p", "i", "i", "x", "n", "y"]

        self.assertEqual(word_score(word, rack), 0)

    def test_blank_tile_parse(self):
        """Should parse out underscores as blanks, verify returns."""

        test_data = {
            "so_me?h?ng": (["s", "o", "m", "e", "h", "n", "g"], 1, 2,),
            "w___r?ds": (["w", "r", "d", "s"], 3, 1),
            "mmhmm": (["m", "m", "h", "m", "m"], 0, 0),
        }

        for word, results in test_data.items():
            expected_letters, expected_blanks, expected_questions = results
            letters, blanks, questions = blank_tiles(word)
            self.assertEqual(expected_letters, letters)
            self.assertEqual(expected_blanks, blanks)
            self.assertEqual(expected_questions, questions)

    def test_word_list_basic(self):
        """Ensure we're getting the words we should be."""

        for word in _call_word_list():
            self.assertEqual("aa", word)
            break

        for word in _call_word_list(sowpods=True):
            self.assertEqual("aa", word)
            break

    def test_word_list_starting(self):
        """Test getting words starting with some characters."""

        starting_characters = "saxifr"
        for word in _call_word_list(start=starting_characters):
            self.assertEqual("saxifrage", word)
            break

        for word in _call_word_list(sowpods=True, start=starting_characters):
            self.assertEqual("saxifragaceous", word)
            break

    def test_word_list_ending(self):
        """Test getting words ending with some characters."""

        ending_characters = "stylar"
        for word in _call_word_list(end=ending_characters):
            self.assertEqual("astylar", word)
            break

        for word in _call_word_list(sowpods=True, end=ending_characters):
            self.assertEqual("amphiprostylar", word)
            break

    def test_both_start_and_end(self):
        """Test specifying both the start and the end."""

        starting = "ab"
        ending = "nally"
        for word in _call_word_list(start=starting, end=ending):
            self.assertEqual("abdominally", word)
            break

        for word in _call_word_list(sowpods=True, start=starting, end=ending):
            self.assertEqual("abactinally", word)
            break

    def test_valid_scrabble_word(self):
        """Confirm a word's validity given a full bag of tiles."""

        test_data = [
            ("aabbccdd", True),
            ("????????????zyx__", True),
            ("????????????zyx___", False),
            ("zzabcdef", True),  # second z is assumed to be a blank
            ("zzzabcdef", True),  # there are two blanks
            ("zzzzabcdef", False),  # now it should return False
            ("xuyxj_ics_", False),
            ("ifoxfxajxk_cw", False),
            ("abcdefghijklmnopqrstuvwxyz_?", True),
        ]

        for word, expected_result in test_data:
            self.assertEqual(
                valid_scrabble_word(word),
                expected_result,
                "{0} is {1}a valid scrabble word, but it should {2}be.".format(
                    word,
                    "not " * int(expected_result),
                    "not " * int(not expected_result),
                )
            )

    def test_unicode_word_is_invalid(self):
        """How many points for a unicode hamburger?"""

        self.assertFalse(valid_scrabble_word("yummy_🍔"))

    def test_unicode_letter_raises(self):
        """Confirm letter_score is the one who raises TypeErrors."""

        for letter in ["🍔", ".", "4", ")"]:
            with self.assertRaises(TypeError):
                letter_score(letter)


if __name__ == "__main__":
    unittest.main()
