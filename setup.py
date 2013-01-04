"""\
Grip
----

Render local readme files before sending off to Github.


Grip is easy to set up
``````````````````````

::

    $ pip install grip
    $ cd myproject
    $ grip
     * Running on http://localhost:5000/


Links
`````

* `Website <http://github.com/joeyespo/grip>`_

"""

import os
import sys
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    sys.exit(os.system('python setup.py sdist upload'))


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='grip',
    version='1.1',
    description='Render local readme files before sending off to Github.',
    long_description=__doc__,
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/grip',
    license='MIT',
    platforms='any',
    packages=find_packages(),
    package_data={'': ['LICENSE'], 'grip': ['static/*', 'templates/*']},
    install_requires=read('requirements.txt'),
    zip_safe=False,
    entry_points={'console_scripts': ['grip = grip.command:main']},
)
