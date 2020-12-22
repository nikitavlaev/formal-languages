import os
from pathlib import Path

from derivative_regex_parser.regex import Regex

class TestDRegexParser:
    tests_folder = 'test_data'

    def test_all(self):
        current_tests_path = Path(
            Path(__file__).parent,
            self.tests_folder,
        )

        for i, filename in enumerate(os.listdir(current_tests_path)):
            print(f"Current test num: {i + 1}, {filename}")
            with open(Path(current_tests_path, filename), 'r') as f:
                regex = Regex(f.readline().strip())
                word = f.readline().strip()
                ans = bool(int(f.readline().strip()))
                print(regex)
                print(word)
                print(ans)
                assert ans == regex.d_accepts(word)