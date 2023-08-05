from fuc.api.common import get_script_name
from fuc.api.BedFrame import BedFrame

def create_parser(subparsers):
    parser = subparsers.add_parser(
        get_script_name(__file__),
        help='[BED] find intersection of two or more BED files',
        description='This command will compute intersections beween '
            'multiple BED files. It essentially wraps the '
            '`pyranges.PyRanges.intersect` method.'
    )
    parser.add_argument('bed_files', help='BED files', nargs='+')

def main(args):
    bfs = [BedFrame.from_file(x) for x in args.bed_files]
    final_bf = bfs[0]
    for bf in bfs[1:]:
        final_bf = final_bf.intersect(bf)
    print(final_bf.to_string())
