from __future__ import print_function, unicode_literals

import base64
import json
import mimetypes
import os
import posixpath
import re
import sys
import threading
import time
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

import requests
from flask import (
    Flask, Response, abort, redirect, render_template, request,
    send_from_directory, url_for)

from . import __version__
from .assets import AssetManager, GitHubAssetManager
from .browser import start_browser_when_ready
from .constants import (
    DEFAULT_GRIPHOME, DEFAULT_GRIPURL, STYLE_ASSET_URLS_INLINE_FORMAT)
from .exceptions import AlreadyRunningError
from .readers import DirectoryReader
from .renderers import GitHubRenderer, ReadmeRenderer


class Grip(Flask):
    """
    A Flask application that can serve the specified file or directory
    containing a README.
    """
    def __init__(self, source=None, auth=None, renderer=None,
                 assets=None, render_wide=None, render_inline=None, title=None,
                 autorefresh=None, quiet=None, grip_url=None,
                 static_url_path=None, instance_path=None, **kwargs):
        # Defaults from ENV
        if instance_path is None:
            instance_path = os.environ.get('GRIPHOME')
            if instance_path is None:
                instance_path = DEFAULT_GRIPHOME
        instance_path = os.path.abspath(os.path.expanduser(instance_path))
        if grip_url is None:
            grip_url = os.environ.get('GRIPURL')
            if grip_url is None:
                grip_url = DEFAULT_GRIPURL
        grip_url = grip_url.rstrip('/')
        if static_url_path is None:
            static_url_path = posixpath.join(grip_url, 'static')

        # Flask application
        super(Grip, self).__init__(
            __name__, static_url_path=static_url_path,
            instance_path=instance_path, **kwargs)
        self.config.from_object('grip.settings')
        self.config.from_pyfile('settings_local.py', silent=True)
        self.config.from_pyfile(
            os.path.join(instance_path, 'settings.py'), silent=True)

        # Defaults from settings
        if render_inline is None:
            render_inline = False
        if autorefresh is None:
            autorefresh = self.config['AUTOREFRESH']

        # Thread-safe event to signal to the polling threads to exit
        self._run_mutex = threading.Lock()
        self._shutdown_event = None

        # Parameterized attributes
        self.auth = auth
        self.autorefresh = autorefresh
        self.reader = (DirectoryReader(source)
                       if source is None or isinstance(source, basestring)
                       else source)
        self.renderer = renderer
        self.assets = assets
        self.render_wide = render_wide
        self.render_inline = render_inline
        self.title = title
        self.quiet = self.config['QUIET']

        # Contextual attributes
        if self.renderer is None:
            self.renderer = self.default_renderer()
            if not isinstance(self.renderer, ReadmeRenderer):
                raise ValueError(
                    'Expected Grip.default_renderer to return '
                    'a ReadmeRenderer instance, got None.')
        if self.assets is None:
            assets = self.default_asset_manager()
            if not isinstance(assets, AssetManager):
                raise ValueError(
                    'Expected Grip.default_asset_manager to return '
                    'an AssetManager instance, got {}.'.format(type(assets)))
            self.assets = assets

        # Add missing content types
        self.add_content_types()

        # Construct routes
        asset_route = posixpath.join(grip_url, 'asset', '')
        asset_subpath = posixpath.join(asset_route, '<path:subpath>')
        refresh_route = posixpath.join(grip_url, 'refresh', '')
        refresh_subpath = posixpath.join(refresh_route, '<path:subpath>')
        rate_limit_route = posixpath.join(grip_url, 'rate-limit-preview')

        # Initialize views
        self.before_first_request(self.retrieve_styles)
        self.add_url_rule(asset_route, 'asset', self._render_asset)
        self.add_url_rule(asset_subpath, 'asset', self._render_asset)
        self.add_url_rule('/', 'render', self._render_page)
        self.add_url_rule('/<path:subpath>', 'render', self._render_page)
        self.add_url_rule(refresh_route, 'refresh', self._render_refresh)
        self.add_url_rule(refresh_subpath, 'refresh', self._render_refresh)
        self.add_url_rule(rate_limit_route, 'rate_limit',
                          self._render_rate_limit_page)
        self.errorhandler(403)(self._render_rate_limit_page)

    def _render_asset(self, subpath):
        """
        Renders the specified cache file.
        """
        # FUTURE: Use subpath exactly instead of flattening it here
        return send_from_directory(
            self.assets.cache_path, posixpath.basename(subpath))

    def _render_page(self, subpath=None):
        # Normalize the subpath
        normalized = self.reader.normalize(subpath)
        if normalized != subpath:
            return redirect(normalized)

        # Get the contextual or overridden title
        title = ('{} - Grip'.format(self.reader.filename_for(subpath))
                 if self.title is None
                 else self.title)

        # Read the Readme text or asset
        data = self.reader.read(subpath)
        if data is None:
            abort(404)

        # Return binary asset
        if self.reader.is_binary(subpath):
            mimetype = self.reader.mimetype_for(subpath)
            return Response(data, mimetype=mimetype)

        # Render the Readme content
        content = self.renderer.render(data)

        # Inline favicon asset
        favicon = None
        if self.render_inline:
            favicon_url = url_for('static', filename='favicon.ico')
            favicon = self._to_data_url(favicon_url, 'image/x-icon')

        autorefresh_url = (url_for('refresh', subpath=subpath)
                           if self.autorefresh
                           else None)

        return render_template(
            'index.html', title=title, content=content, favicon=favicon,
            user_content=self.renderer.user_content,
            wide_style=self.render_wide, style_urls=self.assets.style_urls,
            styles=self.assets.styles, autorefresh_url=autorefresh_url)

    def _render_refresh(self, subpath=None):
        if not self.autorefresh:
            abort(404)

        # Normalize the subpath
        normalized = self.reader.normalize(subpath)
        if normalized != subpath:
            return redirect(normalized)

        # Get the full filename for display
        filename = self.reader.filename_for(subpath)

        # Check whether app is running
        shutdown_event = self._shutdown_event
        if not shutdown_event or shutdown_event.is_set():
            return ''

        def gen():
            last_updated = self.reader.last_updated(subpath)
            try:
                while not shutdown_event.is_set():
                    time.sleep(0.3)

                    # Check for update
                    updated = self.reader.last_updated(subpath)
                    if updated == last_updated:
                        continue
                    last_updated = updated
                    # Notify user that a refresh is in progress
                    if not self.quiet:
                        print(' * Change detected in {}, refreshing'
                              .format(filename))
                    yield 'data: {}\r\n\r\n'.format(
                        json.dumps({'updating': True}))
                    # Binary assets not supported
                    if self.reader.is_binary(subpath):
                        return
                    # Read the Readme text
                    text = self.reader.read(subpath)
                    if text is None:
                        return
                    # Render the Readme content
                    content = self.renderer.render(text)
                    # Return the Readme content
                    yield 'data: {}\r\n\r\n'.format(
                        json.dumps({'content': content}))
            except GeneratorExit:
                pass

        return Response(gen(), mimetype='text/event-stream')

    def _render_rate_limit_page(self, exception=None):
        """
        Renders the rate limit page.
        """
        auth = request.args.get('auth')
        is_auth = auth == '1' if auth else bool(self.auth)
        return render_template('limit.html', is_authenticated=is_auth), 403

    def _download(self, url, binary=False):
        if urlparse(url).netloc:
            r = requests.get(url)
            return r.content if binary else r.text

        with self.test_client() as c:
            r = c.get(url)
            charset = r.mimetype_params.get('charset', 'utf-8')
            data = c.get(url).data
            return data if binary else data.decode(charset)

    def _to_data_url(self, url, content_type):
        asset = self._download(url, binary=True)
        asset64_bytes = base64.b64encode(asset)
        asset64_string = asset64_bytes.decode('ascii')
        return 'data:{0};base64,{1}'.format(content_type, asset64_string)

    def _normalize_url(self, url):
        return url.rsplit('?', 1)[0].rsplit('#', 1)[0]

    def _get_inline_styles(self, style_urls):
        """
        Gets the content of the given list of style URLs and
        inlines assets.
        """
        asset_url = url_for('asset').rstrip('/') or '/'

        styles = []
        for style_url in style_urls:

            def match_asset(match):
                url = urljoin(style_url, self._normalize_url(match.group(1)))
                ext = os.path.splitext(url)[1][1:]
                return 'url({0})'.format(
                    self._to_data_url(url, 'font/' + ext))

            urls_inline = STYLE_ASSET_URLS_INLINE_FORMAT.format(asset_url)
            asset_content = self._download(style_url)
            content = re.sub(urls_inline, match_asset, asset_content)
            styles.append(content)

        return styles

    def retrieve_styles(self):
        """
        Retrieves the style URLs from the source and caches them. This
        is called before the first request is dispatched.
        """
        # Get style URLs
        self.assets.retrieve_styles(url_for('asset'))

        # Download styles directly and clear the URLs when inlining
        if self.render_inline:
            # TODO: Refactor and move to asset manager
            self.assets.styles.extend(
                self._get_inline_styles(self.assets.style_urls))
            self.assets.style_urls[:] = []

    def default_renderer(self):
        """
        Returns the default renderer using the current config.

        This is only used if renderer is set to None in the constructor.
        """
        return GitHubRenderer(api_url=self.config['API_URL'])

    def default_asset_manager(self):
        """
        Returns the default asset manager using the current config.

        This is only used if asset_manager is set to None in the constructor.
        """
        # TODO: Finish this
        cache_directory = self.config['CACHE_DIRECTORY']
        if cache_directory is not None:
            cache_path = os.path.join(
                self.instance_path,
                cache_directory.format(version=__version__))
        else:
            cache_path = None
        return GitHubAssetManager(
            cache_path, self.config['STYLE_URLS'], self.config['DEBUG_GRIP'])

    def add_content_types(self):
        """
        Adds the application/x-font-woff and application/octet-stream
        content types if they are missing.

        Override to add additional content types on initialization.
        """
        mimetypes.add_type('application/x-font-woff', '.woff')
        mimetypes.add_type('application/octet-stream', '.ttf')

    def clear_cache(self):
        self.assets.clear()
        if not self.quiet:
            print('Cache cleared.')

    def render(self, route=None):
        """
        Renders the application and returns the HTML unicode that would
        normally appear when visiting in the browser.
        """
        if route is None:
            route = '/'
        with self.test_client() as c:
            response = c.get(route)
            encoding = response.charset
            return response.data.decode(encoding)

    def run(self, host=None, port=None, debug=None, use_reloader=None,
            open_browser=False):
        """
        Starts a server to render the README.
        """
        if host is None:
            host = self.config['HOST']
        if port is None:
            port = self.config['PORT']
        if debug is None:
            debug = self.debug
        if use_reloader is None:
            use_reloader = self.config['DEBUG_GRIP']

        # Verify the server is not already running and start
        with self._run_mutex:
            if self._shutdown_event:
                raise AlreadyRunningError()
            self._shutdown_event = threading.Event()

        # Authentication message
        if self.auth and not self.quiet:
            auth_method = ('credentials: {}'.format(self.renderer.username)
                           if (isinstance(self.renderer, GitHubRenderer) and
                               self.renderer.username)
                           else 'personal access token')
            print(' * Using', auth_method, file=sys.stderr)

        # Open browser
        browser_thread = (
            start_browser_when_ready(host, port, self._shutdown_event)
            if open_browser else None)

        # Run local server
        super(Grip, self).run(host, port, debug=debug,
                              use_reloader=use_reloader,
                              threaded=True)

        # Signal to the polling and browser threads that they should exit
        if not self.quiet:
            print(' * Shutting down...')
        self._shutdown_event.set()

        # Wait for browser thread to finish
        if browser_thread:
            browser_thread.join()

        # Cleanup
        self._shutdown_event = None