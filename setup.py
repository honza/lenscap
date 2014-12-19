from setuptools import setup

long_desc = open('README.md').read()

setup(
    name='lenscap',
    version='0.2.0',
    url='',
    install_requires=[
        'misaka==1.0.2',
        'jinja2==2.7.3',
        'pillow==2.6.1',
        'pyyaml==3.11'
    ],
    description='static photo story generator',
    long_description=long_desc,
    author='Honza Pokorny',
    author_email='me@honza.ca',
    maintainer='Honza Pokorny',
    maintainer_email='me@honza.ca',
    packages=['lenscap'],
    include_package_data=True,
    scripts=['bin/lenscap']
)
