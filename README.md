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

## CYK and CFPQ  
Added CYK algo implementation and Hellings-based CFPQ in context_free_algos
Added matmul-based and tensor product-based CFPQ algos

[![Build Status](https://travis-ci.com/nikitavlaev/formal-languages.svg?branch=task01)](https://travis-ci.com/nikitavlaev/formal-languages)

## Graph Query Language
### Grammar
-- Main script is a list of statements  
<b>SCRIPT STMT SCRIPT
SCRIPT EPS</b>  

-- Connect to the graph database  
<b>STMT connect " STRING "</b>  
-- Add new production to the grammar  
<b>STMT STRING : PATTERN</b>  
-- Execute query with constraints  
<b>STMT select QOBJECT from GRAPH</b>  

-- Graph can be represented as:  
-- Intersection of 2 other graphs  
<b>GRAPH GRAPH intersect RGR</b>  
-- Regex as DFA  
<b>RGR [ PATTERN ]</b>  
-- Collected grammar as RSM  
<b>RGR grammar</b>  
-- Loaded from the file with provided name from the connected database  
<b>RGR " STRING "</b>  

-- Start and final vertices can be fixed in the graph  
<b>RGR setStartAndFinal VERTICES VERTICES GRAPH</b>  

-- Vertices can be provided as set, range or none  
<b>VERTICES { SET }</b>  
<b>VERTICES INT : INT</b>  
<b>VERTICES _</b>  

-- Query objective is the subject that one might want to select from the graph  
-- All edges, total amount of the edges, or subset of the edges, specified by filter is supported  
<b>QOBJECT EDGES</b>  
<b>QOBJECT count EDGES</b>  
-- Filtering edges:  
<b>EDGES filter COND : EDGES</b>  
<b>COND ( STRING , STRING , STRING ) -> ( BOOL_EXPR )</b>  
-- Boolean expression supports |, &, ! operations    
-- Also predicates like hasLbl, isStart, isFinal are available  

#### Examples 

 - Connect to db:    
   - `connect "/home/user/nikita/db"`
 - Add grammar `S -> a S b S | eps`:
   - `s : nonterm(S).term(a).nonterm(S).term(b)`
   - `s : term(eps)`
 - Select all edges from graph, represented by regex <b>a?b*(c|d)+</b>
   - `select edges from [term(a)?.term(b)*.(term(c)|term(d))+]`
 - Select all edges from graph "g", that has label abc and connect starting and finishing sets of vertices of graph
   - `select filter (v, e, u) -> (e hasLbl abc & isStart v | !(isFinal u)) : edges from "g"`
 - Count all edges in intersection of provided graphs:
   - `select count edges from "g1" intersect ("g2" intersect "g3")`

#### ANTLR grammar 
Added query language grammar for ANTLR. Added tree DOT-file generation.

##### Prerequisites:
```
sudo apt-get update
sudo apt-get install antlr4
pip install antlr4-python3-runtime
```
Generate necessary ANTLR files(root dir):
```
cd query_lang && antlr4 -Dlanguage=Python3 -o antlr_grammar antlr_grammar.g4 && cd ../
```
Generate DOT file:

```
usage: tree.py [-h] script dot_file
Generate DOT file with parse tree of given script
positional arguments:
  script      Path to script written in DB language
  dot_file    Path to save generated DOT file
optional arguments:
  -h, --help  show this help message and exit
```

Example: `python tree.py ./tests/test_data/test1/input.txt ./tree.dot`