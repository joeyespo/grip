import os
from setuptools import setup, find_packages
import grip as package


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name=package.__name__,
    version=package.__version__,
    description=package.__description__,
    long_description=package.__doc__,
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/grip',
    license='MIT',
    platforms='any',
    packages=find_packages(),
    package_data={package.__name__: ['LICENSE', 'static/*', 'templates/*']},
    include_package_data=True,
    install_requires=read('requirements.txt'),
    zip_safe=False,
    entry_points={'console_scripts': ['grip = grip.command:main']},
)
