import os
import tempfile
import pytest
from page_loader import loader


def test_load_files():
    link_for_test = 'https://stanislavglazko.github.io/github.io/style.css'
    with tempfile.TemporaryDirectory() as temp:
        path = os.path.join(temp, loader.get_name(link_for_test, naming_files=True))
        loader.load_files([(link_for_test, path)])
        assert os.path.isfile(path)
        with pytest.raises(loader.KnownError) as e_info:
            loader.load_files([('http://httpbin.org/status/404', path)])
        assert 'status_code != 200' in str(e_info.value)
