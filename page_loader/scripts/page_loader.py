import logging
import sys
from page_loader.cli import args
from page_loader.loader import load, level, KnownError


def main():
    level_logging = args.level
    if level_logging:
        level(level_logging)
    try:
        load(args.link, args.output)
    except KnownError as e:
        logging.error(e.message)
        logging.debug(e.trace)
        sys.exit(1)


if __name__ == '__main__':
    main()
