import logging
import os
import re
import traceback
import magic
import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar


class KnownError(Exception):
    def __init__(self, message, trace):
        self.message = message
        self.trace = trace


def level(level_logging):
    dict_of_level = {'debug': logging.DEBUG,
                     'warning': logging.WARNING,
                     'error': logging.ERROR,
                     'critical': logging.CRITICAL,
                     'info': logging.INFO,
                     }
    return logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                               filename='my.log',
                               filemode='w',
                               level=dict_of_level[level_logging])


def load_page(link):
    logging.info('Loading page')
    try:
        page = requests.get(link)
        page.raise_for_status()
    except requests.exceptions.MissingSchema as e:
        trace = traceback.format_exc()
        raise KnownError('Invalid URL. No schema supplied', trace) from e
    except requests.exceptions.InvalidSchema as e:
        trace = traceback.format_exc()
        raise KnownError('Invalid URL. Invalid scheme', trace) from e
    except requests.exceptions.HTTPError as e:
        trace = traceback.format_exc()
        raise KnownError('status_code != 200', trace) from e
    except requests.exceptions.ConnectionError as e:
        trace = traceback.format_exc()
        raise KnownError('Connection error', trace) from e
    return page.text


def get_name(link, naming_folder=False, naming_files=False):
    if link[-1] == '/':
        link = link[:-1]
    name = re.split('//', link)
    if len(name) != 1:
        name = name[1]
    else:
        name = name[0]
    if naming_files:
        name, extension = os.path.splitext(name)
    final_name = ''
    for letter in name:
        letter_new = re.sub(r'\W', '-', letter)
        final_name += letter_new
        if len(final_name) >= 50:
            break
    if naming_files:
        final_name += extension
    elif naming_folder:
        final_name += '_files'
    else:
        final_name += '.html'
    return final_name


def change_page(page, url, path_to_folder_for_files):
    logging.info('Changing page')
    soup = BeautifulSoup(page, "lxml")
    list_img_scr_link = soup.find_all(["script", "img", "link"])
    result = []
    atr = ''
    link = ''
    for i in list_img_scr_link:
        if 'href' in i.attrs:
            atr = 'href'
            link = i['href']
        elif 'src' in i.attrs:
            atr = 'src'
            link = i['src']
        if atr != '':
            if not re.findall(r'http|www|\.com|\.ru|'
                              r'\.org|\.io|\.рф|\.su|'
                              r'\.net|\.info', link):
                if link[0] == '/':
                    path = os.path.join(url, link[1:])
                else:
                    path = os.path.join(url, link)
                path_to_extra_file = \
                    os.path.join(
                        path_to_folder_for_files,
                        get_name(path, naming_files=True))
                i[atr] = path_to_extra_file
                result.append((path, path_to_extra_file))
    changed_page = soup.prettify("utf-8")
    return changed_page, result


def save_changed_page(changed_page, path_to_page):
    logging.info('Saving page')
    try:
        with open(path_to_page, "wb") as page:
            page.write(changed_page)
    except IOError as e:
        info_for_debug = traceback.format_exc()
        raise KnownError('No such directory', info_for_debug) from e


def load_extra_files(source):
    logging.info('Loading links, images, scripts')
    bar = IncrementalBar('Loading scripts amd images', max=len(source))
    for link, path_to_extra_file in source:
        r = requests.get(link)
        mime_types = {'text/html', 'text/css', 'text/javascript'}
        mime_type = magic.from_buffer(r.content, mime=True)
        if mime_type in mime_types:
            with open(path_to_extra_file, 'w') as f:
                f.write(r.text)
        else:
            with open(path_to_extra_file, 'wb') as f:
                f.write(r.content)
        bar.next()
    bar.finish()


def load(link, folder=''):
    page = load_page(link)
    name_page = get_name(link)
    path_to_page = os.path.join(folder, name_page)
    name_folder_for_files = get_name(link, naming_folder=True)
    path_to_folder_for_files = os.path.join(folder, name_folder_for_files)
    try:
        os.mkdir(path_to_folder_for_files)
    except IOError:
        logging.warning('Do not save one page twice in one folder')
    changed_page, source_of_extra_files = \
        change_page(page, link, path_to_folder_for_files)
    save_changed_page(changed_page, path_to_page)
    load_extra_files(source_of_extra_files)
    logging.info('The page is saved')
    return name_page, name_folder_for_files, path_to_page, \
        path_to_folder_for_files, source_of_extra_files[0][1]
