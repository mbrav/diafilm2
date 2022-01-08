import glob
import json
import os
import re
from pathlib import Path

import requests
from apps.diafilms.models import Film, FilmCover, Frame, Image
from apps.posts.models import GroupCategory, Tag, TagCategory
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from tqdm import tqdm
from transliterate import translit

from .utils.util import async_looper

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

SITE_URL = 'https://diafilmy.su'


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


def getFilmTable():
    url = f'{SITE_URL}/base.php'
    r = requests.get(url)
    with open(html_table_path, 'w') as file:
        file.write(r.text)
    table = open(html_table_path, 'r')
    return table


def scrapeFilms(table):

    table_soup = BeautifulSoup(table.read(), 'html.parser')
    # thead = table_soup.find('thead')
    tbody = table_soup.find('tbody')
    trs = tbody.find_all('tr')

    @async_looper(concurrent=8, items=trs, desc='Downloading HTML files')
    def download_pages(tr):
        i = trs.index(tr)
        if not os.path.exists(f'{HTML_DIR}index-{i+1}.html'):
            r = requests.get(tr.find('a').get('href'))
            with open(f'{HTML_DIR}index-{i+1}.html', 'w') as file:
                file.write(r.text)
    # download_pages()

    # Read all pages in html folder and sort by number in file name
    pages = glob.glob(f'{HTML_DIR}*.html')

    def blob_sort(name):
        file = name.rsplit('/', 1)[-1]
        num = int(re.search(r'\d+', file).group())
        return num
    pages = sorted(pages, key=lambda x: blob_sort(x))

    def lookup_table_index(page_path: str) -> int:
        with open(page_path, 'r') as page:
            page_soup = BeautifulSoup(page.read(), 'html.parser')
            page_url = page_soup.find(property='og:url').get('content')
            table_el = table_soup.find(attrs={"href": page_url})
            table_id = table_el.parent.previous_sibling.get_text()
            return int(table_id)
    # test_name = 4005
    # print(f'{test_name}.html', ' -> ',
    #       lookup_table_index(pages[test_name-1])-1)

    new_data = []
    tr = tbody.find_all('tr')

    # Implemented async, but no improvement as expected
    # since async only helps in IO bounded processes, not CPU bounded ones
    @async_looper(concurrent=8, items=pages, desc='Parsing HTML files')
    def parse_pages(_page):
        p = pages.index(_page)
        table_id = lookup_table_index(_page) - 1

        # test
        # with open(_page, 'r') as page:
        #     test_soup = BeautifulSoup(page.read(), 'html.parser')
        #     desc = test_soup.find(property='og:description').get('content')
        #     title = test_soup.find(property='og:title').get('content')
        #     title_t = tr[table_id].find_all('td')[1].text.strip()
        #     print(
        #         f'file {p+1}.html\nindexes {p}, {table_id}\ntitle "{title}"\ntitle2: "{title_t}"\n')

        with open(pages[p], 'r') as page:
            meta = {
                'id': p + 1,
                'img': [],
                'img-cover': '',
                'description': '',
                'categories': []
            }

            for key in key_dict:
                if key == 1:
                    meta[key_dict[key]] = tr[table_id].find_all('td')[
                        key].text.strip()
                    meta['url'] = tr[table_id].find('a').get('href').strip()
                elif 8 < key < 15:
                    tags = tr[table_id].find_all('td')[key].text.split(',')
                    meta[key_dict[key]] = [x.strip() for x in tags]
                else:
                    meta[key_dict[key]] = tr[table_id].find_all('td')[
                        key].text.strip()

            soup = BeautifulSoup(page.read(), 'html.parser')
            txt_with_category = soup.find(class_='berrorstxt')
            img_cover = soup.find(property='og:image').get('content')
            desc = soup.find(property='og:description').get('content')
            slide = soup.find(class_='cycle-slideshow')

            # Set cover image
            meta['img-cover'] = img_cover.strip()
            # Set description
            meta['description'] = desc.strip()
            # Set categories
            for a in txt_with_category.find_all(
                    href=re.compile('diafilmy.su/diafilmy/')):
                meta['categories'].append(a.get_text().strip())
            # Get gallery images
            for img in slide.find_all('img'):
                meta['img'].append(SITE_URL + img.get('src'))
            new_data.append(meta)
    parse_pages()

    with open(film_json_path, 'w+') as f:
        json.dump(new_data, f)
    with open(film_json_path_min, 'w+') as f:
        json.dump(new_data[0:100], f)

    img_count = 0
    for i in range(len(new_data)):
        for j in range(len(new_data[i]['img'])):
            img_count += 1

    print('Number of image urls', img_count)


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
        self.DEBUG = False

    def add_arguments(self, parser):
        """Optional arguments"""
        parser.add_argument(
            '-i', '--import', action='store_true',
            help=f'Import files into db from {film_json_path}',)
        parser.add_argument('-s', '--scrape', action='store_true',
                            help=f'Scrape new films and save into {HTML_DIR} \
                            parse, and save JSON to {film_json_path}', )
        parser.add_argument(
            '-m', '--memory', action='store_true',
            help='Import tables into memory then dump to sqlitefile. 10x Faster.',)
        parser.add_argument('-d', '--debug', action='store_true',
                            help='Debuging option', )
        parser.add_argument('-t', '--test', action='store_true',
                            help='Do nothing, check if imports are working', )

    def handle(self, *args, **kwargs):
        """Handle the command"""

        imp = kwargs['import']
        scrape = kwargs['scrape']
        memory = kwargs['memory']
        debug = kwargs['debug']
        test = kwargs['test']

        if debug:
            self.DEBUG = True

        if scrape:
            table = getFilmTable()
            scrapeFilms(table)

        if imp:
            self.importFilmsFromJson('default')

        if memory:
            self.sqliteLoadToMemory()
            self.importFilmsFromJson(self.memory_db_name)
            self.sqliteDumpFromMemory()

        if test:
            pass

    def translitSlug(self, string):
        string = translit(string, 'ru', reversed=True).lower()
        string = '-'.join(string.split())
        return slugify(string)

    def importFilmsFromJson(self, db_name=file_db_name):
        """import files from database

        Args:
            db_name ([type], optional): [description]. Defaults to file_db_name.

        Optimization history with DEBUG = True:

            Importing 100 films timings:
                - Initial 49 sec, 2 it/s
                - Bulk import
        """

        # Get User
        User = get_user_model()
        user = User.objects.using(db_name).get(username='diafilm')

        # read and parse full JSON file
        new_json = open(film_json_path, mode='r')
        data = new_json.read()
        obj = json.loads(data)
        new_json.close()

        if self.DEBUG:
            obj = obj[:100]

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

        def genUnboundedObjects(_object):
            tag_cats = []
            for t_c, cat in cat_dict.items():
                c_slug = self.translitSlug(t_c)
                new_cat = TagCategory(
                    name=tag_cat(t_c),
                    slug=c_slug,
                    id=len(tag_cats) + 1)
                tag_cats.append(new_cat)
            TagCategory.objects.bulk_create(tag_cats)

            tags = []
            for _obj in _object:
                # Create dict for Foreign keys
                tag_categories = {
                    'author': _obj['author'],
                    'artist': _obj['artist'],
                    'designer': _obj['designer'],
                    'editor': _obj['editor'],
                    'artistic_editor': _obj['artistic_editor'],
                    'photographer': _obj['photographer'],
                }

                for c, cat in tag_categories.items():
                    for tag in list(filter(None, cat)):
                        tag_slug = self.translitSlug(tag)
                        category = None
                        for x in tag_cats:
                            if x.slug == c:
                                category = x

                        name = tag

                        # name_check = any(
                        #     t.name == category for t in tags)
                        slug_check = any(
                            t.slug == tag_slug for t in tags)

                        if slug_check is False:
                            new_tag = Tag(
                                id=len(tags) + 1,
                                name=name,
                                slug=tag_slug,
                                category=category,
                                category_id=category.id
                            )
                            tags.append(new_tag)
            Tag.objects.bulk_create(tags)

            groups = []
            for _obj in _object:
                for group in _obj['categories']:
                    slug = self.translitSlug(group)
                    # name_check = any(gr.name == group for gr in groups)
                    slug_check = any(gr.slug == slug for gr in groups)

                    if slug_check is False:
                        # print(name_check, slug_check, group, slug)
                        gr = GroupCategory(
                            id=len(groups) + 1,
                            name=group,
                            slug=self.translitSlug(group))
                        groups.append(gr)
            GroupCategory.objects.bulk_create(groups)

            films = []
            for _obj in _object:
                text_not_empty = _obj['description']
                if len(text_not_empty) == 0:
                    text_not_empty = _obj['name']
                f = Film(
                    author=user,
                    id=int('0' + _obj['id']),
                    name=_obj['name'],
                    url=_obj['url'],
                    studio=_obj['studio'],
                    year=int('0' + _obj['year']),
                    color=_obj['color'],
                    film_type=_obj['type'],
                    index=_obj['index'],
                    number=_obj['number'],
                    film_name=_obj['film'],
                    quality=_obj['quality'],
                    text=text_not_empty)

                for group in _obj['categories']:
                    name = group
                    slug = self.translitSlug(group)
                    group_object = None
                    for g in groups:
                        if g.slug == slug:
                            group_object = g

                    # print(group_object)
                    f.groups.add(group_object)

                films.append(f)

            return {
                'tag_categories': tag_categories,
                'tags': tags,
                'groups': groups,
                'films': films,
            }

        # models = genUnboundedObjects(obj)
        # print(f"Categories: {len(models['tag_categories'])}")
        # print(f"Tags: {len(models['tags'])}")
        # print(f"Groups: {len(models['groups'])}")
        # print(f"Films: {len(models['films'])}")
        # print(obj[4356])

        def slow():
            pbar = tqdm(obj, desc='Importing Films')
            for i in pbar:
                if not Film.objects.using(db_name).filter(id=i['id']).exists():
                    pbar.set_description(
                        f'#{i["id"]} {i["name"][:5]}..')
                    text_not_empty = i['description']
                    if len(text_not_empty) == 0:
                        text_not_empty = i['name']
                    f = Film.objects.using(db_name).create(
                        author=user,
                        id=int('0' + i['id']),
                        name=i['name'],
                        url=i['url'],
                        studio=i['studio'],
                        year=int('0' + i['year']),
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
                            name=group, slug=self.translitSlug(group))
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
                        c_slug = self.translitSlug(c)
                        select_tag_cat, tag_cat_created = TagCategory.objects.using(
                            db_name).get_or_create(name=tag_cat(c), slug=c_slug)

                        for tag in cat:
                            if tag != '':
                                tag_slug = self.translitSlug(tag)
                                select_tag, tag_created = Tag.objects.using(
                                    db_name).get_or_create(
                                    name=tag, slug=tag_slug,
                                    category=select_tag_cat)
                                f.tags.add(select_tag)
                        f.category = select_tag_cat

                    # Create frames
                    for key in range(len(i['img'])):
                        Frame.objects.using(db_name).create(
                            url=i['img'][key],
                            external=True,
                            film=f,
                            sequence=key)

                    # Check if image exists for cover image
                    img = None
                    try:
                        img = Image.objects.using(
                            db_name).filter(url=i['img-cover'])[0]
                    except:
                        img = Image(url=i['img-cover'])
                        img.save()
                        pbar.set_description(
                            'image not found:')

                    # Create cover image
                    FilmCover.objects.using(db_name).create(
                        film=f,
                        image=img
                    )
        slow()
