"""
Tests Grip's public API, i.e. everything you can access from `import grip`.

This doesn't send any requests to GitHub (see test_github.py for that), and
this doesn't run a server (see test_cli.py for that). Instead, this creates
fake objects with subclasses and tests the basic expected behavior of Grip.
"""

from __future__ import print_function, unicode_literals

import os
import posixpath

import pytest
from requests.exceptions import HTTPError
from werkzeug.exceptions import NotFound

from helpers import USER_CONTEXT, input_file, input_filename, output_file
from mocks import (
    GitHubAssetManagerMock, GripMock, GitHubRequestsMock, StdinReaderMock)

from grip import (
    DEFAULT_API_URL, DEFAULT_FILENAMES, DEFAULT_FILENAME, DEFAULT_GRIPHOME,
    DEFAULT_GRIPURL, STYLE_ASSET_URLS_INLINE_FORMAT, STYLE_ASSET_URLS_RE,
    STYLE_ASSET_URLS_SUB_FORMAT, STYLE_URLS_RES, STYLE_URLS_SOURCE,
    SUPPORTED_EXTENSIONS, SUPPORTED_TITLES, AlreadyRunningError,
    DirectoryReader, GitHubAssetManager, GitHubRenderer, Grip, OfflineRenderer,
    ReadmeAssetManager, ReadmeNotFoundError, ReadmeReader, ReadmeRenderer,
    TextReader, clear_cache, create_app, export, main, render_content,
    render_page, serve)


# TODO: Test DEFAULT_API_URL, DEFAULT_FILENAMES, DEFAULT_GRIPHOME,
#       DEFAULT_GRIPURL, DEFAULT_GRIPURL, STYLE_ASSET_URLS_RE,
#       STYLE_ASSET_URLS_SUB_FORMAT, STYLE_URLS_RES, STYLE_URLS_SOURCE,
#       SUPPORTED_EXTENSIONS, SUPPORTED_TITLES, ReadmeAssetManager,
#       clear_cache, export, main, render_content, render_page, serve


DIRNAME = os.path.dirname(os.path.abspath(__file__))


def test_exceptions():
    """
    Test that ReadmeNotFoundError behaves like FileNotFoundError on
    Python 3 and IOError on Python 2.
    """
    assert str(ReadmeNotFoundError()) == 'README not found'
    assert (str(ReadmeNotFoundError('.')) == 'No README found at .')
    assert str(ReadmeNotFoundError('some/path', 'Overridden')) == 'Overridden'
    assert ReadmeNotFoundError().filename is None
    assert ReadmeNotFoundError(DEFAULT_FILENAME).filename == DEFAULT_FILENAME


def test_readme_reader():
    with pytest.raises(TypeError):
        ReadmeReader()


