# formal-languages
Repo for SPBU formal languages course practice assignments
## Launch tests manually  
```
conda install -c conda-forge --file=conda-requirements.txt
pip install -r pip-requirements.txt  
pytest
```
## Launch main script to execute graph query
```
usage: main.py [-h] [-g GRAPH_FILE] [-r REGEXP_FILE]
               [--start-vertices-file START_VERTICES_FILE]
               [--end-vertices-file END_VERTICES_FILE]

Script to execute simple query on graph using tensor product automata
intersection

optional arguments:
  -h, --help            show this help message and exit
  -g GRAPH_FILE, --graph-file GRAPH_FILE
                        File with graph as edge list. Format: (vertice, label,
                        vertice)
  -r REGEXP_FILE, --regexp-file REGEXP_FILE
                        File with regexp as a query. e.g. (0 2 (13? 6)*)+ (15
                        | 14)*)
  --start-vertices-file START_VERTICES_FILE
                        File with starting vertices set. e.g. 0 4 5 8
  --end-vertices-file END_VERTICES_FILE
                        File with vertices set. e.g. 0 4 5 8
```
## Transitive closure benchmark results
Full report can be found at benchmark/Report.pdf  
According to testing using LUBM datasets, squaring and multiplying by adjacency matrix shown almost no difference

[![Build Status](https://travis-ci.com/nikitavlaev/formal-languages.svg?branch=task01)](https://travis-ci.com/nikitavlaev/formal-languages)
