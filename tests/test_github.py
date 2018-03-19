"""
Tests GitHub's public API to verify that all assumptions made by Grip
are still in place.

Note that these tests assume a reliable internet connection, so they
may fail despite being correct. To run the tests without making any
external calls, use `py.test -m "not assumption"`
"""

from __future__ import print_function, unicode_literals

import os

import pytest
import requests
from grip import DEFAULT_API_URL, GitHubAssetManager, GitHubRenderer

from helpers import USER_CONTEXT, input_file, output_file


@pytest.fixture
def input_markdown():
    return input_file('gfm-test.md')


@pytest.fixture
def output_readme():
    return output_file('raw', 'gfm-test.html')


@pytest.fixture
def output_user_content():
    return output_file('raw', 'gfm-test-user-content.html')


@pytest.fixture
def output_user_context():
    return output_file('raw', 'gfm-test-user-context.html')


@pytest.mark.assumption
def test_github():
    requests.get(DEFAULT_API_URL).raise_for_status()


@pytest.mark.assumption
def test_github_api():
    assert GitHubRenderer(raw=True).render('') == ''
    assert GitHubRenderer(user_content=True, raw=True).render('') == ''


@pytest.mark.assumption
def test_github_readme(input_markdown, output_readme):
    assert GitHubRenderer(raw=True).render(input_markdown) == output_readme


@pytest.mark.assumption
def test_github_user_content(input_markdown, output_user_content):
    renderer = GitHubRenderer(True, raw=True)
    assert renderer.render(input_markdown) == output_user_content


@pytest.mark.assumption
def test_github_user_context(input_markdown, output_user_context):
    renderer = GitHubRenderer(True, USER_CONTEXT, raw=True)
    assert renderer.render(input_markdown) == output_user_context


@pytest.mark.assumption
def test_styles_exist(tmpdir):
    GitHubAssetManager(str(tmpdir)).retrieve_styles('http://dummy/')
    assert len(tmpdir.listdir()) > 2

    files = list(map(lambda f: os.path.basename(str(f)), tmpdir.listdir()))
    assert any(f.startswith('github-') and f.endswith('.css') for f in files)
    assert any(
        f.startswith('frameworks-') and f.endswith('.css') for f in files)

    # TODO: Test that style retrieval actually parsed CSS with regex


# TODO: Test that local images show up in the browser
# TODO: Test that web images show up in the browser
# TODO: Test that octicons show up in the browser
# TODO: Test that anchor tags still work
