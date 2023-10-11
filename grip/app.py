from __future__ import print_function, unicode_literals

import base64
import json
import mimetypes
import os
import posixpath
import re
import socket
import sys
import threading
import time
import errno
from traceback import format_exc
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
try:
    str_type = basestring
except NameError:
    str_type = str

import requests
from flask import (
    Flask, Response, abort, redirect, render_template, request,
    send_from_directory, url_for)

from . import __version__
from .assets import GitHubAssetManager, ReadmeAssetManager
from .browser import start_browser_when_ready
from .constants import (
    DEFAULT_GRIPHOME, DEFAULT_GRIPURL, STYLE_ASSET_URLS_INLINE_FORMAT)
from .exceptions import AlreadyRunningError, ReadmeNotFoundError
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
        # Defaults
        if source is None or isinstance(source, str_type):
            source = DirectoryReader(source)
        if render_wide is None:
            render_wide = False
        if render_inline is None:
            render_inline = False

        # Defaults from ENV
        if grip_url is None:
            grip_url = os.environ.get('GRIPURL')
            if grip_url is None:
                grip_url = DEFAULT_GRIPURL
        grip_url = grip_url.rstrip('/')
        if static_url_path is None:
            static_url_path = posixpath.join(grip_url, 'static')
        if instance_path is None:
            instance_path = os.environ.get('GRIPHOME')
            if instance_path is None:
                instance_path = DEFAULT_GRIPHOME
        instance_path = os.path.abspath(os.path.expanduser(instance_path))

        # Flask application
        super(Grip, self).__init__(
            __name__, static_url_path=static_url_path,
            instance_path=instance_path, **kwargs)
        self.config.from_object('grip.settings')

        try:
            self.config.from_pyfile('settings_local.py', silent=True)
            self.config.from_pyfile(
                os.path.join(instance_path, 'settings.py'), silent=True)
        except IOError as ex:
            # Flask workaround for when ~/.grip exists but is not a directory
            if ex.errno != errno.ENOTDIR:
                raise

        # Defaults from settings
        if autorefresh is None:
            autorefresh = self.config['AUTOREFRESH']
        if quiet is None:
            quiet = self.config['QUIET']
        if auth is None:
            username = self.config['USERNAME']
            password = self.config['PASSWORD']
            if username or password:
                auth = (username or '', password or '')

        # Thread-safe event to signal to the polling threads to exit
        self._run_mutex = threading.Lock()
        self._shutdown_event = None

        # Parameterized attributes
        self.auth = auth
        self.autorefresh = autorefresh
        self.reader = source
        self.renderer = renderer
        self.assets = assets
        self.render_wide = render_wide
        self.render_inline = render_inline
        self.title = title
        self.quiet = quiet
        if self.quiet:
            import logging
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

        # Overridable attributes
        if self.renderer is None:
            renderer = self.default_renderer()
            if not isinstance(renderer, ReadmeRenderer):
                raise TypeError(
                    'Expected Grip.default_renderer to return a '
                    'ReadmeRenderer instance, got {0}.'.format(type(renderer)))
            self.renderer = renderer
        if self.assets is None:
            assets = self.default_asset_manager()
            if not isinstance(assets, ReadmeAssetManager):
                raise TypeError(
                    'Expected Grip.default_asset_manager to return an '
                    'ReadmeAssetManager instance, got {0}.'.format(
                        type(assets)))
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
        self._styles_retrieved = False
        self.before_request(self._retrieve_styles)
        self.add_url_rule(asset_route, 'asset', self._render_asset)
        self.add_url_rule(asset_subpath, 'asset', self._render_asset)
        self.add_url_rule('/', 'render', self._render_page)
        self.add_url_rule('/<path:subpath>', 'render', self._render_page)
        self.add_url_rule(refresh_route, 'refresh', self._render_refresh)
        self.add_url_rule(refresh_subpath, 'refresh', self._render_refresh)
        self.add_url_rule(rate_limit_route, 'rate_limit',
                          self._render_rate_limit_page)
        self.errorhandler(403)(self._render_rate_limit_page)

    def _redirect_to_subpath(self, subpath=None):
        """
        Redirects to the specified subpath, which is the relative path
        part of the root location (i.e. the current working directory
        or the path part of a URL excluding the initial '/').
        """
        route = posixpath.normpath('/' + (subpath or '').lstrip('/'))
        return redirect(route)

    def _render_asset(self, subpath):
        """
        Renders the specified cache file.
        """
        return send_from_directory(
            self.assets.cache_path, self.assets.cache_filename(subpath))

    def _render_page(self, subpath=None):
        # Normalize the subpath
        normalized = self.reader.normalize_subpath(subpath)
        if normalized != subpath:
            return self._redirect_to_subpath(normalized)

        # Read the Readme text or asset
        try:
            text = self.reader.read(subpath)
        except ReadmeNotFoundError:
            abort(404)

        # Return binary asset
        if self.reader.is_binary(subpath):
            mimetype = self.reader.mimetype_for(subpath)
            return Response(text, mimetype=mimetype)

        # Render the Readme content
        try:
            content = self.renderer.render(text, self.auth)
        except requests.HTTPError as ex:
            if ex.response.status_code == 403:
                abort(403)
            raise
        except requests.exceptions.SSLError as ex:
            if 'TLSV1_ALERT_PROTOCOL_VERSION' in str(ex):
                print('Error: GitHub has turned off TLS1.0 support. '
                      'Please upgrade your version of Python or Homebrew '
                      'to use a later version of openssl. '
                      'For more information, see '
                      'https://github.com/joeyespo/grip/issues/262')
                abort(500)
            raise

        # Inline favicon asset
        favicon = None
        if self.render_inline:
            favicon_url = url_for('static', filename='favicon.ico')
            favicon = self._to_data_url(favicon_url, 'image/x-icon')

        autorefresh_url = (url_for('refresh', subpath=subpath)
                           if self.autorefresh
                           else None)

        return render_template(
            'index.html', filename=self.reader.filename_for(subpath),
            title=self.title, content=content, favicon=favicon,
            user_content=self.renderer.user_content,
            wide_style=self.render_wide, style_urls=self.assets.style_urls,
            styles=self.assets.styles, autorefresh_url=autorefresh_url)

    def _render_refresh(self, subpath=None):
        if not self.autorefresh:
            abort(404)

        # Normalize the subpath
        normalized = self.reader.normalize_subpath(subpath)
        if normalized != subpath:
            return self._redirect_to_subpath(normalized)

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
                        print(' * Change detected in {0}, refreshing'
                              .format(filename))
                    yield 'data: {0}\r\n\r\n'.format(
                        json.dumps({'updating': True}))
                    # Binary assets not supported
                    if self.reader.is_binary(subpath):
                        return
                    # Read the Readme text
                    try:
                        text = self.reader.read(subpath)
                    except ReadmeNotFoundError:
                        return
                    # Render the Readme content
                    try:
                        content = self.renderer.render(text, self.auth)
                    except requests.HTTPError as ex:
                        if ex.response.status_code == 403:
                            abort(403)
                        raise
                    # Return the Readme content
                    yield 'data: {0}\r\n\r\n'.format(
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

    def _match_asset(self, match):
        url = match.group(1)
        ext = os.path.splitext(url)[1][1:]
        return 'url({0})'.format(
            self._to_data_url(url, 'font/' + ext))

    def _get_styles(self, style_urls, asset_url_path):
        """
        Gets the content of the given list of style URLs and
        inlines assets.
        """
        styles = []
        for style_url in style_urls:
            urls_inline = STYLE_ASSET_URLS_INLINE_FORMAT.format(
                asset_url_path.rstrip('/'))
            asset_content = self._download(style_url)
            content = re.sub(urls_inline, self._match_asset, asset_content)
            styles.append(content)

        return styles

    def _inline_styles(self):
        """
        Downloads the assets from the style URL list, clears it, and adds
        each style with its embedded asset to the literal style list.
        """
        styles = self._get_styles(self.assets.style_urls, url_for('asset'))
        self.assets.styles.extend(styles)
        self.assets.style_urls[:] = []

    def _retrieve_styles(self):
        """
        Retrieves the style URLs from the source and caches them. This
        is called before the first request is dispatched.
        """
        if self._styles_retrieved:
            return
        self._styles_retrieved = True

        try:
            self.assets.retrieve_styles(url_for('asset'))
        except Exception as ex:
            if self.debug:
                print(format_exc(), file=sys.stderr)
            else:
                print(' * Error: could not retrieve styles:', ex,
                      file=sys.stderr)
        if self.render_inline:
            self._inline_styles()

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
        cache_path = None
        cache_directory = self.config['CACHE_DIRECTORY']
        if cache_directory:
            cache_directory = cache_directory.format(version=__version__)
            cache_path = os.path.join(self.instance_path, cache_directory)
        return GitHubAssetManager(
            cache_path, self.config['STYLE_URLS'], self.quiet)

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
            response = c.get(route, follow_redirects=True)
            encoding = getattr(response, 'charset', 'utf-8')
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
            if isinstance(self.auth, tuple):
                username, password = self.auth
                auth_method = ('credentials: {0}'.format(username)
                               if username
                               else 'personal access token')
            else:
                auth_method = type(self.auth).__name__
            print(' * Using', auth_method, file=sys.stderr)

        # Get random port manually when needed ahead of time
        if port == 0 and open_browser:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', 0))
            port = sock.getsockname()[1]
            sock.close()

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
