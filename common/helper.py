import argparse


def get_argparser():
    parser = argparse.ArgumentParser(description='NVCCPlugin params')
    parser.add_argument("-t", "--timeit", action='store_true',
                        help='flag to return timeit result instead of stdout')
    parser.add_argument("--custom", nargs='*')
    parser.add_argument("--compile_custom", nargs='+')
    return parser


def print_out(out: str):
    for l in out.split('\n'):
        print(l)
