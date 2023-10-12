from __future__ import print_function, unicode_literals

import errno
import os
import posixpath
import re
import sys
import shutil
from abc import ABCMeta, abstractmethod
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests

from ._compat import safe_join

from .constants import (
    STYLE_URLS_SOURCE, STYLE_URLS_RES, STYLE_ASSET_URLS_RE,
    STYLE_ASSET_URLS_SUB_FORMAT, SCRIPT_FILENAMES_RES,
    SCRIPT_URLS_SOURCE, SCRIPT_URLS_RES)
from .vendor.six import add_metaclass


@add_metaclass(ABCMeta)
class ReadmeAssetManager(object):
    """
    Manages the style and font assets rendered with Readme pages.

    Set cache_path to None to disable caching.
    """
    def __init__(self, cache_path, style_urls=None, quiet=None):
        super(ReadmeAssetManager, self).__init__()
        self.cache_path = cache_path
        self.style_urls = list(style_urls) if style_urls else []
        self.styles = []
        self.script_urls = []
        self.quiet = quiet

    def _strip_url_params(self, url):
        return url.rsplit('?', 1)[0].rsplit('#', 1)[0]

    def clear(self):
        """
        Clears the asset cache.
        """
        if self.cache_path and os.path.exists(self.cache_path):
            shutil.rmtree(self.cache_path)

    def cache_filename(self, url):
        """
        Gets a suitable relative filename for the specified URL.
        """
        # FUTURE: Use url exactly instead of flattening it here
        url = posixpath.basename(url)
        return self._strip_url_params(url)

    @abstractmethod
    def retrieve_styles(self, asset_url_path):
        """
        Get style URLs from the source HTML page and specified cached asset
        URL path.
        """
        pass

    @abstractmethod
    def retrieve_scripts(self, asset_url_path):
        """
        Get scripts URLs from the source HTML page and specified cached asset
        URL path.
        """
        pass


