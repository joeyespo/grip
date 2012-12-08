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

__version__ = '1.0'
__description__ = '\n\n'.join(__doc__.split('\n\n')[1:]).split('\n\n\n')[0]


import os
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='grip',
    version=__version__,
    description=__description__,
    long_description=__doc__,
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/grip',
    license='MIT',
    platforms='any',
    packages=find_packages(),
    package_data={'': ['LICENSE'], 'grip': ['static/*', 'templates/*']},
    include_package_data=True,
    install_requires=read('requirements.txt'),
    zip_safe=False,
    entry_points={'console_scripts': ['grip = grip.command:main']},
)
