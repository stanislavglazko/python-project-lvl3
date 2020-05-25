import requests
import re
import os
from bs4 import BeautifulSoup


def load_page(link):
    page = requests.get(link)
    return page.text


def get_name(link, folder=None, extra=None):
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
    if folder:
        final_name = '{}_files'.format(result)
    elif extra:
        final_name = '{}{}'.format(result, f)
    else:
        final_name = '{}.html'.format(result)
    return final_name


def get_link(soup, new_folder, link):
    list_link = soup.find_all("link")
    for i in list_link:
        j = i['href']
        if len(j) >= 2:
            if j[0] == '/' and j[1] != '/':
                path_to_extra_file = os.path.join(new_folder,
                                                  get_name(j[1:], extra=1))
                with open(path_to_extra_file, 'w', encoding='utf-8') as f2:
                    f2.write(load_page(link + j))
                i['href'] = path_to_extra_file


def get_scripts_img(soup, new_folder, link):
    for i in soup.find_all(["script", "img"]):
        if 'src' in i.attrs:
            j = i['src']
            if j[0] == '/' and j[1] != '/':
                path_to_extra_file = os.path.join(new_folder,
                                                  get_name(j[1:], extra=1))
                with open(path_to_extra_file, 'w', encoding='utf-8') as f2:
                    f2.write(load_page(link + j))
                i['src'] = path_to_extra_file


def save_page(link, folder=''):
    if folder is None:
        path_to_file = get_name(link)
    else:
        path_to_file = os.path.join(folder, get_name(link))
    with open(path_to_file, 'w', encoding='utf-8') as f:
        f.write(load_page(link))
    with open(path_to_file, "r") as fx:
        contents = fx.read()
    soup = BeautifulSoup(contents, "lxml")
    if folder is None:
        new_folder = get_name(link, folder=1)
    else:
        new_folder = os.path.join(folder, get_name(link, folder=1))
    os.mkdir(new_folder)
    get_link(soup, new_folder, link)
    get_scripts_img(soup, new_folder, link)
    html = soup.prettify("utf-8")
    with open(path_to_file, "wb") as file:
        file.write(html)
    return path_to_file, new_folder
