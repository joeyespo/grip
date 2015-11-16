from __future__ import print_function, unicode_literals

import io
import os


DIRNAME = os.path.dirname(os.path.abspath(__file__))
USER_CONTEXT = 'joeyespo/grip'


def input_filename(*parts):
    return os.path.join(DIRNAME, 'input', *parts)


def output_filename(*parts):
    return os.path.join(DIRNAME, 'output', *parts)


def input_file(*parts, **kwargs):
    encoding = kwargs.pop('encoding', 'utf-8')
    with io.open(input_filename(*parts), 'rt', encoding=encoding) as f:
        return f.read()


def output_file(*parts, **kwargs):
    encoding = kwargs.pop('encoding', 'utf-8')
    with io.open(output_filename(*parts), 'rt', encoding=encoding) as f:
        return f.read()
