import csv
import glob
import json
import os
import re
import sqlite3
from io import StringIO
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from apps.diafilms.models import Film, FilmCover, Frame, Image
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from apps.posts.models import GroupCategory, Tag, TagCategory
from transliterate import translit

from diafilm import settings

# Find the project base directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.abspath(__file__)
# Specify number of directories to go up from current file
PATH_UP = 1
BASE_DIR = str(Path(FILE_PATH).parents[PATH_UP])
DATA_DIR = BASE_DIR + '/data/'
HTML_DIR = BASE_DIR + '/html/'
film_json_path = DATA_DIR + 'post-metadata-all.json'
film_json_path_min = DATA_DIR + 'post-metadata-min.json'
html_table_path = DATA_DIR + 'diafilms-v2.html'

key_dict = {
    0: 'id',
    1: 'name',
    2: 'studio',
    3: 'year',
    4: 'color',
    5: 'type',
    6: 'frames',
    7: 'index',
    8: 'number',
    9: 'author',
    10: 'artist',
    11: 'designer',
    12: 'editor',
    13: 'artistic_editor',
    14: 'photographer',
    15: 'film',
    16: 'quality',
}


def translitSlug(string):
    string = translit(string, 'ru', reversed=True).lower()
    string = '-'.join(string.split())
    return slugify(string)


def getFilmTable():
    url = 'https://diafilmy.su/base.php'

    r = requests.get(url)
    with open(html_table_path, 'w') as file:
        file.write(r.text)

    table = open(html_table_path, 'r')

    # for i, th in enumerate(thead.find_all('th')):
    #     print(i, key_dict[i], th.get_text())

    return table


def scrapeFilms(table):

    soup = BeautifulSoup(table.read(), 'html.parser')
    thead = soup.find('thead')
    tbody = soup.find('tbody')

    for i, tr in enumerate(tbody.find_all('tr')):
        if os.path.exists(f'{HTML_DIR}index-{i+1}.html'):
            pass
        else:
            print(f'{HTML_DIR}index-{i+1}.html', i+1,
                  tr.find('a').text, 'does not exist')
            r = requests.get(tr.find('a').get('href'))
            with open(f'{HTML_DIR}index-{i+1}.html', 'w') as file:
                file.write(r.text)

    # Read all pages in html folder
    pages = glob.glob(f'{HTML_DIR}*.html')

    site_url = 'https://diafilmy.su'
    new_data = []

    tr = tbody.find_all('tr')
    for p in range(len(pages)):
        # for p in range(50):
        with open(pages[p], 'r') as page:

            dict = {
                'id': re.findall('\d+', page.name)[0],
                'img': [],
                'img-cover': '',
                'description': '',
                'categories': []
            }

            for i in key_dict:
                if i == 1:
                    dict[key_dict[i]] = tr[p].find_all('td')[i].text.strip()
                    dict['url'] = tr[p].find('a').get('href').strip()
                elif 8 < i < 15:
                    tags = tr[p].find_all('td')[i].text.split(',')
                    dict[key_dict[i]] = [x.strip() for x in tags]
                else:
                    dict[key_dict[i]] = tr[p].find_all('td')[i].text.strip()

            soup = BeautifulSoup(page.read(), 'html.parser')
            title = soup.find(id='news-title').get_text()
            img_cover = soup.find(property='og:image').get('content')
            desc = soup.find(property='og:description').get('content')
            slide = soup.find(class_='cycle-slideshow')
            txt_with_category = soup.find(class_='berrorstxt')

            # Set cover image
            dict['img-cover'] = img_cover.strip()

            # Set description
            dict['description'] = desc.strip()

            # Set categories
            for a in txt_with_category.find_all(href=re.compile('diafilmy.su/diafilmy/')):
                dict['categories'].append(a.get_text().strip())

            # Get gallery images
            for img in slide.find_all('img'):
                dict['img'].append(site_url + img.get('src'))

            new_data.append(dict)
            print(p, title, 'DONE')

    print(f'TEST, #673: {new_data[673]}')

    with open(film_json_path, 'w+') as f:
        json.dump(new_data, f)

    with open(film_json_path_min, 'w+') as f:
        json.dump(new_data[0:100], f)

    img_count = 0
    for i in range(len(new_data)):
        for j in range(len(new_data[i]['img'])):
            img_count += 1

    print('Number of images scraped', img_count)


