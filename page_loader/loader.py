import requests
import re
import os


def load_page(link):
    page = requests.get(link)
    return page.text


def get_name_file(link):
    name = re.split('//', link)
    if len(name) != 1:
        name = name[1]
    result = ''
    for letter in name:
        letter_new = re.sub(r'\W', '-', letter)
        result += letter_new
    final_name = '{}.html'.format(result)
    return final_name


def save_page(link, folder=''):
    if folder is None:
        path_to_file = get_name_file(link)
    else:
        path_to_file = os.path.join(folder, get_name_file(link))
    with open(path_to_file, 'w', encoding='utf-8') as f:
        f.write(load_page(link))
