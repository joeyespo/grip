"""
Regenerates all the rendered Markdown files in the output/ directory.
"""

from __future__ import print_function, unicode_literals

import sys
import io
import os

DIRNAME = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.dirname(DIRNAME))

from grip import Grip, GitHubRenderer, TextReader
from helpers import USER_CONTEXT, input_file, input_filename
from mocks import GripMock


# Use auth from user settings
AUTH = Grip(TextReader('')).auth


def write(text, *parts):
    filename = os.path.join(DIRNAME, 'output', *parts)
    return io.open(filename, 'wt', encoding='utf-8').write(text)


def regenerate_app():
    zero = input_filename('zero.md')
    simple = input_filename('simple.md')
    gfm_test = input_filename('gfm-test.md')

    write(GripMock(zero, AUTH).render(), 'app', 'zero.html')
    write(GripMock(zero, AUTH, GitHubRenderer(True)).render(),
          'app', 'zero-user-context.html')
    write(GripMock(zero, AUTH, GitHubRenderer(True, USER_CONTEXT)).render(),
          'app', 'zero-user-context.html')

    write(GripMock(simple, AUTH).render(), 'app', 'simple.html')
    write(GripMock(simple, AUTH, GitHubRenderer(True)).render(),
          'app', 'simple-user-context.html')
    write(GripMock(simple, AUTH, GitHubRenderer(True, USER_CONTEXT)).render(),
          'app', 'simple-user-context.html')

    write(GripMock(gfm_test, AUTH).render(), 'app', 'gfm-test.html')
    write(GripMock(gfm_test, AUTH, GitHubRenderer(True)).render(),
          'app', 'gfm-test-user-context.html')
    write(GripMock(gfm_test, AUTH, GitHubRenderer(True, USER_CONTEXT))
          .render(), 'app', 'gfm-test-user-context.html')


def regenerate_exporter():
    # TODO: Implement
    # TODO: Strip out inlined CSS specifics?
    pass


def regenerate_renderer():
    simple = input_file('simple.md')
    gfm_test = input_file('gfm-test.md')

    write(GitHubRenderer().render(simple, AUTH),
          'renderer', 'simple.html')
    write(GitHubRenderer(True).render(simple, AUTH),
          'renderer', 'simple-user-content.html')
    write(GitHubRenderer(True, USER_CONTEXT).render(simple, AUTH),
          'renderer', 'simple-user-context.html')

    write(GitHubRenderer().render(gfm_test, AUTH),
          'renderer', 'gfm-test.html')
    write(GitHubRenderer(True).render(gfm_test, AUTH),
          'renderer', 'gfm-test-user-content.html')
    write(GitHubRenderer(True, USER_CONTEXT).render(gfm_test, AUTH),
          'renderer', 'gfm-test-user-context.html')


def regenerate_raw():
    zero = input_file('zero.md')
    simple = input_file('simple.md')
    gfm_test = input_file('gfm-test.md')

    write(GitHubRenderer(raw=True).render(zero, AUTH),
          'raw', 'zero.html')
    write(GitHubRenderer(True, raw=True).render(zero, AUTH),
          'raw', 'zero-user-content.html')
    write(GitHubRenderer(True, USER_CONTEXT, raw=True).render(zero, AUTH),
          'raw', 'zero-user-context.html')

    write(GitHubRenderer(raw=True).render(simple, AUTH),
          'raw', 'simple.html')
    write(GitHubRenderer(True, raw=True).render(simple, AUTH),
          'raw', 'simple-user-content.html')
    write(GitHubRenderer(True, USER_CONTEXT, raw=True).render(simple, AUTH),
          'raw', 'simple-user-context.html')

    write(GitHubRenderer(raw=True).render(gfm_test, AUTH),
          'raw', 'gfm-test.html')
    write(GitHubRenderer(True, raw=True).render(gfm_test, AUTH),
          'raw', 'gfm-test-user-content.html')
    write(GitHubRenderer(True, USER_CONTEXT, raw=True)
          .render(gfm_test, AUTH), 'raw', 'gfm-test-user-context.html')


def regenerate():
    print('Regenerating output files...')
    regenerate_app()
    regenerate_exporter()
    regenerate_renderer()
    regenerate_raw()


if __name__ == '__main__':
    regenerate()
