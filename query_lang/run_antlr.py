from query_lang.parsing import ANTLRGrammar
from pathlib import Path

print(ANTLRGrammar(Path('/home/nikita/prog/formal-languages/query_lang/tests/test_data/test5/input.txt')).check())