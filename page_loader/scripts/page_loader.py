import logging
import sys
from page_loader import cli
from page_loader import loader


def main():
    args = cli.parser.parse_args()
    loader.set_level(args.level)
    try:
        loader.load(args.link, args.output)
    except loader.KnownError as e:
        logging.error(e.message)
        logging.debug(e.trace)
        sys.exit(1)


if __name__ == '__main__':
    main()