class GitHubAssetManager(ReadmeAssetManager):
    """
    Reads the styles used for rendering Readme pages.

    Set cache_path to None to disable caching.
    """
    def __init__(self, cache_path, style_urls=None, quiet=None):
        super(GitHubAssetManager, self).__init__(cache_path, style_urls, quiet)

    def _get_style_urls(self, asset_url_path):
        """
        Gets the specified resource and parses all style URLs and their
        assets in the form of the specified patterns.
        """
        # Check cache
        if self.cache_path:
            cached = self._get_cached_style_urls(asset_url_path)
            # Skip fetching styles if there's any already cached
            if cached:
                return cached

        # Find style URLs
        r = requests.get(STYLE_URLS_SOURCE)
        if not 200 <= r.status_code < 300:
            print('Warning: retrieving styles gave status code',
                  r.status_code, file=sys.stderr)
        urls = []
        content = r.text
        for style_urls_re in STYLE_URLS_RES:
            print(re.findall(style_urls_re, content))
            urls.extend(re.findall(style_urls_re, content))
        if not urls:
            print('Warning: no styles found - see https://github.com/joeyespo/'
                  'grip/issues/265', file=sys.stderr)

        # Cache the styles and their assets
        if self.cache_path:
            is_cached = self._cache_contents(urls, asset_url_path)
            if is_cached:
                urls = self._get_cached_style_urls(asset_url_path)

        return urls

    def _get_script_urls(self, asset_url_path):
        """
        Gets the specified resource and parses all style URLs and their
        assets in the form of the specified patterns.
        """
        # Check cache
        if self.cache_path:
            cached = self._get_cached_script_urls(asset_url_path)
            # Skip fetching styles if there's any already cached
            if cached:
                return cached

        # Find script URLs
        r = requests.get(SCRIPT_URLS_SOURCE)
        if not 200 <= r.status_code < 300:
            print('Warning: retrieving script gave status code',
                  r.status_code, file=sys.stderr)
        urls = []
        content = r.text
        for script_urls_re in SCRIPT_URLS_RES:
            print(re.findall(script_urls_re, content))
            urls.extend(re.findall(script_urls_re, content))
        if not urls:
            print('Warning: no script found - see https://github.com/joeyespo/'
                  'grip/issues/265', file=sys.stderr)

        # Cache the script and their assets
        if self.cache_path:
            is_cached = self._cache_contents(urls, asset_url_path)
            if is_cached:
                urls = self._get_cached_script_urls(asset_url_path)

        return urls

    def _get_cached_style_urls(self, asset_url_path):
        """
        Gets the URLs of the cached styles.
        """
        try:
            cached_styles = os.listdir(self.cache_path)
        except IOError as ex:
            if ex.errno != errno.ENOENT and ex.errno != errno.ESRCH:
                raise
            return []
        except OSError:
            return []
        return [posixpath.join(asset_url_path, style)
                for style in cached_styles
                if style.endswith('.css')]

    def _get_cached_script_urls(self, asset_url_path):
        """
        Gets the URLs of the cached scripts.
        """
        try:
            cached_scripts = os.listdir(self.cache_path)
        except IOError as ex:
            if ex.errno != errno.ENOENT and ex.errno != errno.ESRCH:
                raise
            return []
        except OSError:
            return []
        return [posixpath.join(asset_url_path, script)
                for script in cached_scripts
                if script.endswith('.js')]

    def _cache_contents(self, style_urls, asset_url_path):
        """
        Fetches the given URLs and caches their contents
        and their assets in the given directory.
        """
        files = {}

        asset_urls = []
        for style_url in style_urls:
            if not self.quiet:
                print(' * Downloading style or script', style_url, file=sys.stderr)
            r = requests.get(style_url)
            if not 200 <= r.status_code < 300:
                print(' -> Warning: Style request responded with',
                      r.status_code, file=sys.stderr)
                files = None
                continue
            asset_content = r.text
            # Find assets and replace their base URLs with the cache directory
            for url in re.findall(STYLE_ASSET_URLS_RE, asset_content):
                asset_urls.append(urljoin(style_url, url))
            contents = re.sub(
                STYLE_ASSET_URLS_RE,
                STYLE_ASSET_URLS_SUB_FORMAT.format(asset_url_path.rstrip('/')),
                asset_content)
            # Prepare cache
            if files is not None:
                filename = self.cache_filename(style_url)
                files[filename] = contents.encode('utf-8')

        for asset_url in asset_urls:
            if not self.quiet:
                print(' * Downloading asset', asset_url, file=sys.stderr)
            # Retrieve binary file and show message
            r = requests.get(asset_url, stream=True)
            if not 200 <= r.status_code < 300:
                print(' -> Warning: Asset request responded with',
                      r.status_code, file=sys.stderr)
                files = None
                continue
            # Prepare cache
            if files is not None:
                filename = self.cache_filename(asset_url)
                files[filename] = r.raw.read(decode_content=True)

        # Skip caching if something went wrong to try again next time
        if not files:
            return False

        # Cache files if all downloads were successful
        cache = {}
        for relname in files:
            cache[safe_join(self.cache_path, relname)] = files[relname]
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        for filename in cache:
            with open(filename, 'wb') as f:
                f.write(cache[filename])
        if not self.quiet:
            print(
                ' * Cached all downloads in', self.cache_path, file=sys.stderr)
        return True

    def retrieve_styles(self, asset_url_path):
        """
        Get style URLs from the source HTML page and specified cached
        asset base URL.
        """
        if not asset_url_path.endswith('/'):
            asset_url_path += '/'
        self.style_urls.extend(self._get_style_urls(asset_url_path))

    def cache_asset (self, asset_url):
        if not asset_url.startswith('math_renderer/'):
            asset_url = 'https://github.com/assets/%s' %asset_url
        else:
            asset_url = asset_url[len("math_renderer/"):]
            asset_url = 'https://github.githubassets.com/static/%s' %asset_url
        r = requests.get(asset_url, stream=True)
        if not 200 <= r.status_code < 300:
            print(' -> Warning: Asset request responded with',
                  r.status_code, file=sys.stderr)
            print(' -> try to use the "--clear" option')
            return

        filename = self.cache_filename(asset_url)
        file_content = r.raw.read(decode_content=True)

        # Cache file if the download was successful
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        filename = safe_join(self.cache_path, filename)
        with open(filename, 'wb') as f:
            f.write(file_content)

    def retrieve_scripts(self, asset_url_path):
        """
        Get script URLs from the source HTML page and specified cached
        asset base URL.
        """
        if not asset_url_path.endswith('/'):
            asset_url_path += '/'
        urls = self._get_script_urls(asset_url_path)
        script_urls = []
        for script_filename_re in SCRIPT_FILENAMES_RES:
            script_urls += [script_url for script_url in urls if
                            re.search(script_filename_re, script_url)]
        self.script_urls.extend(script_urls)
