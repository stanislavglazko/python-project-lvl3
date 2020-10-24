import logging
import os
import tempfile
import pytest
from page_loader import loader


def test_name():
    link_for_test_name_page = 'https://stanislavglazko.github.io/github.io/'
    link_for_test_name_file = 'https://stanislavglazko.github.io/github.io/style.css'
    name_page_for_test = 'stanislavglazko-github-io-github-io.html'
    name_folder_for_test = 'stanislavglazko-github-io-github-io_files'
    name_file_for_test = 'stanislavglazko-github-io-github-io-style.css'
    name_page = loader.get_name(link_for_test_name_page)
    name_folder_for_files = loader.get_name(link_for_test_name_page, naming_folder=True)
    name_file = loader.get_name(link_for_test_name_file, naming_files=True)
    assert name_page == name_page_for_test
    assert name_folder_for_files == name_folder_for_test
    assert name_file == name_file_for_test
