"""Test anagram finding functions."""


import pytest

from nagaram.anagrams import anagrams_in_word


def _get_anagrams(word, sowpods=False, start="", end=""):
    """Run the anagrams_in_word generator until its done, return as a list."""

    return [result for result in anagrams_in_word(word, sowpods, start, end)]


@pytest.mark.parametrize(
    "word,sowpods,start,end, expected",
    (
        ("word", False, "", "", [
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
        ]),
        ("word", True, "", "", [
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
        ]),
        ("word", False, "b", "d", [("bod", 6)]),
        ("word", True, "b", "d", [("bod", 6), ("bord", 7), ("brod", 7)]),
    ),
    ids=("twl_basic", "sowpods_basic", "twl_both", "sowpods_both")
)
def test_anagrams_in_word(word, sowpods, start, end, expected):
    """Ensure we're looking up and scoring anagrams correctly."""

    received = _get_anagrams(word, sowpods=sowpods, start=start, end=end)

    for scored_anagram in received:
        assert scored_anagram in expected

    for scored_anagram in expected:
        assert scored_anagram in received
