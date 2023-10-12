"""\
Grip
----

Render local readme files before sending off to GitHub.

:copyright: (c) 2014-2022 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

__version__ = '4.6.2'  # noqa

import sys

# Patch for Flask 11.0+ on Python 3 (pypy3)
if not hasattr(sys, 'exc_clear'):  # noqa
    sys.exc_clear = lambda: None

from .api import (
    clear_cache, create_app, export, render_content, render_page, serve)
from .app import Grip
from .assets import GitHubAssetManager, ReadmeAssetManager
from .command import main
from .constants import (
    DEFAULT_API_URL, DEFAULT_FILENAMES, DEFAULT_FILENAME, DEFAULT_GRIPHOME,
    DEFAULT_GRIPURL, STYLE_ASSET_URLS_INLINE_FORMAT, STYLE_ASSET_URLS_RE,
    STYLE_ASSET_URLS_SUB_FORMAT, STYLE_URLS_RES, STYLE_URLS_SOURCE,
    SUPPORTED_EXTENSIONS, SUPPORTED_TITLES)
from .exceptions import AlreadyRunningError, ReadmeNotFoundError
from .readers import ReadmeReader, DirectoryReader, StdinReader, TextReader
from .renderers import ReadmeRenderer, GitHubRenderer, OfflineRenderer


__all__ = [
    '__version__',

    'DEFAULT_API_URL', 'DEFAULT_FILENAMES', 'DEFAULT_FILENAME',
    'DEFAULT_GRIPHOME', 'DEFAULT_GRIPURL', 'STYLE_ASSET_URLS_INLINE_FORMAT',
    'STYLE_ASSET_URLS_RE', 'STYLE_ASSET_URLS_SUB_FORMAT', 'STYLE_URLS_RES',
    'STYLE_URLS_SOURCE', 'SUPPORTED_EXTENSIONS', 'SUPPORTED_TITLES',

    'AlreadyRunningError', 'DirectoryReader', 'GitHubAssetManager',
    'GitHubRenderer', 'Grip', 'OfflineRenderer', 'ReadmeNotFoundError',
    'ReadmeAssetManager', 'ReadmeReader', 'ReadmeRenderer', 'StdinReader',
    'TextReader',

    'clear_cache', 'create_app', 'export', 'main', 'render_content',
    'render_page', 'serve',
]
