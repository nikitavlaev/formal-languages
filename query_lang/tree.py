from argparse import ArgumentParser
from query_lang.parsing import ANTLRGrammar

if __name__ == "__main__":
    parser = ArgumentParser(
        description="""Generate DOT file with parse tree of given script"""
    )
    parser.add_argument(
        'script',
        help='Path to script written in DB language'
    )
    parser.add_argument(
        'dot_file',
        help='Path to save generated DOT file'
    )

    args = parser.parse_args()
    ANTLRGrammar(args.script).generate_dot_tree(args.dot_file)