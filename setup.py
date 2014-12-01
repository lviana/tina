#!/usr/bin/python

import os
from setuptools import setup

templates = []
for file in os.listdir('src/templates'):
    templates.append('src/templates/%s' % file)

setup(
    name='tina',
    version='0.0.1',
    description='Resource manager and platform orchestrator',
    long_description='Resource manager and virtualization platform orchestrator',
    author='Luiz Viana',
    author_email='lviana@include.io',
    maintainer='Luiz Viana',
    maintainer_email='lviana@include.io',
    url='https://github.com/lviana/tina',
    packages=['tina'],
    package_dir={'tina': 'src/lib'},
    license='Apache',
    data_files=[('/usr/bin', ['src/bin/tinad']),
                ('/usr/bin', ['src/bin/tina']),
                ('/usr/share/tina', templates),
                ('/etc/tina', ['src/config/tina.conf'])]
)
