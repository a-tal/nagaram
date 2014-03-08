"""Tests for argument parsing and string output formatting."""


import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
    from StringIO import StringIO
else:
    import unittest
    from io import StringIO

import nagaram
from nagaram.anagrams import anagrams_in_word
from nagaram.cmdline import pretty_print, argument_parser, main


class CmdLineTests(unittest.TestCase):
    """TestCases for command line entry and exit formatting."""

    def setUp(self):
        """Capture sys.stdout and stderr, reset sys.argv."""

        while len(sys.argv) > 1:
            sys.argv.pop(-1)

        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def tearDown(self):
        """Reset stdout and stderr."""

        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def test_pretty_print_twl(self):
        """Ensure we are formatting twl output correctly."""

        twl_output = [
            "Anagrams for word:",
            "8 points: word",
            "7 points: dow",
            "6 points: row",
            "5 points: ow, wo",
            "4 points: dor, rod",
            "3 points: do, od",
            "2 points: or",
        ]
        pretty_print("word", anagrams_in_word("word"))
        stdout = sys.stdout.getvalue().strip().splitlines()
        for line in twl_output:
            self.assertIn(line, stdout)

    def test_pretty_print_sowpods(self):
        """Ensure we are formatting sowpods output correctly."""

        sowpods_output = [
            "Anagrams for word:",
            "8 points: drow, word",
            "7 points: dow",
            "6 points: row",
            "5 points: ow, wo",
            "4 points: dor, ord, rod",
            "3 points: do, od",
            "2 points: or",
        ]
        pretty_print("word", anagrams_in_word("word", sowpods=True))
        stdout = sys.stdout.getvalue().strip().splitlines()
        for line in sowpods_output:
            self.assertIn(line, stdout)

    def test_print_twl_by_length(self):
        """Ensure we are formatting twl by length output correctly."""

        twl_output = [
            "Anagrams for word (score):",
            "4 tiles: word (8)",
            "3 tiles: dor (4), dow (7), rod (4), row (6)",
            "2 tiles: do (3), od (3), or (2), ow (5), wo (5)",
        ]
        pretty_print("word", anagrams_in_word("word"), by_length=True)
        stdout = sys.stdout.getvalue().strip().splitlines()
        for line in twl_output:
            self.assertIn(line, stdout)

    def test_print_sowpods_by_length(self):
        """Ensure we are formatting sowpods by length output correctly."""

        sowpods_output = [
            "Anagrams for word (score):",
            "4 tiles: drow (8), word (8)",
            "3 tiles: dor (4), dow (7), ord (4), rod (4), row (6)",
            "2 tiles: do (3), od (3), or (2), ow (5), wo (5)",
        ]
        pretty_print("word", anagrams_in_word("word", sowpods=True), True)
        stdout = sys.stdout.getvalue().strip().splitlines()
        for line in sowpods_output:
            self.assertIn(line, stdout)

    def test_print_invalid_word(self):
        """Ensure we inform the user their starting word was invalid."""

        word = "vin_diesel_in_xxx"
        pretty_print(word, anagrams_in_word(word))
        stdout = sys.stdout.getvalue().strip().splitlines()
        expected = "{} is not possible in Scrabble.".format(word)
        self.assertIn(expected, stdout)

    def test_arg_parsing_basic(self):
        """Test cmd line parsing a simple use case."""

        args = ["someword"]
        words, sowpods, by_length, starting, ending = argument_parser(args)
        self.assertEqual(args, words)
        self.assertFalse(sowpods)
        self.assertFalse(by_length)
        self.assertEqual(starting, "")
        self.assertEqual(ending, "")

    def test_arg_parsing_sowpods(self):
        """Test cmd line parsing a simple use case using sowpods."""

        args = ["--sowpods", "someword"]
        words, sowpods, by_length, starting, ending = argument_parser(args)
        self.assertEqual(["someword"], words)
        self.assertTrue(sowpods)
        self.assertFalse(by_length)
        self.assertEqual(starting, "")
        self.assertEqual(ending, "")

    def test_arg_parsing_by_length(self):
        """Test cmd line parsing a simple use case using by_length."""

        args = ["-l", "someword"]
        words, sowpods, by_length, starting, ending = argument_parser(args)
        self.assertEqual(["someword"], words)
        self.assertFalse(sowpods)
        self.assertTrue(by_length)
        self.assertEqual(starting, "")
        self.assertEqual(ending, "")

    def test_arg_parsing_starting(self):
        """Test cmd line parsing a simple use case using starting chars."""

        args = ["-s", "some", "word"]
        words, sowpods, by_length, starting, ending = argument_parser(args)
        self.assertEqual(["word"], words)
        self.assertFalse(sowpods)
        self.assertFalse(by_length)
        self.assertEqual(starting, "some")
        self.assertEqual(ending, "")

    def test_arg_parsing_ending(self):
        """Test cmd line parsing a simple use case using ending chars."""

        args = ["--ends-with", "some", "word"]
        words, sowpods, by_length, starting, ending = argument_parser(args)
        self.assertEqual(["word"], words)
        self.assertFalse(sowpods)
        self.assertFalse(by_length)
        self.assertEqual(starting, "")
        self.assertEqual(ending, "some")

    def test_arg_parsing_multiword(self):
        """Test cmd line parsing multiple words."""

        args = ["some", "word", "and", "others"]
        words, sowpods, by_length, starting, ending = argument_parser(args)
        self.assertEqual(args, words)
        self.assertFalse(sowpods)
        self.assertFalse(by_length)
        self.assertEqual(starting, "")
        self.assertEqual(ending, "")

    def test_version_output(self):
        """Make sure the version information is properly displayed."""

        expected_version = "Nagaram {} (Released: {})".format(
            nagaram.__version__,
            nagaram.__release_date__,
        )
        with self.assertRaises(SystemExit):
            argument_parser(["--version"])
        stderr = sys.stderr.getvalue().strip().splitlines()
        self.assertIn(expected_version, stderr)

        with self.assertRaises(SystemExit):
            argument_parser(["-v"])
        stderr = sys.stderr.getvalue().strip().splitlines()
        self.assertIn(expected_version, stderr)

    def test_help_is_docstring(self):
        """The help message should be the __doc__ from the __init__.py."""

        expected_help = nagaram.__doc__.strip().splitlines()
        with self.assertRaises(SystemExit) as error:
            argument_parser(["--help"])

        if sys.version_info < (3,):
            error_message = error.exception.message.strip().splitlines()
        else:
            error_message = error.exception.code.strip().splitlines()

        for line in expected_help:
            self.assertIn(line, error_message)

    def test_no_args_prints_use(self):
        """Should provide some help to the user when passed no args."""

        expected_help = [
            'usage: nagaram [-h] [--sowpods] [--length] [--starts-with chars]',
            '               [--ends-with chars] [--version]',
            '               ...',
        ]

        with self.assertRaises(SystemExit):
            argument_parser([])

        stdout = sys.stdout.getvalue().strip().splitlines()
        for line in expected_help:
            self.assertIn(line, stdout)

    def test_main_with_args(self):
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
        stdout = sys.stdout.getvalue().strip().splitlines()
        for line in expected_output:
            self.assertIn(line, stdout)

    def test_main_without_args(self):
        """Main should look up args from sys.argv if not passed any."""

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
        sys.argv.extend(["--sowpods", "word"])
        main()
        stdout = sys.stdout.getvalue().strip().splitlines()
        for line in expected_output:
            self.assertIn(line, stdout)


if __name__ == "__main__":
    unittest.main()
