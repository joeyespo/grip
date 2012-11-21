from setuptools import setup, find_packages
import grip as package


def read(fname):
    import os
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name=package.__name__,
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/grip',
    license='MIT',
    version=package.__version__,
    description=package.__description__,
    long_description=package.__doc__,
    platforms='any',
    packages=find_packages(),
    package_data={package.__name__: ['LICENSE', 'static/*', 'templates/*']},
    entry_points={'console_scripts': ['grip = grip.command:main']},
    install_requires=read('requirements.txt'),
)