def test_directory_reader():
    input_path = 'input'
    markdown_path = posixpath.join(input_path, 'gfm-test.md')
    default_path = posixpath.join(input_path, 'default')
    input_img_path = posixpath.join(input_path, 'img.png')

    input_dir = os.path.join(DIRNAME, 'input')
    markdown_file = os.path.join(input_dir, 'gfm-test.md')
    default_dir = os.path.join(input_dir, 'default')
    default_file = os.path.join(default_dir, DEFAULT_FILENAME)

    DirectoryReader(input_filename('default'))
    DirectoryReader(input_filename(default_file))
    DirectoryReader(input_filename(default_file), silent=True)
    DirectoryReader(input_filename('empty'), silent=True)
    with pytest.raises(ReadmeNotFoundError):
        DirectoryReader(input_filename('empty'))
    with pytest.raises(ReadmeNotFoundError):
        DirectoryReader(input_filename('empty', DEFAULT_FILENAME))

    reader = DirectoryReader(DIRNAME, silent=True)
    assert reader.root_filename == os.path.join(DIRNAME, DEFAULT_FILENAME)
    assert reader.root_directory == DIRNAME

    assert reader.normalize_subpath(None) is None
    assert reader.normalize_subpath('.') == './'
    assert reader.normalize_subpath('./././') == './'
    assert reader.normalize_subpath('non-existent/.././') == './'
    assert reader.normalize_subpath('non-existent/') == 'non-existent'
    assert reader.normalize_subpath('non-existent') == 'non-existent'
    with pytest.raises(NotFound):
        reader.normalize_subpath('../unsafe')
    with pytest.raises(NotFound):
        reader.normalize_subpath('/unsafe')
    assert reader.normalize_subpath(input_path) == input_path + '/'
    assert reader.normalize_subpath(markdown_path) == markdown_path
    assert reader.normalize_subpath(markdown_path + '/') == markdown_path

    assert reader.readme_for(None) == os.path.join(DIRNAME, DEFAULT_FILENAME)
    with pytest.raises(ReadmeNotFoundError):
        reader.readme_for('non-existent')
    with pytest.raises(ReadmeNotFoundError):
        reader.readme_for(input_path)
    assert reader.readme_for(markdown_path) == os.path.abspath(markdown_file)
    assert reader.readme_for(default_path) == os.path.abspath(default_file)

    # TODO: 'README.md' vs 'readme.md'

    assert reader.filename_for(None) == DEFAULT_FILENAME
    assert reader.filename_for(input_path) is None
    assert reader.filename_for(default_path) == os.path.relpath(
        default_file, reader.root_directory)

    assert not reader.is_binary()
    assert not reader.is_binary(input_path)
    assert not reader.is_binary(markdown_path)
    assert reader.is_binary(input_img_path)

    assert reader.last_updated() is None
    assert reader.last_updated(input_path) is None
    assert reader.last_updated(markdown_path) is not None
    assert reader.last_updated(default_path) is not None
    assert DirectoryReader(default_dir).last_updated is not None

    with pytest.raises(ReadmeNotFoundError):
        assert reader.read(input_path) is not None
    assert reader.read(markdown_path)
    assert reader.read(default_path)
    with pytest.raises(ReadmeNotFoundError):
        assert reader.read()
    assert DirectoryReader(default_dir).read() is not None


def test_text_reader():
    text = 'Test *Text*'
    filename = DEFAULT_FILENAME

    assert TextReader(text).normalize_subpath(None) is None
    assert TextReader(text).normalize_subpath('././.') == '.'
    assert TextReader(text).normalize_subpath(filename) == filename

    assert TextReader(text).filename_for(None) is None
    assert TextReader(text, filename).filename_for(None) == filename
    assert TextReader(text, filename).filename_for('.') is None

    assert TextReader(text).last_updated() is None
    assert TextReader(text, filename).last_updated() is None
    assert TextReader(text, filename).last_updated('.') is None
    assert TextReader(text, filename).last_updated(filename) is None

    assert TextReader(text).read() == text
    assert TextReader(text, filename).read() == text
    with pytest.raises(ReadmeNotFoundError):
        TextReader(text).read('.')
    with pytest.raises(ReadmeNotFoundError):
        TextReader(text, filename).read('.')
    with pytest.raises(ReadmeNotFoundError):
        TextReader(text, filename).read(filename)


def test_stdin_reader():
    text = 'Test *STDIN*'
    filename = DEFAULT_FILENAME

    assert StdinReaderMock(text).normalize_subpath(None) is None
    assert StdinReaderMock(text).normalize_subpath('././.') == '.'
    assert StdinReaderMock(text).normalize_subpath(filename) == filename

    assert StdinReaderMock(text).filename_for(None) is None
    assert StdinReaderMock(text, filename).filename_for(None) == filename
    assert StdinReaderMock(text, filename).filename_for('.') is None

    assert StdinReaderMock(text).last_updated() is None
    assert StdinReaderMock(text, filename).last_updated() is None
    assert StdinReaderMock(text, filename).last_updated('.') is None
    assert StdinReaderMock(text, filename).last_updated(filename) is None

    assert StdinReaderMock(text).read() == text
    assert StdinReaderMock(text, filename).read() == text
    with pytest.raises(ReadmeNotFoundError):
        StdinReaderMock(text).read('.')
    with pytest.raises(ReadmeNotFoundError):
        StdinReaderMock(text, filename).read('.')
    with pytest.raises(ReadmeNotFoundError):
        StdinReaderMock(text, filename).read(filename)


