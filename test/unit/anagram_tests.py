"""Test anagram finding functions."""


import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


from nagaram.anagrams import anagrams_in_word

def _get_anagrams(word, sowpods=False, start="", end=""):
    """Run the anagrams_in_word generator until its done, return as a list."""

    return [result for result in anagrams_in_word(word, sowpods, start, end)]


class AnagramTests(unittest.TestCase):
    """Ensure we're finding the correct anagrams."""

    def test_twl_basic(self):
        """Simple TWL use case."""

        test_data = [
            ("word", 8),
            ("dow", 7),
            ("row", 6),
            ("wo", 5),
            ("ow", 5),
            ("dor", 4),
            ("rod", 4),
            ("do", 3),
            ("od", 3),
            ("or", 2),
        ]

        result_data = _get_anagrams("word")

        for scored_anagram in result_data:
            self.assertIn(scored_anagram, test_data)

        for scored_anagram in test_data:
            self.assertIn(scored_anagram, result_data)

    def test_sowpods_basic(self):
        """Simple sowpods use case."""

        test_data = [
            ("word", 8),
            ("drow", 8),
            ("dow", 7),
            ("row", 6),
            ("wo", 5),
            ("ow", 5),
            ("dor", 4),
            ("rod", 4),
            ("ord", 4),
            ("do", 3),
            ("od", 3),
            ("or", 2),
        ]

        result_data = _get_anagrams("word", sowpods=True)

        for scored_anagram in result_data:
            self.assertIn(scored_anagram, test_data)

        for scored_anagram in test_data:
            self.assertIn(scored_anagram, result_data)

    def test_start_end_chars_are_added(self):
        """Starting or ending chars should be used to find anagrams."""

        twl_expected = [("bod", 6)]
        twl_data = _get_anagrams("word", start="b", end="d")

        for scored_anagram in twl_expected:
            self.assertIn(scored_anagram, twl_data)

        for scored_anagram in twl_data:
            self.assertIn(scored_anagram, twl_expected)

        sowpods_expected = [("bod", 6), ("bord", 7), ("brod", 7)]
        sowpods_data = _get_anagrams("word", sowpods=True, start="b", end="d")

        for scored_anagram in sowpods_expected:
            self.assertIn(scored_anagram, sowpods_data)

        for scored_anagram in sowpods_data:
            self.assertIn(scored_anagram, sowpods_expected)


if __name__ == "__main__":
    unittest.main()
