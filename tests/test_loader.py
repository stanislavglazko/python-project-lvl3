import logging
import os
import tempfile
import pytest
from page_loader import loader


def test_load():
    link_for_test = 'https://stanislavglazko.github.io/github.io/'
    name_page_for_test = 'stanislavglazko-github-io-github-io.html'
    name_folder_for_test = 'stanislavglazko-github-io-github-io_files'
    name_file_for_test = 'stanislavglazko-github-io-github-io-style.css'
    with tempfile.TemporaryDirectory() as temp:
        result = loader.load(link_for_test, temp)
        name_page, name_folder_for_files, path_to_page, path_to_folder_for_files, name_file = result
        assert name_page == name_page_for_test
        assert name_folder_for_files == name_folder_for_test
        assert name_file == os.path.join(temp, name_folder_for_test, name_file_for_test)
        assert path_to_page == os.path.join(temp, name_page_for_test)
        assert path_to_folder_for_files == os.path.join(temp, name_folder_for_test)
        assert os.path.isfile(path_to_page)
        assert os.path.isfile(name_file)
        assert os.path.exists(path_to_folder_for_files)


def test_exception():
    with pytest.raises(loader.KnownError) as e_info:
        loader.load('stanislavglazko.github.io/github.io/')
    assert 'Invalid URL. No schema supplied' in str(e_info.value)
    with pytest.raises(loader.KnownError) as e_info:
        loader.load('ht://stanislavglazko.github.io/github.io/')
    assert 'Invalid URL. Invalid scheme' in str(e_info.value)
    with pytest.raises(loader.KnownError) as e_info:
        loader.load('http://httpbin.org/status/404')
    assert 'status_code != 200' in str(e_info.value)
    with pytest.raises(loader.KnownError) as e_info:
        loader.load('https://stanislavglazko.github.io/github.io/', 'unreal_path_to_file')
    assert 'Your folder is incorrect' in str(e_info.value)
