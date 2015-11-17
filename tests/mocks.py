from __future__ import print_function, unicode_literals

import json

import requests
import responses
from grip import DEFAULT_API_URL, GitHubAssetManager, Grip, StdinReader

from helpers import USER_CONTEXT, input_file, output_file


class GitHubRequestsMock(responses.RequestsMock):
    auth = ('test-username', 'test-password')
    bad_auth = ('bad-username', 'bad-password')

    def __init__(self, assert_all_requests_are_fired=False):
        super(GitHubRequestsMock, self).__init__(
            assert_all_requests_are_fired=assert_all_requests_are_fired)
        self._response_map = {
            input_file('zero.md'): {
                'markdown': output_file('raw', 'zero.html'),
                'user-content': output_file('raw', 'zero-user-content.html'),
                'user-context': output_file('raw', 'zero-user-context.html'),
            },
            input_file('simple.md'): {
                'markdown': output_file('raw', 'simple.html'),
                'user-content': output_file('raw', 'simple-user-content.html'),
                'user-context': output_file('raw', 'simple-user-context.html'),
            },
            input_file('gfm-test.md'): {
                'markdown': output_file('raw', 'gfm-test.html'),
                'user-content': output_file(
                    'raw', 'gfm-test-user-content.html'),
                'user-context': output_file(
                    'raw', 'gfm-test-user-context.html'),
            },
        }
        self.add_callback(
            responses.POST, '{0}/markdown'.format(DEFAULT_API_URL),
            callback=self._markdown_request)
        self.add_callback(
            responses.POST, '{0}/markdown/raw'.format(DEFAULT_API_URL),
            callback=self._markdown_raw_request)

    def _authenticate(self, request):
        if 'Authorization' not in request.headers:
            return None
        dummy = requests.Request()
        requests.auth.HTTPBasicAuth(*self.auth)(dummy)
        if request.headers['Authorization'] != dummy.headers['Authorization']:
            return (401, {'content-type': 'application/json; charset=utf-8'},
                    '{"message":"Bad credentials"}')
        return None

    def _output_for(self, content, mode=None, context=None):
        for request_content in self._response_map:
            if request_content != content:
                continue
            responses = self._response_map[request_content]
            if mode is None or mode == 'markdown':
                return responses['markdown']
            elif context is None:
                return responses['user-content']
            elif context == USER_CONTEXT:
                return responses['user-context']
            else:
                raise ValueError(
                    'Markdown group not found for user context: {0}'.format(
                        USER_CONTEXT))
        raise ValueError('Markdown group not found for: {!r}'.format(content))

    def _decode_body(self, request):
        if 'charset=UTF-8' not in request.headers['content-type']:
            raise ValueError('Expected UTF-8 charset, got: {!r}'.format(
                request.headers['content-type']))
        return request.body.decode('utf-8') if request.body else ''

    def _markdown_request(self, request):
        r = self._authenticate(request)
        if r:
            return r
        payload = json.loads(self._decode_body(request))
        return (200, {'content-type': 'text/html'}, self._output_for(
            payload['text'], payload['mode'], payload.get('context', None)))

    def _markdown_raw_request(self, request):
        r = self._authenticate(request)
        if r:
            return r
        return (200, {'content-type': 'text/html'}, self._output_for(
            self._decode_body(request)))


class StdinReaderMock(StdinReader):
    def __init__(self, mock_stdin, *args, **kwargs):
        super(StdinReaderMock, self).__init__(*args, **kwargs)
        self._mock_stdin = mock_stdin

    def read_stdin(self):
        return self._mock_stdin


class GitHubAssetManagerMock(GitHubAssetManager):
    def __init__(self, cache_path=None, style_urls=None):
        if cache_path is None:
            cache_path = 'dummy-path'
        super(GitHubAssetManagerMock, self).__init__(cache_path, style_urls)
        self.clear_calls = 0
        self.cache_filename_calls = 0
        self.retrieve_styles_calls = 0

    def clear(self):
        self.clear_calls += 1

    def cache_filename(self, url):
        self.cache_filename_calls += 1
        return super(GitHubAssetManagerMock, self).cache_filename(url)

    def retrieve_styles(self, asset_url_path):
        self.retrieve_styles_calls += 1


class GripMock(Grip):
    def default_asset_manager(self):
        return GitHubAssetManagerMock()