def test_readme_renderer():
    with pytest.raises(TypeError):
        ReadmeRenderer()


def test_github_renderer():
    simple_input = input_file('simple.md')
    gfm_test_input = input_file('gfm-test.md')

    with GitHubRequestsMock() as responses:
        assert (GitHubRenderer().render(simple_input) ==
                output_file('renderer', 'simple.html'))
        assert (GitHubRenderer(True).render(simple_input) ==
                output_file('renderer', 'simple-user-content.html'))
        assert (GitHubRenderer(True).render(simple_input) ==
                output_file('renderer', 'simple-user-context.html'))
        assert len(responses.calls) == 3

    assert (output_file('renderer', 'gfm-test-user-content.html') !=
            output_file('renderer', 'gfm-test-user-context.html'))

    with GitHubRequestsMock() as responses:
        assert (GitHubRenderer().render(gfm_test_input) ==
                output_file('renderer', 'gfm-test.html'))
        assert (GitHubRenderer(True).render(gfm_test_input) ==
                output_file('renderer', 'gfm-test-user-content.html'))
        assert (GitHubRenderer(True, USER_CONTEXT).render(gfm_test_input) ==
                output_file('renderer', 'gfm-test-user-context.html'))
        assert len(responses.calls) == 3

    with GitHubRequestsMock() as responses:
        assert (
            GitHubRenderer().render(simple_input, GitHubRequestsMock.auth) ==
            output_file('renderer', 'simple.html'))
        with pytest.raises(HTTPError):
            GitHubRenderer().render(simple_input, GitHubRequestsMock.bad_auth)
        assert len(responses.calls) == 2


def test_offline_renderer():
    # TODO: Test all GitHub rendering features and get the renderer to pass
    # FUTURE: Expose OfflineRenderer once all Markdown features are tested
    pass


def test_readme_asset_manager():
    with pytest.raises(TypeError):
        ReadmeRenderer()


def test_github_asset_manager(tmpdir):
    cache_dir = tmpdir.mkdir('cache-dummy')
    assets = GitHubAssetManager(str(cache_dir))

    cache_dir.join('dummy1.css').write_text('', 'utf-8')
    cache_dir.join('dummy2.css').write_text('', 'utf-8')
    assert len(cache_dir.listdir()) == 2
    assets.clear()
    assert not cache_dir.check()

    # TODO: Test style retrieval on a fresh cache
    # TODO: Test that an existing cache is used when styles are requested
    # TODO: Test the upgrade case (cache-x.y.z should be fresh)


# TODO: test_browser?


def test_app(monkeypatch, tmpdir):
    monkeypatch.setenv('GRIPHOME', str(tmpdir))
    zero_path = input_filename('zero.md')
    zero_output = output_file('app', 'zero.html')
    gfm_test_path = input_filename('gfm-test.md')
    gfm_test_output = output_file('app', 'gfm-test.html')
    assets = GitHubAssetManagerMock()

    with GitHubRequestsMock() as responses:
        assert Grip(zero_path, assets=assets).render() == zero_output
        assert Grip(zero_path, assets=assets).render('/') == zero_output
        assert Grip(zero_path, assets=assets).render('/x/../') == zero_output
        with Grip(zero_path, assets=assets).test_client() as client:
            assert client.get('/').data.decode('utf-8') == zero_output
        assert len(responses.calls) == 4

    with GitHubRequestsMock() as responses:
        app = Grip(gfm_test_path, assets=assets)
        assert app.render() == gfm_test_output
        assert app.render('/') == gfm_test_output
        assert len(responses.calls) == 2

    # TODO: Test all constructor parameters
    # TODO: Test other methods
    # TODO: cd('input', 'default') and run on cwd
    # TODO: Test 403 responses
    # TODO: Test behaviors? -> anchor tags, autorefresh


def test_api():
    assert isinstance(create_app(grip_class=GripMock), GripMock)

    # TODO: Test all API functions and argument combinations


def test_command():
    # TODO: Test main(argv) with all command and argument combinations
    # TODO: Test autorefresh by mimicking the browser with a manually GET
    # TODO: Test browser opening using monkey patching?
    pass
