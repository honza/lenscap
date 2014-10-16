import os
import misaka
import yaml
from jinja2 import Environment, FileSystemLoader


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


class NotEnoughPhotosException(Exception):
    pass


class ConfigurationException(Exception):
    pass


class MissingPhotoException(Exception):
    pass


class RowLayout(object):

    def __init__(self, data, options, env):
        self.data = data
        self.options = options
        self.env = env
        self.rows = data.get('rows', '1')
        self.rows = map(int, self.rows.split(','))
        self.items = data['items']

        if sum(self.rows) != len(self.items):
            raise ConfigurationException('wrong number of photos in layout')

        self.assert_photos_exist()

    def assert_photos_exist(self):
        for photo in self.items:
            full_path = os.path.join(self.options.photos_dir, photo)
            if not os.path.exists(full_path):
                raise MissingPhotoException(photo)

    def render_template(self, template, values):
        t = self.env.get_template(template)
        return t.render(values)

    def render(self):
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

                if row == 1:
                    pass
                else:
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
                    'filename': photo_filenames[0]
                })

                photo_filenames = photo_filenames[1:]

            rows.append(new_row)

        context = {
            'rows': rows,
            'options': self.options
        }

        return self.render_template('rows.html', context)


class LayoutRenderer(object):

    def __init__(self, data, options, env):
        self.data = data
        self.options = options
        self.env = env

        self.layout = RowLayout(data, options, env)

    def render(self):
        return self.layout.render()


class TripodRenderer(misaka.HtmlRenderer):

    def set_options(self, options, env):
        self.options = options
        self.env = env

    def block_code(self, text, lang):
        data = None

        if lang == 'yaml':
            data = yaml.safe_load(text)

        if not data:
            return ''

        r = LayoutRenderer(data, self.options, self.env)
        return r.render()


def main(filename, options):
    with open(filename) as f:
        data = f.read()

    base = os.path.splitext(filename)[0]

    templates_path = options.templates_dir or '../templates'
    env = Environment(loader=FileSystemLoader(templates_path))

    r = TripodRenderer()
    r.set_options(options, env)
    m = misaka.Markdown(r, extensions=misaka.EXT_FENCED_CODE)
    html = m.render(data)

    with open('{}.html'.format(base), 'w') as f:
        t = env.get_template('base.html')
        f.write(t.render({
            'content': html,
            'options': options
        }))
