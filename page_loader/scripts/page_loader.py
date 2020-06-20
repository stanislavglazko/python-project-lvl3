from page_loader.cli import parse_args
from page_loader.loader import save_page, KnownError
import sys


def main():
    args = parse_args()
    try:
        save_page(args.link, args.output, level_logging=args.level)
    except KnownError:
        sys.exit(1)


if __name__ == '__main__':
    main()
