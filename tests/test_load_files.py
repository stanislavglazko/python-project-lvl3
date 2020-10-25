import logging
import os
import tempfile
import magic
import pytest
import requests
from page_loader import loader


def test_load_files():
    link_for_test = 'https://stanislavglazko.github.io/github.io/style.css'
    with tempfile.TemporaryDirectory() as temp:
        path = os.path.join(temp, loader.get_name(link_for_test, naming_files=True))
        loader.load_files([(link_for_test, path)])
        assert os.path.isfile(path)
