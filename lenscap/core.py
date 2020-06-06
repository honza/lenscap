import os
import misaka
import yaml
import hashlib
from shutil import copyfile
from jinja2 import Environment, FileSystemLoader
from PIL import Image


columns = {
    1: 40,
    2: 100,
    3: 160,
    4: 220,
    5: 280,
    6: 340,
    7: 400,
    8: 460,
    9: 520,
    10: 580,
    11: 640,
    12: 700,
    13: 760,
    14: 820,
    15: 880,
    16: 940,
    'third': 300
}

columns_classes = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    'third': 'one-third'
}


def hash_file(filename):
    return hashlib.sha1(open(filename).read()).hexdigest()


class RowLayout(object):

    def __init__(self, data, options, env):
        self.data = data
        self.options = options
        self.env = env
        self.rows = str(data.get('rows', '1'))
        self.rows = list(map(int, self.rows.split(',')))
        self.items = data['items']

        if sum(self.rows) != len(self.items):
            raise Exception('wrong number of photos in layout')

        self.assert_photos_exist()
        self.parsed_rows = self.collect_photo_info()
        self.assert_photos_big_enough()

    def assert_photos_exist(self):
        for photo in self.items:
            full_path = os.path.join(self.options.photos_dir, photo)
            if not os.path.exists(full_path):
                raise Exception(photo)

    def assert_photos_big_enough(self):
        for row in self.parsed_rows:
            for photo in row:
                full_path = os.path.join(self.options.photos_dir,
                                         photo['filename'])
                col_width = columns[photo['columns']]
                im = Image.open(full_path)
                w, h = im.size

                if w < col_width:
                    raise Exception('Photo {} not wide enough. '
                                    'Need {}px, got only {}px'.format(
                                        photo['filename'], col_width, w))

                if self.options.resize:
                    hash = hash_file(full_path)[:10]
                    base, ext = os.path.splitext(photo['filename'])
                    out = ''.join([base, '_', hash, ext])
                    full_out = os.path.join(self.options.photos_dir, out)
                    new_size = None

                    new_width = col_width
                    ratio = float(w) / float(h)
                    new_height = int(round(new_width / ratio))

                    new_size = (new_width, new_height)

                    im.thumbnail(new_size)
                    im.save(full_out, im.format)

                    photo['filename'] = out

    def render_template(self, template, values):
        t = self.env.get_template(template)
        return t.render(values)

    def collect_photo_info(self):
        rows = []
        photo_filenames = self.items

        for row in self.rows:
            new_row = []

            for photo in range(0, row):

                if row == 3:
                    r = 'third'
                else:
                    r = 16 / row

                classes = []

                if photo == 0:
                    classes.append('alpha')

                if photo == (row - 1):
                    classes.append('omega')

                classes.append(columns_classes[r])

                if r in ['one', 'third']:
                    classes.append('column')
                else:
                    classes.append('columns')

                new_row.append({
                    'classes': ' '.join(classes),
                    'columns': r,
                    'filename': photo_filenames[0]
                })

                photo_filenames = photo_filenames[1:]

            rows.append(new_row)

        return rows

    def render(self):
        context = {
            'rows': self.parsed_rows,
            'options': self.options
        }

        return self.render_template('rows.html', context)


class LenscapRenderer(misaka.HtmlRenderer):

    def set_options(self, options, env):
        self.options = options
        self.env = env

    def block_code(self, text, lang):
        data = None

        if lang == 'yaml':
            data = yaml.safe_load(text)

        if not data:
            return ''

        r = RowLayout(data, self.options, self.env)
        return r.render()


class Lenscap(object):

    def __init__(self, options):
        self.options = options

        if not options.theme:
            self.theme = 'default'
        else:
            self.theme = options.theme

        templates_path = options.templates_dir or os.path.join(
            os.path.dirname(__file__), 'templates', self.theme)

        self.stylesheet_path = options.stylesheet_path or os.path.join(
            os.path.dirname(__file__), 'templates/style.css')
        self.skeleton_path = os.path.join(os.path.dirname(__file__),
                                          'templates/skeleton.css')

        self.env = Environment(loader=FileSystemLoader(templates_path))

        r = LenscapRenderer()
        r.set_options(self.options, self.env)
        self.markdown = misaka.Markdown(r, extensions=misaka.EXT_FENCED_CODE)

    def render_template(self, template, values):
        t = self.env.get_template(template)
        return t.render(values)

    def add_stylesheet(self, filename):
        directory = os.path.dirname(os.path.abspath(filename))
        stylesheet = os.path.join(directory, 'style.css')
        skeleton = os.path.join(directory, 'skeleton.css')

        if not os.path.exists(stylesheet):
            copyfile(self.stylesheet_path, stylesheet)
            copyfile(self.skeleton_path, skeleton)

    def process_file(self, filename):
        with open(filename) as f:
            data = f.read()

        if self.options.output_file:
            filename = self.options.output_file
        else:
            base = os.path.splitext(filename)[0]
            filename = '{}.html'.format(base)

        html = self.markdown.render(data)

        with open(filename, 'w') as f:
            f.write(self.render_template('base.html', {
                'content': html,
                'options': self.options
            }))

        self.add_stylesheet(filename)


def main(filenames, options):
    lens = Lenscap(options)

    for f in filenames:
        lens.process_file(f)
