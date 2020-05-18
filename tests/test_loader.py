from page_loader import loader
import pytest
import os
import tempfile


check = {
    'https://exler.ru': 'exler-ru.html',
    'https://brodude.ru': 'brodude-ru.html',
    'https://meduza.io': 'meduza-io.html',
    'https://hexlet.io/courses': 'hexlet-io-courses.html',
}


def test():
    for key, item in check.items():
        with tempfile.TemporaryDirectory() as temp:
            result = loader.save_page(key, temp)
            assert result == item
