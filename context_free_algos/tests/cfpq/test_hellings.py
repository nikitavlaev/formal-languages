from pathlib import Path
import os
from context_free_algos.cfpq.hellings import run_hellings_from_file
from itertools import starmap


class TestHellings:
    tests_folder = 'test_data'

    def test_all(self):
        current_tests_path = Path(
            Path(__file__).parent.parent,
            self.tests_folder,
        )

        for f in os.listdir(current_tests_path):
            res = set(starmap(
                lambda vs, ve: (int(vs), int(ve)),
                map(lambda s: s.split(),
                    open(Path(current_tests_path, f, 'res_hellings.txt'),'r').readlines()),
            ))
            assert res == run_hellings_from_file(
                Path(current_tests_path, f, 'test_g.txt'),
                Path(current_tests_path, f, 'test_gram.txt'),
            )
