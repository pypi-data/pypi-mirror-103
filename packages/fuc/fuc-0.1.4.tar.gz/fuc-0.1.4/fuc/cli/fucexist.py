from pathlib import Path
import sys
from fuc.api.common import get_script_name

def create_parser(subparsers):
    parser = subparsers.add_parser(
        get_script_name(__file__),
        help='[FUC] check whether files/dirs exist',
        description='This command will check whether files/dirs exist. '
                    'It will look for stdin if there are no arguments (e.g. '
                    f"$ cat files.list | fuc {get_script_name(__file__)})."
    )
    parser.add_argument('paths', nargs='*',
        help='file/dir paths (default: stdin)')

def main(args):
    if args.paths:
        paths = args.paths
    elif not sys.stdin.isatty():
        paths = sys.stdin.read().rstrip('\n').split('\n')
    else:
        raise ValueError('no input files detected')
    for path in paths:
        print(Path(path).exists(), path)
