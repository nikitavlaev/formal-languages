import pytest
import random
from src.graph import Graph
from src.regexp import Regexp


@pytest.fixture(scope="function", params=[
    (vertices_num, regex)
    for regex in ['a*b*c*', '(a|b)+(c|d)*', 'a?b*c+d']
    for vertices_num in [5, 10, 25, 50, 100]
])
def random_data(request):
    vertices_num, regex_str = request.param
    edges_num = vertices_num * (vertices_num - 1) // 5
    v_from = [random.randint(0, vertices_num) for _ in range(edges_num)]
    v_to = [random.randint(0, vertices_num) for _ in range(edges_num)]
    values = [random.choice(['a', 'b', 'c', 'd']) for _ in range(edges_num)]
    edges_list = zip(v_from, values, v_to)
    graph = Graph(edges_list, vertices_num + 1)
    regex = Regexp.from_str(regex_str)
    return graph, regex


def test_intersection_random(random_data):
    graph, regex = random_data
    intersection_bool_ms = graph.intersection_bool_ms(regex)

    for (value, matrix) in intersection_bool_ms.items():
        matrix_lists = matrix.to_lists()
        for i in range(len(matrix_lists[0])):
            v_from = matrix_lists[0][i]
            v_to = matrix_lists[1][i]

            graph_from, graph_to = v_from // regex.size, v_to // regex.size
            regex_from, regex_to = v_from % regex.size, v_to % regex.size

            assert matrix[v_from, v_to] == 1
            assert graph.bool_ms[value][graph_from, graph_to] == 1
            assert regex.bool_ms[value][regex_from, regex_to] == 1
