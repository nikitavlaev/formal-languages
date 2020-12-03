from pathlib import Path
import os

from query_lang.parsing import ANTLRGrammar

class TestANTLR:
    tests_folder = 'test_data'

    def test_all(self):
        current_tests_path = Path(
            Path(__file__).parent,
            self.tests_folder,
        )

        for i, f in enumerate(os.listdir(current_tests_path)):
            print(f"Current test num: {i + 1}, {f}")
            print(open(Path(current_tests_path, f, 'res.txt')).readline())
            res = bool(int(open(Path(current_tests_path, f, 'res.txt')).readline())) 
            assert res == ANTLRGrammar(Path(current_tests_path, f, 'input.txt')).check()

