import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('link', type=str)
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='folder for saving link'
    )
    args = parser.parse_args()
    return args
