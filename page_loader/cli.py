import argparse

DEBUG, INFO, WARNING, ERROR, CRITICAL = \
    'debug', 'info', 'error', 'warning', 'critical'

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
    default=INFO,
    choices=[DEBUG, INFO, WARNING, ERROR, CRITICAL],
    help='level of logging'
)
