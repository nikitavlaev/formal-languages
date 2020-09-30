from pathlib import Path
import os
from context_free_algos.cyk import run_cyk_from_file


class TestCYK:
    tests_folder = 'test_data'

    def test_all(self):
        current_tests_path = Path(
            Path(__file__).parent,
            self.tests_folder,
        )

        for f in os.listdir(current_tests_path):
            res = list(map(lambda x: bool(int(x)), open(Path(current_tests_path, f, 'res_cyk.txt')).readlines()))
            assert res == run_cyk_from_file(
                Path(current_tests_path, f, 'test_gram.txt'),
                Path(current_tests_path, f, 'test_w.txt'),
            )
