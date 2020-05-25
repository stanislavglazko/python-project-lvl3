import pytest
import os
import tempfile
from page_loader import loader


check = {
    'https://exler.ru': ('exler-ru.html', 'exler-ru_files'),
    'https://brodude.ru': ('brodude-ru.html', 'brodude-ru_files'),
    'https://meduza.io': ('meduza-io.html', 'meduza-io_files'),
    'https://hexlet.io/courses': ('hexlet-io-courses.html', 'hexlet-io-courses_files'),
}


def test():
    for key, item in check.items():
        with tempfile.TemporaryDirectory() as temp:
            result = loader.save_page(key, temp)
            assert result[0] == os.path.join(temp, item[0])
            assert result[1] == os.path.join(temp, item[1])
