import os
import time 

from pathlib import Path

from src.algo import algo
from src.graph import Graph
from src.regexp import Regexp
from src import utils


DATA_FOLDER = "benchmark/refinedDataForRPQ"

SAMPLE_FOLDER = "LUBM1.9M"

RESULT_FILE = f"res_{SAMPLE_FOLDER}.csv"

EXP_NUM = 5

get_ms = lambda: int(round(time.time() * 1000))

with open(RESULT_FILE, 'w') as res_f:
    res_f.write("algo,graph,regex,reachable_pairs,intersection+closure_time_ms,pairs_time_ms\n")
    graph = Graph.from_txt(Path(DATA_FOLDER, SAMPLE_FOLDER, f"{SAMPLE_FOLDER}.txt"))

    regex_folder = Path(DATA_FOLDER, SAMPLE_FOLDER, "regexes")
    for number, regex_file in enumerate(os.listdir(regex_folder)):
        print(number, regex_file)
        regexp = Regexp.from_txt(Path(regex_folder, regex_file), py=False)

        for algo_num in (0, 1):
            intersection_and_closure_time_sum = 0
            pairs_time_sum = 0

            for _ in range(EXP_NUM):
                start_time = get_ms()
                intersection_bool_ms = graph.intersect(regexp)

                intersection_squashed = utils.squash_bool_ms(intersection_bool_ms)
                res = utils.transitive_closure(intersection_squashed, algo_num)
                intersection_and_closure_time_sum += get_ms() - start_time
                start_time = get_ms()
                labeled_edges = {}
                for label, bool_m in intersection_bool_ms.items():
                    labeled_edges[label] = bool_m.nvals
                pairs_time_sum += get_ms() - start_time
            
            res_f.write(f'{algo_num},{SAMPLE_FOLDER},{regex_file},{res.nvals},'
                        f'{intersection_and_closure_time_sum // EXP_NUM},{pairs_time_sum // EXP_NUM}\n')