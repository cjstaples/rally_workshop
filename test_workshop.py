import pytest
import argparse
import sys
import unittest
import workshop


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here

    def test_help_output_is_generated(capsys):
        sys.argv = ['workshop.py', '-h']
        with pytest.raises(SystemExit):
            workshop.main()
        capture = capsys.readouterr()
        assert 'usage:' in capture.out
        # assert 'Query and Update Rally project data' in out
        # assert '-h, --help            show this help message and exit' in out


if __name__ == '__main__':
    unittest.main()
