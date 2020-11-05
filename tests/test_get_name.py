from page_loader import loader


def test_get_name_for_page():
    assert loader.get_name(
        'https://stanislavglazko.github.io/github.io/'
    ) == 'stanislavglazko-github-io-github-io.html'


def test_get_name_for_folder():
    assert loader.get_name(
        'https://stanislavglazko.github.io/github.io/',
        naming_folder=True
    ) == 'stanislavglazko-github-io-github-io_files'


def test_get_name_for_file():
    assert loader.get_name(
        'https://stanislavglazko.github.io/github.io/style.css',
        naming_files=True
    ) == 'stanislavglazko-github-io-github-io-style.css'
