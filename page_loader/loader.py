import logging
import os
import re
import magic
import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from urllib.parse import urlparse
from page_loader.cli import DEBUG, INFO, WARNING, ERROR, CRITICAL


class KnownError(Exception):
    pass


def set_level(level_logging):
    dict_of_level = {DEBUG: logging.DEBUG,
                     WARNING: logging.WARNING,
                     ERROR: logging.ERROR,
                     CRITICAL: logging.CRITICAL,
                     INFO: logging.INFO,
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
    except (requests.exceptions.MissingSchema,
            requests.exceptions.InvalidSchema) as e:
        raise KnownError('Wrong address!') from e
    except requests.exceptions.HTTPError as e:
        raise KnownError('Connection failed') from e
    except requests.exceptions.ConnectionError as e:
        raise KnownError('Connection error') from e
    return page.text


def get_name(link, naming_folder=False, naming_files=False):
    link = link.rstrip('/')
    o = urlparse(link)
    name = o.netloc + o.path
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


def update_links(page, url, path_to_folder_for_files):
    logging.info('Changing page')
    soup = BeautifulSoup(page, "lxml")
    links = soup.find_all(["script", "img", "link"])
    forbidden_prefixes = ['http', 'www']
    result = []
    attr = ''
    link = ''
    for tag in links:
        if 'href' in tag.attrs:
            attr = 'href'
            link = tag['href']
        elif 'src' in tag.attrs:
            attr = 'src'
            link = tag['src']
        if attr != '':
            if all(not link.startswith(prefix)
                   for prefix in forbidden_prefixes):
                link = link.lstrip('/')
                path = os.path.join(url, link)
                path_to_extra_file = \
                    os.path.join(
                        path_to_folder_for_files,
                        get_name(path, naming_files=True))
                tag[attr] = path_to_extra_file
                result.append((path, path_to_extra_file))
    changed_page = soup.prettify("utf-8")
    return changed_page, result


def save_changed_page(changed_page, path_to_page):
    logging.info('Saving page')
    try:
        with open(path_to_page, "wb") as page:
            page.write(changed_page)
    except IOError as e:
        raise KnownError('Your folder is incorrect') from e


def load_files(source):
    logging.info('Loading links')
    bar = IncrementalBar('Loading links', max=len(source))
    for link, path_to_extra_file in source:
        try:
            r = requests.get(link)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise KnownError('Connection failed') from e
        except requests.exceptions.ConnectionError as e:
            raise KnownError('Connection error') from e
        text_types = {'text/html', 'text/css', 'text/javascript'}
        mime_type = magic.from_buffer(r.content, mime=True)
        mode, data = ('w', r.text) if mime_type in text_types \
            else ('wb', r.content)
        with open(path_to_extra_file, mode) as f:
            f.write(data)
        bar.next()
    bar.finish()


def load(link, folder=''):
    bar = IncrementalBar('Loading page', max=5, suffix='%(percent)d%%')
    page = load_page(link)
    bar.next()
    name_of_page = get_name(link)
    path_to_page = os.path.join(folder, name_of_page)
    name_of_folder = get_name(link, naming_folder=True)
    path_to_folder = os.path.join(folder, name_of_folder)
    if not os.path.exists(path_to_folder):
        try:
            os.mkdir(path_to_folder)
        except IOError as e:
            raise KnownError('Your folder is incorrect') from e
    bar.next()
    changed_page, source_of_files = \
        update_links(page, link, path_to_folder)
    bar.next()
    save_changed_page(changed_page, path_to_page)
    bar.next()
    load_files(source_of_files)
    bar.next()
    bar.finish()
    logging.info('The page is saved')
    return name_of_page, name_of_folder, path_to_page, path_to_folder
