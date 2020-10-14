from pathlib import Path
import os
import pytest
from itertools import starmap
from context_free_algos.cfpq.tensor import run_cfpq_from_file


class TestTensor:
    current_tests_path = Path(
        Path(__file__).parent.parent,
        'test_data',
    )

    @pytest.fixture(scope="function", params=[
        f
        for f in os.listdir(current_tests_path)
    ])
    def test_res(self, request):
        return request.param, set(starmap(
            lambda vs, ve: (int(vs), int(ve)),
            map(lambda s: s.split(),
                open(Path(self.current_tests_path, request.param, 'res_hellings.txt'),'r').readlines()),
        ))

    def test_all(self, test_res):
        f, res = test_res
        assert res == run_cfpq_from_file(
            Path(self.current_tests_path, f, 'test_g.txt'),
            Path(self.current_tests_path, f, 'test_gram.txt'),
        )
