import requests
import re
import os
from bs4 import BeautifulSoup
import logging
from progress.bar import IncrementalBar


class KnownError(Exception):
    pass


list_of_logging = ['debug', 'DEBUG', 'INFO', 'info', 'warning', 'WARNING',
                   'ERROR', 'error', 'critical', 'CRITICAL', None, '']


def load_page(link):
    logging.info('Loading page')
    try:
        page = requests.get(link)
        assert page.status_code == 200
    except requests.exceptions.MissingSchema as e:
        logging.error('Invalid URL. No schema supplied', exc_info=True)
        raise KnownError('URL error') from e
    except requests.exceptions.ConnectionError as e:
        logging.error('Connection error', exc_info=True)
        raise KnownError('Connection error') from e
    except AssertionError as e:
        logging.error('Assertion error', exc_info=True)
        raise KnownError('Assertion error') from e
    return page.text


def get_name(link, folder=None, extra=None):
    logging.info('Getting name')
    name = re.split('//', link)
    if len(name) != 1:
        name = name[1]
    else:
        name = name[0]
    result = ''
    if extra:
        name, f = os.path.splitext(name)
    for letter in name:
        letter_new = re.sub(r'\W', '-', letter)
        result += letter_new
        if len(result) >= 40:
            break
    if folder:
        final_name = '{}_files'.format(result)
    elif extra:
        final_name = '{}{}'.format(result, f)
    else:
        final_name = '{}.html'.format(result)
    logging.debug(final_name)
    return final_name


def get_link(soup, new_folder, link):
    logging.info('Getting links')
    list_link = soup.find_all("link")
    bar = IncrementalBar('Loading links', max=len(list_link))
    for i in list_link:
        j = i['href']
        if len(j) >= 2:
            if j[0] == '/' and j[1] != '/':
                path_to_extra_file = os.path.join(new_folder,
                                                  get_name(j[1:], extra=1))
                with open(path_to_extra_file, 'w', encoding='utf-8') as f2:
                    f2.write(load_page(link + j))
                i['href'] = path_to_extra_file
        bar.next()
    bar.finish()


def get_scripts_img(soup, new_folder, link):
    logging.info('Getting scripts and img')
    list_img_scr = soup.find_all(["script", "img"])
    bar = IncrementalBar('Loading scripts amd images', max=len(list_img_scr))
    for i in list_img_scr:
        if 'src' in i.attrs:
            j = i['src']
            if j[0] == '/' and j[1] != '/':
                path_to_extra_file = os.path.join(new_folder,
                                                  get_name(j[1:], extra=1))
                with open(path_to_extra_file, 'w', encoding='utf-8') as f2:
                    f2.write(load_page(link + j))
                i['src'] = path_to_extra_file
        bar.next()
    bar.finish()


def save_page(link, folder='', level_logging=''):
    try:
        assert level_logging in list_of_logging
    except Exception as e:
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                            filename='my.log',
                            filemode='w',
                            level=logging.ERROR)
        logging.error('Your level of logging is not correct', exc_info=True)
        raise KnownError('Level is not correct') from e
    if level_logging == 'debug' or level_logging == 'DEBUG':
        level_logging = logging.DEBUG
    elif level_logging == 'warning' or level_logging == 'WARNING':
        level_logging = logging.WARNING
    elif level_logging == 'error' or level_logging == 'ERROR':
        level_logging = logging.ERROR
    elif level_logging == 'critical' or level_logging == 'CRITICAL':
        level_logging = logging.CRITICAL
    else:
        level_logging = logging.INFO
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename='my.log',
                        filemode='w',
                        level=level_logging)
    logging.debug(level_logging)
    if folder is None:
        path_to_file = get_name(link)
    else:
        path_to_file = os.path.join(folder, get_name(link))
    logging.debug(path_to_file)
    try:
        with open(path_to_file, 'w', encoding='utf-8') as f:
            f.write(load_page(link))
    except IOError as e:
        logging.error('No such directory', exc_info=True)
        raise KnownError('No such directory') from e
    with open(path_to_file, "r") as fx:
        contents = fx.read()
    soup = BeautifulSoup(contents, "lxml")
    if folder is None:
        new_folder = get_name(link, folder=1)
    else:
        new_folder = os.path.join(folder, get_name(link, folder=1))
    try:
        os.mkdir(new_folder)
    except IOError:
        logging.warning('Do not save one page twice in one folder')
    get_link(soup, new_folder, link)
    get_scripts_img(soup, new_folder, link)
    html = soup.prettify("utf-8")
    with open(path_to_file, "wb") as file:
        file.write(html)
    logging.info('The page is saved')
    return path_to_file, new_folder
