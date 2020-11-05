import logging
import os
import tempfile
import pytest
from page_loader import loader


LINK_FOT_TEST, NAME_PAGE_FOR_TEST, NAME_FOLDER_FOR_TEST, NAME_FILE_FOR_TEST = (
    'https://stanislavglazko.github.io/github.io/',
    'stanislavglazko-github-io-github-io.html',
    'stanislavglazko-github-io-github-io_files',
    'stanislavglazko-github-io-github-io-style.css'
)


def test_load():
    with tempfile.TemporaryDirectory() as temp:
        result = loader.load(LINK_FOT_TEST, temp)
        name_page, name_folder, path_to_page, path_to_folder = result
        assert name_page == NAME_PAGE_FOR_TEST
        assert name_folder == NAME_FOLDER_FOR_TEST
        assert path_to_page == os.path.join(temp, NAME_PAGE_FOR_TEST)
        assert path_to_folder == os.path.join(temp, NAME_FOLDER_FOR_TEST)
        assert os.path.isfile(path_to_page)
        assert os.path.exists(path_to_folder)


def test_exception_no_schema():
    with pytest.raises(loader.KnownError) as e_info:
        loader.load('stanislavglazko.github.io/github.io/')
    assert 'Wrong address!' in str(e_info.value)


def test_exception_invalid_schema():
    with pytest.raises(loader.KnownError) as e_info:
        loader.load('ht://stanislavglazko.github.io/github.io/')
    assert 'Wrong address!' in str(e_info.value)


def test_exception_200():
    with pytest.raises(loader.KnownError) as e_info:
        loader.load('http://httpbin.org/status/404')
    assert 'Connection failed' in str(e_info.value)


def test_exception_umreal_folder():
    with pytest.raises(loader.KnownError) as e_info:
        loader.load('https://stanislavglazko.github.io/github.io/', 'unreal_path_to_file')
    assert 'Your folder is incorrect' in str(e_info.value)
