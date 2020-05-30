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
    parser.add_argument(
        '-l', '--level',
        type=str,
        default=None,
        help='level of logging'
    )
    args = parser.parse_args()
    return args
