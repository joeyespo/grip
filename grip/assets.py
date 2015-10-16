from __future__ import print_function, unicode_literals

import errno
import os
import posixpath
import re
import sys
import shutil
from abc import ABCMeta, abstractmethod
from traceback import format_exc
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests

from .constants import (
    STYLE_URLS_SOURCE, STYLE_URLS_RE, STYLE_ASSET_URLS_RE,
    STYLE_ASSET_URLS_SUB_FORMAT)


class AssetManager(object):
    """
    Manages the style and font assets rendered with Readme pages.

    Set cache_path to None to disable caching.
    """
    __metaclass__ = ABCMeta

    def __init__(self, cache_path, style_urls=None):
        super(AssetManager, self).__init__()
        self.cache_path = cache_path
        self.style_urls = list(style_urls) if style_urls else []
        self.styles = []

    def clear(self):
        """
        Clears the asset cache.
        """
        if self.cache_path and os.path.exists(self.cache_path):
            shutil.rmtree(self.cache_path)

    @abstractmethod
    def retrieve_styles(self, asset_url):
        """
        Get style URLs from the source HTML page and specified cached
        asset base URL.
        """
        pass


class GitHubAssetManager(AssetManager):
    """
    Reads the styles used for rendering Readme pages.

    Set cache_path to None to disable caching.
    """
    def __init__(self, cache_path, style_urls=None, debug=None):
        super(GitHubAssetManager, self).__init__(cache_path, style_urls)
        self.debug = debug if debug is not None else False

    def _get_style_urls(self, asset_url):
        """
        Gets the specified resource and parses all style URLs and their
        assets in the form of the specified patterns.
        """
        try:
            # Check cache
            if self.cache_path:
                cached = self._get_cached_style_urls(asset_url)
                # Skip fetching styles if there's any already cached
                if cached:
                    return cached

            # Find style URLs
            r = requests.get(STYLE_URLS_SOURCE)
            if not 200 <= r.status_code < 300:
                print('Warning: retrieving styles gave status code',
                      r.status_code, file=sys.stderr)
            urls = re.findall(STYLE_URLS_RE, r.text)

            # Cache the styles and their assets
            if self.cache_path:
                is_cached = self._cache_contents(urls, asset_url)
                if is_cached:
                    urls = self._get_cached_style_urls(asset_url)

            return urls
        except Exception as ex:
            # TODO: Extract printing and debug info to app?
            if self.debug:
                print(format_exc(), file=sys.stderr)
            else:
                print(' * Error: could not retrieve styles:', ex,
                      file=sys.stderr)
            return []

    def _get_cached_style_urls(self, asset_url):
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
        return [posixpath.join(asset_url, style)
                for style in cached_styles
                if style.endswith('.css')]

    def _write_binary_file(self, filename, data):
        """
        Creates the specified file and writes binary data to it.
        """
        with open(filename, 'wb') as f:
            f.write(data)

    def _cache_contents(self, style_urls, asset_url):
        """
        Fetches the given URLs and caches their contents
        and their assets in the given directory.
        """
        files = {}

        asset_urls = []
        for style_url in style_urls:
            print(' * Downloading style', style_url, file=sys.stderr)
            filename = self._cache_filename(style_url)
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
                STYLE_ASSET_URLS_SUB_FORMAT.format(asset_url),
                asset_content)
            # Prepare cache
            if files is not None:
                files[filename] = contents.encode('utf-8')

        for asset_url in asset_urls:
            print(' * Downloading asset', asset_url, file=sys.stderr)
            filename = self._cache_filename(asset_url)
            # Retrieve binary file and show message
            r = requests.get(asset_url, stream=True)
            if not 200 <= r.status_code < 300:
                print(' -> Warning: Asset request responded with',
                      r.status_code, file=sys.stderr)
                files = None
                continue
            # Prepare cache
            if files is not None:
                files[filename] = r.raw.read(decode_content=True)

        # Skip caching if something went wrong to try again next time
        if not files:
            return False

        # Cache files if all downloads were successful
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        for filename in files:
            self._write_binary_file(filename, files[filename])

        print(' * Cached all downloads in', self.cache_path, file=sys.stderr)
        return True

    def _cache_filename(self, url):
        if '?' in url:
            url = url[:url.find('?')]
        if '#' in url:
            url = url[:url.find('#')]
        # FUTURE: Use url exactly instead of flattening it here
        return os.path.join(self.cache_path, posixpath.basename(url))

    def _normalize_base_url(self, url):
        return (url or '/').rstrip('/') or '/'

    def retrieve_styles(self, asset_url):
        """
        Get style URLs from the source HTML page and specified cached
        asset base URL.
        """
        self.style_urls.extend(
            self._get_style_urls(self._normalize_base_url(asset_url)))