def copy_database(source_connection, dest_dbname=':memory:'):
    script = ''.join(source_connection.iterdump())
    dest_conn = sqlite3.connect(dest_dbname)
    dest_conn.executescript(script)
    return dest_conn


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    # Selecting DB
    # https://docs.djangoproject.com/en/3.2/topics/db/multi-db/#manually-selecting-a-database-for-a-queryset

    # Dumping sqlite into mememory and back
    # https://stackoverflow.com/a/10856450
    # https://stackoverflow.com/a/33920763
    # https://stackoverflow.com/a/3826587
    # https://coderoad.ru/8045602/

    # file_db = sqlite3.connect(settings.DATABASES[file_db_name]['NAME'])
    # memory_db = sqlite3.connect(settings.DATABASES[memory_db_name]['NAME'])

    file_db_name = 'default'
    memory_db_name = 'memory'

    def __init__(self):
        file_db = settings.DATABASES[self.file_db_name]['NAME']
        memory_db = settings.DATABASES[self.memory_db_name]['NAME']
        self.file_con = sqlite3.connect(file_db)
        self.memory_con = sqlite3.connect(memory_db)

        # Read database to tempfile
        # con = sqlite3.connect(app.config['SQLITE_DATABASE'])
        tempfile = StringIO()
        for line in self.file_con.iterdump():
            tempfile.write('%s\n' % line)
        self.file_con.close()
        tempfile.seek(0)

        # Create a database in memory and import from tempfile
        # app.sqlite = sqlite3.connect(":memory:")
        self.memory_con.cursor().executescript(tempfile.read())
        self.memory_con.commit()
        self.memory_con.row_factory = sqlite3.Row

    def add_arguments(self, parser):
        """Optional arguments"""
        parser.add_argument('-i', '--import', action='store_true',
                            help=f'Import files into db from {film_json_path}', )
        parser.add_argument('-s', '--scrape', action='store_true',
                            help=f'Scrape new films and save into {HTML_DIR} \
                            parse, and save JSON to {film_json_path}', )
        parser.add_argument('-m', '--memory', action='store_true',
                            help=f'Import tables into memory then dump to sqlitefile. 10x Faster.', )

    def handle(self, *args, **kwargs):
        """Handle the command"""

        imp = kwargs['import']
        scrape = kwargs['scrape']
        memory = kwargs['memory']

        if scrape:
            table = getFilmTable()
            scrapeFilms(table)

        if imp:
            self.importFilmsFromJson('default')

        if memory:
            self.sqliteLoadToMemory()
            self.importFilmsFromJson(self.memory_db_name)
            self.sqliteDumpFromMemory()

    def sqliteLoadToMemory(self):
        pass

    def sqliteDumpFromMemory(self):
        pass

    def importFilmsFromJson(self, db_name=file_db_name):

        # Get User
        User = get_user_model()
        user = User.objects.using(db_name).get(username='diafilm')

        # read and parse full JSON file
        new_json = open(film_json_path, mode='r')
        data = new_json.read()
        obj = json.loads(data)
        print('JSON Read, #112:', obj[112]['name'])

        # Film.objects.using(db_name).all().delete()
        # Image.objects.using(db_name).all().delete()
        # Frame.objects.using(db_name).all().delete()
        # FilmCover.objects.using(db_name).all().delete()
        # GroupCategory.objects.using(db_name).all().delete()

        cat_dict = {
            'author': 'Автор',
            'editor': 'Редактор',
            'designer': 'Художественный редактор',
            'artist': 'Художник',
            'artistic_editor': 'Художник-оформитель',
            'photographer': 'Фотограф'
        }

        def tag_cat(string):
            if string in cat_dict:
                return cat_dict[string]
            return string

        for i in obj:
            if not Film.objects.using(db_name).filter(id=i['id']).exists():
                print(f'Adding #{i["id"]} - {i["name"]}')
                text_not_empty = i['description']
                if len(text_not_empty) == 0:
                    text_not_empty = i['name']
                f = Film.objects.using(db_name).create(
                    author=user,
                    id=int('0'+i['id']),
                    name=i['name'],
                    url=i['url'],
                    studio=i['studio'],
                    year=int('0'+i['year']),
                    color=i['color'],
                    film_type=i['type'],
                    index=i['index'],
                    number=i['number'],
                    film_name=i['film'],
                    quality=i['quality'],
                    text=text_not_empty,
                )

                for group in i['categories']:
                    gr, gr_create = GroupCategory.objects.using(db_name).get_or_create(
                        name=group,
                        slug=translitSlug(group))
                    if gr_create:
                        print(f'INFO: Created new GroupCategory "{group}"')

                    f.groups.add(gr)

                # Create dict for Foreign keys
                tag_categories = {
                    'author': i['author'],
                    'artist': i['artist'],
                    'designer': i['designer'],
                    'editor': i['editor'],
                    'artistic_editor': i['artistic_editor'],
                    'photographer': i['photographer'],
                }

                for c, cat in tag_categories.items():
                    c_slug = translitSlug(c)
                    select_tag_cat, tag_cat_created = TagCategory.objects.using(db_name).get_or_create(
                        name=tag_cat(c),
                        slug=c_slug)
                    if tag_cat_created:
                        print(f'INFO: Created new TagCategory "{tag_cat(c)}"')

                    for tag in cat:
                        if tag != '':
                            tag_slug = translitSlug(tag)
                            select_tag, tag_created = Tag.objects.using(db_name).get_or_create(
                                name=tag,
                                slug=tag_slug,
                                category=select_tag_cat)
                            if tag_created:
                                print(
                                    f'INFO: Created new tag {tag_slug} for category {tag_cat(c)}')
                            f.tags.add(select_tag)
                    f.category = select_tag_cat

                # Create frames
                for key in range(len(i['img'])):
                    fr = Frame.objects.using(db_name).create(
                        url=i['img'][key],
                        external=True,
                        film=f,
                        sequence=key,
                    )

                # Check if image exists for cover image
                img = None
                try:
                    img = Image.objects.using(
                        db_name).filter(url=i['img-cover'])[0]
                except:
                    img = Image(url=i['img-cover'])
                    img.save()
                    print('image not found:', i['img-cover'])

                # Create cover image
                film_cover = FilmCover.objects.using(db_name).create(
                    film=f,
                    image=img
                )
