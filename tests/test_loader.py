import pytest
import os
import tempfile
from page_loader import loader
import logging


check = {
    'https://exler.ru': ('exler-ru.html', 'exler-ru_files'),
    'https://brodude.ru': ('brodude-ru.html', 'brodude-ru_files'),
    'https://meduza.io': ('meduza-io.html', 'meduza-io_files'),
}


def test():
    for key, item in check.items():
        with tempfile.TemporaryDirectory() as temp:
            result = loader.save_page(key, temp, level_logging='debug')
            assert result[0] == os.path.join(temp, item[0])
            assert result[1] == os.path.join(temp, item[1])


def test_exception():
    with pytest.raises(loader.KnownError) as e_info:
        loader.save_page('brodude')
    assert 'URL error' in str(e_info.value)
    with pytest.raises(loader.KnownError) as e_info:
        loader.save_page('https://brodude.ru', level_logging='BBB')
    assert 'Level is not correct' in str(e_info.value)
    with pytest.raises(loader.KnownError) as e_info:
        loader.save_page('https://brodude.ru', 'ccc')
    print(str(e_info.value))
    assert 'No such directory' in str(e_info.value)
