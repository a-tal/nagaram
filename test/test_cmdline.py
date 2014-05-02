"""Tests for argument parsing and string output formatting."""


import sys
import pytest

import nagaram
from nagaram.anagrams import anagrams_in_word
from nagaram.cmdline import pretty_print, argument_parser, main


@pytest.mark.parametrize(
    "sowpods,expected_output",
    (
        (False, [
            "Anagrams for word:",
            "8 points: word",
            "7 points: dow",
            "6 points: row",
            "5 points: ow, wo",
            "4 points: dor, rod",
            "3 points: do, od",
            "2 points: or",
        ]),
        (True, [
        "Anagrams for word:",
        "8 points: drow, word",
        "7 points: dow",
        "6 points: row",
        "5 points: ow, wo",
        "4 points: dor, ord, rod",
        "3 points: do, od",
        "2 points: or",
        ]),
    ),
    ids=("twl", "sowpods")
)
def test_pretty_print_word(sowpods, expected_output, capfd):
    """Ensure we are formatting the literal word 'word' correctly."""

    pretty_print("word", anagrams_in_word("word", sowpods=sowpods))

    stdout, _ = capfd.readouterr()
    for line in expected_output:
        assert line in stdout


@pytest.mark.parametrize(
    "sowpods,expected_output",
    (
        (False, [
            "Anagrams for word (score):",
            "4 tiles: word (8)",
            "3 tiles: dor (4), dow (7), rod (4), row (6)",
            "2 tiles: do (3), od (3), or (2), ow (5), wo (5)",
        ]),
        (True, [
            "Anagrams for word (score):",
            "4 tiles: drow (8), word (8)",
            "3 tiles: dor (4), dow (7), ord (4), rod (4), row (6)",
            "2 tiles: do (3), od (3), or (2), ow (5), wo (5)",
        ]),
    ),
    ids=("twl", "sowpods")
)
def test_print_word_by_length(sowpods, expected_output, capfd):
    """Ensure we are formatting words by length output correctly."""

    pretty_print("word", anagrams_in_word("word", sowpods=sowpods),
                 by_length=True)
    stdout, _ = capfd.readouterr()
    for line in expected_output:
        assert line in stdout


def test_print_invalid_word(capfd):
    """Ensure we inform the user their starting word was invalid."""

    word = "vin_diesel_in_xxx"
    pretty_print(word, anagrams_in_word(word))
    stdout, _ = capfd.readouterr()
    assert "{0} is not possible in Scrabble.".format(word) in stdout


@pytest.mark.parametrize(
    "args,expected_output",
    (
        (["word"], (["word"], False, False, "", "")),
        (["--sowpods", "word"], (["word"], True, False, "", "")),
        (["-l", "word"], (["word"], False, True, "", "")),
        (["-s", "ok", "word"], (["word"], False, False, "ok", "")),
        (["--ends-with", "ok", "word"], (["word"], False, False, "", "ok")),
        (["some", "word", "and", "others"], (["some", "word", "and", "others"],
            False, False, "", "")),
    ),
    ids=("basic", "sowpods", "by_length", "start", "end", "multiword"),
)
def test_arg_parsing(args, expected_output):
    """Test cmd line parsing."""

    for received, expected in zip(argument_parser(args), expected_output):
        assert received == expected


@pytest.mark.parametrize("arg", ("-v", "--version"), ids=("short", "long"))
def test_version_output(arg, capfd):
    """Make sure the version information is properly displayed."""

    expected_version = "Nagaram {0} (Released: {1})".format(
        nagaram.__version__,
        nagaram.__release_date__,
    )
    with pytest.raises(SystemExit):
        argument_parser([arg])
    stdout, stderr = capfd.readouterr()
    assert expected_version in stdout + stderr


def test_help_is_docstring():
    """The help message should be the __doc__ from the __init__.py."""

    with pytest.raises(SystemExit) as error:
        argument_parser(["--help"])

    for line in nagaram.__doc__.strip().splitlines():
        for arg in error.value.args:
            if line in arg:
                break
        else:
            assert 0, "{0} not found in {1}".format(line, error.value.args)


def test_no_args_prints_use(capfd):
    """Should provide some help to the user when passed no args."""

    expected_help = [
        'usage: nagaram [-h] [--sowpods] [--length] [--starts-with chars]',
        '               [--ends-with chars] [--version]',
        '               ...',
    ]

    with pytest.raises(SystemExit):
        argument_parser([])

    stdout, _ = capfd.readouterr()
    for line in expected_help:
        assert line in stdout


def test_main_with_args(capfd):
    """Confirm everything works together."""

    expected_output = [
        "Anagrams for word:",
        "8 points: word",
        "7 points: dow",
        "6 points: row",
        "5 points: ow, wo",
        "4 points: dor, rod",
        "3 points: do, od",
        "2 points: or",
    ]

    main(["word"])
    stdout, _ = capfd.readouterr()
    for line in expected_output:
        assert line in stdout


def test_main_without_args(capfd):
    """Main should look up args from sys.argv if not passed any."""

    sys.argv = ["nagaram", "--sowpods", "word"]

    expected_output = [
        "Anagrams for word:",
        "8 points: drow, word",
        "7 points: dow",
        "6 points: row",
        "5 points: ow, wo",
        "4 points: dor, ord, rod",
        "3 points: do, od",
        "2 points: or",
    ]
    main()
    stdout, _ = capfd.readouterr()
    for line in expected_output:
        assert line in stdout
