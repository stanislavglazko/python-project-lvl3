from page_loader.cli import parse_args
from page_loader.loader import save_page


def main():
    args = parse_args()
    save_page(args.link, args.output)


if __name__ == '__main__':
    main()
