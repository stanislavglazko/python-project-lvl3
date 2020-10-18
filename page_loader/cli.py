import argparse

parser = argparse.ArgumentParser(description='Page loader')
parser.add_argument('link', type=str)
parser.add_argument(
    '-o', '--output',
    type=str,
    default='',
    help='folder for saving link'
)
parser.add_argument(
    '-l', '--level',
    type=str,
    default='info',
    choices=['debug', 'info', 'warning', 'error', 'critical'],
    help='level of logging'
)
args = parser.parse_args()
