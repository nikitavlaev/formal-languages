from pyformlang.cfg import Variable

from context_free_algos.cyk import CYK
from context_free_algos.cfg import custom_CFG

GRAMMAR_PATH = 'query_lang/grammar.txt'
KEYWORDS_PATH = 'query_lang/keywords.txt'
PUNCTUATION = ['"', '.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '_', '->', '&', '!', '|']

def preprocess_script(raw_script):
    raw_script = raw_script.strip()
    for p in PUNCTUATION:
        raw_script = raw_script.replace(p, f" {p} ")
    with open(KEYWORDS_PATH, 'r') as f:
        keywords = f.read().splitlines()

    script = []
    for l in raw_script.split():
        script.append(l) if (l in keywords or l in PUNCTUATION) else script.extend(l)
    return script

def run_script(raw_script, gram=None):
    if gram is None:
        with open(GRAMMAR_PATH, 'r') as f:
            gram = custom_CFG.read_cfg(
                f.read(),
                start_symbol=Variable("SCRIPT"),
                contains_regexes=True,
                track_variables=True,
            )
        gram = gram.to_normal_form()
    script = preprocess_script(raw_script)
    return CYK(gram, script)

if __name__ == '__main__':
    raw_script = """
        select count edges from ("graph" intersect [term(a).term(b)*.(term(c)|term(d))+])
    """
    print(run_script(raw_script))